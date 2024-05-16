from libsrg.Config import Config

from Santa_IW.Node import Node
from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import TestBase


class Naughty(Subassembly):
    """
    Data Recording subassembly

    """

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name)  # super defines self.logger
        self.sep = self.config().get_item("tree_name_separator")
        self._suspects: set[Subassembly] = set()
        self.clear_attention_busy = False

    def start(self) -> None:
        self.set_annotation("Setting up to observe misbehaviour...")
        self.log_internal_status(Status.OK, "Started", assess=True)

        Subassembly.register_global_status_observer(self.observe_subsystem_status)

        self.log_internal_status(Status.OK, "Running...", assess=True)
        # self.logger.info("Finished")

    # noinspection PyUnusedLocal
    def observe_subsystem_status(self, child: Subassembly, status: Status, attention: bool, assess=True) -> None:
        if status.value > Status.OK.value or attention and (isinstance(child, TestBase) or isinstance(child, Node)):
            self._suspects |= {child}
            msg = f"Add Suspect {child.short_name()} {status=} {attention=}"
        else:
            self._suspects -= {child}
            msg = f"Clear Suspect {child.short_name()} {status=} {attention=}"
        self.logger.info(msg)
        self.set_annotation(msg)

    def clear_attention(self):
        if self.clear_attention_busy:
            self.log_internal_status(Status.OK, "Suppressing recursive clear_attention", assess=True)
        else:
            self.clear_attention_busy = True
            self.log_internal_status(Status.OK, "Clearing attention...", assess=True)
            # self._suspects.clear()
            lst = list(self._suspects)
            for sub in lst:
                sub.clear_attention()
            super().clear_attention()
            self.log_internal_status(Status.OK, "Done clearing attention", assess=True)
            self.clear_attention_busy = False

    def suspects(self) -> list["Subassembly"]:
        sus = set(super().suspects())
        sus |= self._suspects
        sus -= {self}
        lst = list(sus)
        lst.sort()
        return lst

    def shutdown_instance(self):
        super().shutdown_instance()
