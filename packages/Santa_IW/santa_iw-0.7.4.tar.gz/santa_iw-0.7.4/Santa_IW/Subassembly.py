import logging
import os
import threading
from collections import ChainMap
from threading import Event
from typing import Any, Self, Callable, Optional

import scipy.constants
from libsrg.Config import Config
from libsrg.ElapsedTime import ElapsedTime
from libsrg.Statistics.ADStatsBase import ADStatsBase
from libsrg.Statistics.DiscreteStatsCumulative import DiscreteStatsCumulative

from Santa_IW.Status import Status, StatusSummation


class Subassembly:
    """
    A subassembly is part of a tree structure of subassemblies.
    Each subassembly has a parent except for one subassembly at the root of a tree structure.
    At each level, a given subassembly can have one parent (or zero parents for the root of the tree).
    At each level, a given subassembly can have zero or more direct_children.

    Note: the phrase parent or child refers to a subassembly above or below the given subassembly
    - parent: zero or one Subassembiles which will start/spawn/monitor zero or more direct_children
    - stepparent: zero or one Subassembiles which monitor zero or more step_children but do not start/spawn them
    - directchild: A subassembly whose start/spawn actions are controlled by a parent and is monitored by that parent
    - stepchild: A subassembly NOT controlled by a stepparent but monitored by that stepparent
    - child: Either a directchild or a stepchild

    """

    tree_root_subassembly: Optional[Self] = None
    """ This is the root subassembly instance, which will be of type TreeRoot in the Santa_IW application """
    tree_root_name: str | None = None
    """ This is the name of the root subassembly instance """

    all_subassemblies: dict[str, "Subassembly"] = {}
    """ This is a mapping of instance name to instance for all subassemblies.
     Instance names are required to be globally unique."""

    global_status_observers: list[Callable] = []
    """This is a list of observers (Callables to callback functions) registered to receive status updates from all instances of Subassembly."""

    sc = scipy.constants
    """
    scipy.constants provides constants for converting minutes and hours to seconds
    It can be accessed from any subclass of Subassembly or instance of a subclass.
    {
    "period": 7*TestBase.sc.minutes # results in 420 seconds
    }
    """

    ###################################################
    # Classmethods
    ###################################################

    @classmethod
    def reset_class_for_unittest(cls):
        cls.all_subassemblies = {}
        cls.secret_lookup = {}
        cls.global_status_observers = []
        cls.tree_root_subassembly = None
        cls.tree_root_name = None

    @classmethod
    def _register_subassembly_with_class(cls, subassembly: "Subassembly"):
        nam = subassembly.name()
        logging.info(f"Registering subassembly {nam}")
        cls.all_subassemblies[nam] = subassembly
        if cls.tree_root_subassembly is None:
            logging.info(f"Setting tree root subassembly to {nam}")
            cls.tree_root_subassembly = subassembly
            cls.tree_root_name = nam
            logging.info(f"Tree root is now {cls.tree_root_subassembly.name()}")

    @classmethod
    def subassembly_map(cls) -> dict[str, "Subassembly"]:
        return cls.all_subassemblies

    @classmethod
    def get_subassembly_by_name(cls, name: str) -> Optional["Subassembly"]:
        return cls.all_subassemblies.get(name, None)

    @classmethod
    def get_tree_root_subassembly(cls) -> Optional["Subassembly"]:
        return cls.tree_root_subassembly

    @classmethod
    def register_global_status_observer(cls, observer: Callable):
        cls.global_status_observers.append(observer)

    @classmethod
    def unregister_global_status_observer(cls, observer: Callable):
        cls.global_status_observers.remove(observer)

    ###################################################
    # Constructor and Dunders
    ###################################################

    def __init__(self, instance_config: Config, short_name: str,
                 parent: Optional["Subassembly"], stepparent: Optional["Subassembly"] = None) -> None:
        self._status_lock=threading.RLock()
        self._pre_attention_status = None
        self._attention_flag = False
        self.logger = logging.getLogger(self.__class__.__name__)
        self._parent = parent
        self._stepparent = stepparent
        tree_root = Subassembly.get_tree_root_subassembly()
        if parent is None:
            self.logger.info(f"Creating tree root subassembly {self.__class__.__name__}")
            if tree_root is not None and tree_root != self:
                self.logger.critical(f"Cannot create two subassemblies with no parent: {self.tree_root_subassembly}")
                raise ValueError(f"Cannot create two subassemblies with no parent")
            self._short_name = short_name
            self._name = short_name
            self._ancestor_short_names = [self._name]
        else:
            self._short_name = short_name
            self._name = parent.prefix_name(self._short_name)
            # _ancestor_short_names is a list of all ancestors short_names, oldest first for sorting
            self._ancestor_short_names = self._parent._ancestor_short_names.copy()
            self._ancestor_short_names.append(self._short_name)

        self.logger.info(
            f"@@@@ {self.__class__.__name__} {self.name()} initialized by {threading.get_native_id()=} {threading.current_thread()=} {os.getpid()=}")
        # can register after name set
        Subassembly._register_subassembly_with_class(self)
        # Line above should register the first instance as root of tree
        tree_root = Subassembly.get_tree_root_subassembly()
        if tree_root is None:
            raise Exception(f"Empty tree root subassembly")
        self._instance_config = instance_config
        if stepparent and not parent:
            raise Exception(f"Cannot create subassemblies with stepparent but no parent")
        elif stepparent:
            self._merged_config = Config(self.instance_config(), stepparent.instance_config(), parent.config())
        elif parent:
            self._merged_config = Config(self.instance_config(), parent.config())
        else:
            self._merged_config = self.instance_config()

        # these are always set opposite to each other
        # Top level thread can wait for treeroot to be disabled before shutdown
        self._subassembly_enabled = Event()
        self._subassembly_disabled = Event()
        self.mark_subsystem_enabled(False)  # initially disabled

        self._registered_direct_children: dict[str, Self] = {}
        self._registered_stepchildren: dict[str, Self] = {}
        self._registered_children: ChainMap[str, Self] = ChainMap(self._registered_direct_children,
                                                                  self._registered_stepchildren)

        self._child_summation = StatusSummation(name="child")
        self._internal_summation = StatusSummation(name="internal")
        self._overall_summation = StatusSummation(name="overall")
        self._first_status = True
        self._always_send_assessments = False

        self._registered_status_observers: list[Callable] = []
        self._internal_assess_stats = DiscreteStatsCumulative(self.prefix_name("InternalAssessment"))
        self._child_assess_stats = DiscreteStatsCumulative(self.prefix_name("ChildAssessment"))
        self._overall_assess_stats = DiscreteStatsCumulative(self.prefix_name("OverallAssessment"))
        self._nominal_class = self.config().get_item("test_type", default=self.__class__.__name__)
        self._since_last_notify = ElapsedTime("Elapsed Since Last Notify")
        self._observer_period_nochange = float(self.config().get_item("observer_period_nochange", default=50.))

        # We don't want to inherit this parameter, only valid if direct set in instance_config
        depth,val=self.config().find_item_depth("propagate_child_status_in_overall")
        self._propagate_child_status_in_overall = (depth!=0) or bool(val)
        if not self._propagate_child_status_in_overall:
            self.log_internal_status(Status.OK,f"{self._short_name} has propagate_child_status_in_overall=False")

        self._pull_up_child_annotation = bool(self.config().get_item("pull_up_child_annotation"))
        # keep these last
        if parent is not None:
            parent.child_registers_with_parent(self)
        if stepparent is not None:
            stepparent.child_registers_with_parent(self, stepparent=True)

    def __lt__(self, other: Self):
        """ support sorting by name_list (parent first) """
        return self._ancestor_short_names < other._ancestor_short_names

    def __str__(self):
        return f"{self.__class__.__name__}({self._name})"

    ###################################################
    # Config
    ###################################################

    def config(self) -> Config[str, Any]:
        return self._merged_config

    def instance_config(self) -> Config[str, Any]:
        return self._instance_config

    ###################################################
    # Start/Spawn/Enable
    ###################################################
    def mark_subsystem_enabled(self, enable: bool = True, deep: bool = False):
        if enable:
            self._subassembly_disabled.clear()
            self._subassembly_enabled.set()
        else:

            self._subassembly_enabled.clear()
            self._subassembly_disabled.set()
        if deep:
            for child in self.children():
                child.mark_subsystem_enabled(enable=enable, deep=deep)

    def subsystem_is_enabled(self):
        return self._subassembly_enabled.is_set()

    def start(self):
        pass

    def spawn(self):
        self.logger.info(f"Spawning Subassembly {self} with direct_children {self._registered_direct_children}")
        for child in self._registered_direct_children.values():
            # noinspection PyTypeChecker
            self.logger.info(f"{self} Spawning {child}")
            child.mark_subsystem_enabled()
            child.spawn()
        self.mark_subsystem_enabled()

    ###################################################
    # parent/child/naming
    ###################################################
    def prefix_name(self, prefix: str, suffix: Optional[str] = None) -> str:
        if suffix is None:
            suffix = self._name
        out = prefix + self.config().get_item("tree_name_separator") + suffix
        out = out.replace("/", "⧸")
        out = out.replace(" ", "﹇")
        out = out.replace("+", "＋")
        return out

    def name(self):
        return self._name

    def parent(self) -> Self | None:
        return self._parent

    def stepparent(self) -> Self | None:
        return self._stepparent

    def short_name(self) -> str:
        return self._short_name

    def children(self) -> list["Subassembly"]:
        """return set of all children of this subassembly"""
        res = list(self._registered_children.values())
        res.sort()
        return res

    def child_registers_with_parent(self, child: Self, stepparent=False) -> None:
        """
        Registers child subassembly with parent or stepparent
        """
        child_name = child.name()
        if child_name in self._registered_children:
            msg = f"Duplicate Child Name {child_name} below {self.name()}"
            self.logger.error(msg)
            raise KeyError(msg)
        if stepparent:
            self._registered_stepchildren[child_name] = child
        else:
            self._registered_direct_children[child_name] = child
        child.register_status_observer(self.observe_child_status)

    ###################################################
    # attention/annotation
    ###################################################
    def annotation(self) -> str:
        out = ""
        if self._attention_flag:
            out += self.config().get_item("tree_attention_char")
        if len(out) > 0:
            out += " "
        ann = self._overall_summation.message()
        if ann:
            out += str(ann)
        return out

    def set_attention(self):
        self._attention_flag = True

    def update_attention(self, new_status):
        if self._pre_attention_status is not None and self._pre_attention_status != new_status:
            self.set_attention()
        self._pre_attention_status = new_status

    def clear_attention(self):
        for child in self.children():
            child.clear_attention()
        self._pre_attention_status = None
        self._attention_flag = False
        self.log_internal_status(Status.NODATA, f"Cleared attention flag {self.name()}", assess=True)

    def set_annotation(self, text: str | None = None) -> None:
        self._overall_summation.set_message(text)

    ###################################################
    # Status Summation
    ###################################################
    def latest_status(self) -> Status:
        return self._overall_summation.worst()

    def assess_overall_status(self) -> Status:
        with self._status_lock:
            prior_status = self._overall_summation.worst()

            self._child_assess_stats.sample(self._child_summation.worst())
            if self._propagate_child_status_in_overall:
                self._overall_summation.add_from(self._child_summation)

            self._internal_assess_stats.sample(self._internal_summation.worst())

            self._overall_summation.add_from(self._internal_summation)

            worst = self._overall_summation.worst()

            self._overall_assess_stats.sample(worst)

            self.new_overall_status(prior_status, worst)

            changed = prior_status != worst

            # current is current elapsed time since start, without stopping timer
            age_last_status = self._since_last_notify.current()
            stale = age_last_status > self._observer_period_nochange
            send = stale or changed or self._first_status or self._always_send_assessments
            self.update_attention(worst)
            self.logger.info(
                f"Overall Status {worst.name}<-{prior_status.name} " +
                f"{send=} {changed=} {stale=} {age_last_status=}")
            if send:
                self.notify_status_observers()
                self._first_status = False

        return worst

    def new_overall_status(self, old_status: Status, new_status: Status):
        """
        called after evaluation, but before notification of observers
        intended to be overridden by TestBase
        """
        pass

    def get_internal_status_map(self) -> dict[Any, Status]:
        return self._internal_summation.as_dict()

    def get_child_status_map(self) -> dict[Any, Status]:
        return self._child_summation.as_dict()

    def log_internal_status(self, status: Status, tag: str | None = None, message: str | None = None,
                            assess=False) -> None:
        """
        Internal status could be used by subtests within a single test execution, or
        processing steps in a factory or other process.

        Tests should reset_internal_status at the start of a test cycle and call
        assess_status at test completion to summarize and propagate results.
        This will prevent partial results from looking like a test is thrashing.

        Factories and other processes would probably want to set assess=true directly on
        the call to set_internal_status.

        :param tag:
        :param status:
        :param message:
        :param assess:
        :return:
        """
        assert isinstance(status, Status)
        if message is not None and tag is None:
            tag = message
        if tag is None:
            tag = "internal status"
        self._internal_summation.add(status, tag=tag, message=message)
        if message is not None:
            if status.is_bad():
                self.logger.warning(message)
            else:
                self.logger.info(message)
            self.set_annotation(message)

        if assess:
            self.reset_one_internal_status("INTERNAL_ASSESSMENT")
            self.assess_overall_status()
            self.log_internal_status(self._internal_summation.worst(), "INTERNAL_ASSESSMENT", assess=False)

    def reset_one_internal_status(self, tag: Any):
        self._internal_summation.remove(tag)

    def reset_internal_status(self) -> None:
        self._internal_summation.reset()
        self._child_summation.reset()
        self.log_internal_status(Status.OK, "INTERNAL_STATUS reset", assess=True)

    ###################################################
    # Status Observers
    ###################################################
    def observe_child_status(self, child: Self, status: Status, attention: bool, assess=True) -> None:
        self._child_summation.add(status, tag=child)
        if attention and self._propagate_child_status_in_overall:
            self.set_attention()
        msg = child._overall_summation.message()
        if self._pull_up_child_annotation and msg and len(str(msg)) > 4:
            self.set_annotation(f"{self.config().get_item('tree_child_data_char')} {msg}")
        self.logger.info(f"Child {child.name()} reported {status} to {self.name()}")
        if assess:
            self.assess_overall_status()

    def notify_status_observers(self):
        with self._status_lock:
            worst = self._overall_summation.worst()
        thread = threading.Thread(target=self._notify_in_thread, args=(worst,), daemon=True)
        thread.start()
        self._since_last_notify.start()

    def _notify_in_thread(self, worst):
        for observer in self._registered_status_observers:
            observer(self, worst, attention=self._attention_flag)
        for observer in self.global_status_observers:
            observer(self, worst, attention=self._attention_flag)

    def register_status_observer(self, observer: Callable):
        self._registered_status_observers.append(observer)

    def unregister_status_observer(self, observer: Callable):
        self._registered_status_observers.remove(observer)

    ###################################################
    # Test runs
    ###################################################
    def mark_test_due_to_run(self, enable: bool = True):
        for child in self.children():
            child.mark_test_due_to_run(enable)

    def queue_test_on_node(self, test: Self) -> None:
        self.logger.critical("Subassembly does not implement queue_test_on_node")
        raise NotImplementedError("Subassembly does not implement queue_test_on_node")

    ###################################################
    # Misc
    ###################################################

    def deep_reset(self) -> None:
        self.logger.info(f"deep_reset called at {self._name}")
        for child in self.children():
            child.deep_reset()
        self.reset_internal_status()
        stats = ADStatsBase.find_in_object(self)
        for stat in stats:
            stat.reset()

    def report(self) -> str:
        try:
            out = f"{self._name} instance of {self.__class__.__name__}\n"
            # out += "Configuration Data (merged)\n{\n"
            # keys = list(self._merged_config.keys())
            # keys.sort()
            # for k in keys:
            #     v= self._merged_config.get(k,None)
            #     out += f"   {k!r:<30}: {v!r}\n"
            # out += "}\n---------------------"
            return out
        except Exception as e:
            self.logger.error(f"{self._name} {e}", stack_info=True, exc_info=True)
            raise e

    def suspects(self) -> list[Self]:
        return []

    def shutdown(self):
        """
        Shutdown all children then shutdown_instance on self

        Note that this method will typically be called from a WebGUI thread and should return
        to caller without trying to directly exit the calling thread.
        :return: None
        """
        for child in self.children():
            child.shutdown()
        self.mark_subsystem_enabled(False)
        self.shutdown_instance()

    def shutdown_instance(self):
        """
        Close any files or connections owned by this subassembly. Subassembly has already been marked disabled.

        Note that this method will typically be called from a WebGUI thread and should return
        to caller without trying to directly exit the calling thread.
        :return: None
        """
        pass
