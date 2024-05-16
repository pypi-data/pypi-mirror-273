import datetime
import html
import os
import signal
import sys
import threading
from pathlib import Path
from time import sleep
from typing import Optional, Any

from flask import Flask, render_template, redirect, url_for, request, send_file
from libsrg.Config import Config
from libsrg.ElapsedTime import ElapsedTime
from libsrg.Statistics.AnalogStatsBase import AnalogStatsBase
from libsrg.Statistics.DiscreteStatsBase import DiscreteStatsBase

from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import TestBase

my_file = __file__
flask_dir = Path(my_file).parent
app_dir = flask_dir.parent.parent
template_dir = flask_dir / 'templates'
static_dir = flask_dir / 'static'

app = Flask("Santa_IW",
            static_folder=static_dir,
            template_folder=template_dir,
            )
"""
Flask Lessons Learned:
* jinja does not support f-strings in {{ }}, had to use "{val:.8g}".format(val=stat.mean())
* @app.xxxx magic only works on static functions 
* for .jinja files
   * [(<Status.OK: 0>, 3)]  did not get "<" autoescaped
   * flask.escape no longer exists
   * html.escape converted "<" to "&lt"
   * "&lt got autoescaped to "&&lt" and displayed as "&lt"
   * explicitly escaping through WebGUI.escape() and setting {% autoescape false %} passed string as intended
"""
# When the TreeRoot singleton constructs the WebGUI singleton, the WebGUI will set this module level
# variable to be a handle to the singleton
webgui: Optional["WebGUI"] = None


def webgui_self_register(me) -> Flask:
    global webgui
    webgui = me
    return app


class WebGUI(Subassembly):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly):
        """


        :param instance_config:
        :param short_name:
        :param parent:
        """
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name)  # super defines self.logger
        self.app: Flask = webgui_self_register(self)
        self._my_thread = None
        self.focus: Subassembly = self.tree_root_subassembly
        self.shutting_down = False
        self.runtime = ElapsedTime()

    def spawn(self):
        pass
        # if self._my_thread is None:
        #     self._my_thread = Thread(target=self._run_in_thread, daemon=True,name=self.name())
        #     self._my_thread.start()

    def takeover_main_thread(self):
        self.set_annotation("Flask WebGUI started in main thread")
        msg = f"@@@@ WebGui is now {threading.get_native_id()=} {threading.current_thread()=} {os.getpid()=} {self.__class__=} {self.__module__=} {__file__=} {__name__=}"
        self.logger.info(msg)
        self.log_internal_status(Status.OK, assess=True)
        port = self.config().get_item("gui_port")
        host = self.config().get_item("gui_host")
        debug = bool(self.config().get_item("gui_debug"))
        try:
            self.app.run(host=host, port=port, debug=debug)
            # sleep(60)
        except Exception as e:
            self.log_internal_status(Status.CRITICAL, "Exception", assess=True)
            self.logger.exception(e, stack_info=True, exc_info=True)
        msg = f"@@@@ WebGui is exiting {threading.get_native_id()=} {threading.current_thread()=} {os.getpid()=} {self.__class__=} {self.__module__=} {__file__=} {__name__=}"
        self.logger.info(msg)

    def _run_in_thread(self):
        pass

    def request_shutdown(self, kill: bool = False):
        self.shutting_down = True
        msg = f"Flask WebGUI commanded shutdown({kill:=})!"
        self.set_annotation(msg)
        self.logger.info(f"*********************** Shutting down WebGUI ********************************\n{msg}")
        self.tree_root_subassembly.set_annotation(msg)
        self.tree_root_subassembly.log_internal_status(Status.NODATA, msg)
        self.tree_root_subassembly.shutdown()
        sleep(10)
        self.shutdown_server()

    # noinspection PyMethodMayBeStatic
    def shutdown_server(self):
        """Raises a signal to main thread which is WebGUI to shut down."""
        signal.raise_signal(2)

    def describe_focus(self) -> str:
        out = f"Info for {self.focus.name():<30} {self.focus.latest_status()}\n"
        childs = self.focus.children()
        for child in childs:
            out += f"   {child.name():<30} {child.latest_status()}\n"
        self.logger.info(out)
        return out

    def find_subsystem(self, name: str) -> Subassembly | None:
        val = self.config().get_item(name, default=0)
        if isinstance(val, Subassembly):
            return val
        if name == "home" or name == "top" or name == "root":
            self.focus = self.tree_root_subassembly
        else:
            self.focus = Subassembly.get_subassembly_by_name(name)
        if self.focus is None:
            self.logger.info(f"No subassembly for {name}")
            self.focus = self.tree_root_subassembly
        self.logger.info(f"Focus set to {self.focus.name():<}")
        return self.focus

    def log(self, message: str) -> None:
        self.logger.info(message)

    # noinspection PyMethodMayBeStatic
    def sort_config_list(self,sub: Subassembly):
        lst=sub.config().to_list()
        lst.sort(key=lambda x: f"{x[2]:02n}{x[0]}")
        return lst

    def prepare_focus_page(self, name: str, **extras) -> Config:
        """
This method prepares a dict with the following template inputs:
* title - title for page
* focus - Subassembly to display
* trail - list of subassemblies from root to focus inclusive
* child_nodes - non-test children of focus
* child_tests - test children of focus
* body - block of preformatted text
* time_slug - footer text (expected to include time of day)

        :param name:
        :return:
        """
        now = datetime.datetime.now()
        current_time_txt = now.strftime("%Y-%m-%d %H:%M:%S")
        self.runtime.stop()
        elapsed_time_txt = self.runtime.elapsed_asc()
        focus: Subassembly = self.find_subsystem(name) if not self.shutting_down else self.tree_root_subassembly
        version = self.config().get_item("SANTA_IW_VERSION")
        branch = self.config().get_item("branch", default="local")
        flask_config = Config({
            "title": f"SHUTDOWN",
            "root_tint": self.tree_root_subassembly.latest_status().tint(),
            "focus_tint": focus.latest_status().tint(),
            "focus": focus,
            "root": self.tree_root_subassembly,
            "parent": focus.parent(),
            "stepparent": focus.stepparent(),
            "trail": [focus],
            "child_nodes": None,
            "child_tests": None,
            "suspects": None,
            "version": f"{version}/{branch}",
            "python_version": sys.version,
            "body": focus.report(),
            "current_time_txt": current_time_txt,
            "elapsed_time_txt": elapsed_time_txt,
            "astats": None,
            "dstats": None,
            "istats": None,
            "cstats": None,
            "webgui": self,
            "refresh_interval": None,
            "focus_config_list": self.sort_config_list(focus),
            "localhost": self.config().get_item("localhost_hostname", default="localhost"),
            "image": None,
        })
        if self.shutting_down:
            self.logger.info(f"Preparing shutdown page")
            flask_config.set_item("title", "SHUTDOWN")
            return flask_config
        self.logger.info(f"Preparing page for {name}")
        sub = focus
        flask_config.set_item("title", f"Status for {focus.name()}")

        trail = []
        while sub is not None:
            trail.append(sub)
            sub = sub.parent()
        trail.reverse()
        flask_config.set_item("trail", trail)

        child_nodes = []
        child_tests = []
        for child in focus.children():
            if isinstance(child, TestBase):
                child_tests.append(child)
            else:
                child_nodes.append(child)
        flask_config.set_item("child_nodes", child_nodes)
        flask_config.set_item("child_tests", child_tests)

        suspects = focus.suspects()
        flask_config.set_item("suspects", suspects)

        flask_config.set_item("istats", focus.get_internal_status_map())
        flask_config.set_item("cstats", focus.get_child_status_map())
        flask_config.set_item("astats", AnalogStatsBase.find_in_object(focus))
        flask_config.set_item("dstats", DiscreteStatsBase.find_in_object(focus))
        flask_config.set_item("refresh_interval", self.config().get_item("gui_page_refresh_interval"))

        astat = extras.get("astat", None)
        if astat is not None:
            png_ = "/plot/" + str(astat) + ".png"
            flask_config.set_item("body", f"image is {png_}")
            flask_config.set_item("image", png_)

        return flask_config

    # noinspection PyBroadException
    @staticmethod
    def format_8g(val):
        try:
            return f"{val:.8g}"
        except Exception:
            return val

    # noinspection PyMethodMayBeStatic
    def escape(self, obj: Any) -> str:
        txt = html.escape(str(obj), quote=False)
        return txt


@app.route("/")
def jump_home():
    focus = webgui.find_subsystem("home")
    ssname = focus.name()
    return redirect(url_for("focus_page", ssname=ssname))


@app.route("/jump/<token>")
def jump(token):
    focus = webgui.find_subsystem(token)
    ssname = focus.name()
    return redirect(url_for("focus_page", ssname=ssname))


@app.route("/focus/<ssname>")
def focus_page(ssname):
    extras = request.args
    config: Config = webgui.prepare_focus_page(ssname, **extras)
    return render_template("focus_page.html.jinja", **config)


@app.route("/reset/<ssname>")
def reset_page(ssname):
    focus = webgui.find_subsystem(ssname)
    focus.deep_reset()
    return redirect(url_for("focus_page", ssname=ssname))


@app.route("/ack/<ssname>")
def ack_page(ssname):
    focus = webgui.find_subsystem(ssname)
    focus.clear_attention()
    return redirect(url_for("focus_page", ssname=ssname))


@app.route("/run/<ssname>")
def run_page(ssname):
    focus = webgui.find_subsystem(ssname)
    focus.mark_test_due_to_run(True)
    return redirect(url_for("focus_page", ssname=ssname))


@app.route("/enable/<ssname>")
def enable_page(ssname):
    focus = webgui.find_subsystem(ssname)
    focus.mark_subsystem_enabled(True, deep=True)
    return redirect(url_for("focus_page", ssname=ssname))


@app.route("/disable/<ssname>")
def disable_page(ssname):
    focus = webgui.find_subsystem(ssname)
    focus.mark_subsystem_enabled(False, deep=True)
    return redirect(url_for("focus_page", ssname=ssname))


@app.route("/control")
def control():
    config: Config = webgui.prepare_focus_page("home")
    return render_template("control_page.html.jinja", **config)


@app.route("/shutdown/")
def shutdown():
    webgui.logger.info("shutdown Page")
    webgui.request_shutdown()
    # redirect is important here!
    # if firefox was refreshing a shutdown page when the connection died,
    # it tended to reconnect to the shutdown page and kill a restarted system.
    return redirect(url_for("focus_page", ssname="home"))


@app.route("/kill/")
def kill_page():
    webgui.logger.info("kill Page")
    webgui.request_shutdown(kill=True)
    # redirect is important here!
    # if firefox was refreshing a shutdown page when the connection died,
    # it tended to reconnect to the shutdown page and kill a restarted system.
    return redirect(url_for("focus_page", ssname="home"))


# def get_astat_image(sensor):
#     file = webgui.config().get_item("data_recording_db")
#     path = 'sqlite:///' + file
#     engine = sqlalchemy.create_engine(path)
#     cmd = f"SELECT time,value FROM asamples WHERE name='{sensor}'"
#     df: DataFrame = pd.read_sql_query(cmd, engine)
#     df['DateTime'] = pd.to_datetime(df['time'], unit='s')
#     fig = df.plot(y='value', x='DateTime').get_figure()
#     img = BytesIO()
#     fig.savefig(img, format='png')
#     img.seek(0)
#     return img


@app.route('/plot/<sensor>.png')
def plot_sensor(sensor):
    """Views for rendering city specific charts"""
    webgui.logger.info("Plot Sensor start")
    data_recording = webgui.config().get_item("data_recording")
    img = data_recording.get_astat_image(sensor)
    response = send_file(img, mimetype='image/png')
    get_headers(response)
    webgui.logger.info("Plot Sensor end")
    return response


def get_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
