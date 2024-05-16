import json
from pathlib import Path
from typing import Any

from libsrg.Config import Config

from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly


class TemplateFactory(Subassembly):
    """
    Factory for creating Nodes from json data.

    """

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name)  # super defines self.logger
        # self.logger.info(map_chain_as_str(self.args))
        self.template_dict: dict[str, Any] = {}
        self.template_names_not_found: set[str] = set()
        self.template_used_by: dict[str, set[str]] = {}

    def start(self) -> None:
        self.set_annotation("Loading Templates...")
        self.log_internal_status(Status.OK, "Started", assess=True)
        # self.logger.info("Started")
        # self.logger.info(map_chain_as_str(self.args))
        template_dirs = self.config().get_item("template_dirs")
        for template_dir in template_dirs:
            dpath = Path(template_dir).resolve()
            if not dpath.is_dir():
                self.log_internal_status(Status.WARNING, f"Not a directory: {str(dpath)!r}", assess=True)
            else:
                self.log_internal_status(Status.OK, f"Loading {dpath}", assess=True)
                for template_file in dpath.glob("*.json"):
                    try:
                        self.logger.info(f"loading {template_file}")
                        with open(template_file, "r") as f:
                            data = json.load(f)
                        self.logger.info(f"parsed {template_file} to {data}")
                        template_name = template_file.stem
                        if template_name in self.template_dict:
                            self.log_internal_status(Status.WARNING,
                                                     f"Template {template_name} already loaded, ignoring {template_file}")
                        else:
                            self.template_dict[template_name] = data
                            self.template_used_by[template_name] = set()
                    except Exception as e:
                        self.logger.exception(e, stack_info=True, exc_info=True)
                        self.log_internal_status(Status.WARNING, f"Template did not load {template_file} {e}")
        self.log_internal_status(Status.OK, message=f"Loaded {len(self.template_dict)} Templates, {len(self.template_names_not_found)} names not found", assess=True)
        # self.logger.info("Finished")



    def apply_templates(self, data: Config) -> Config:
        pending = data.get("templates", []).copy()
        applied = []
        if "tests" not in data:
            data["tests"] = []
        while len(pending) > 0:
            template_name = pending.pop(0)
            if not isinstance(template_name, str):
                self.log_internal_status(Status.WARNING, f"Template name {template_name} is {type(template_name)}")
                self.logger.warning(f"Unexpected Template name {template_name} in {data}")
                continue
            if template_name in applied:
                msg = f"template {template_name} reload ignored"
                self.logger.warning(msg)
                self.log_internal_status(Status.WARNING, msg, assess=True)

                continue
            applied.append(template_name)
            if template_name not in self.template_dict:
                msg = f"template {template_name} requested but not found"
                self.logger.warning(msg)
                self.log_internal_status(Status.WARNING, msg, assess=True)
                self.template_names_not_found |= {template_name}
                continue
            template = self.template_dict[template_name]
            self.template_used_by[template_name] |= {data.get_item("short_name")}
            for test_x in template.get("tests", []):
                data["tests"].append(test_x)
            for template_x in template.get("templates", []):
                pending.append(template_x)
        data["templates_applied"] = applied

        return data  # also modified in place

    def report_all_templates(self) -> str:
        out = ""
        if self.template_names_not_found:
            out += f"Templates not found {self.template_names_not_found}\n"
        out += "\nTemplate Usage:\n"
        names: list[str] = list(self.template_used_by.keys())
        names.sort()
        for name in names:
            val = self.template_used_by[name]
            if len(val) != 0:
                out += f"\t{name}: {val}\n"
        out += "\nTemplates Not Used:\n"
        for name in names:
            val = self.template_used_by[name]
            if len(val) == 0:
                out += f"\t{name}\n"

        return out

    def report(self) -> str:
        out = super().report()
        out += self.report_all_templates()
        return out
