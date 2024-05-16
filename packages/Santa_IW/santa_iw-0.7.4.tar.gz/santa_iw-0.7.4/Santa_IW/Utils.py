import argparse
import functools
import json
import logging
from collections import ChainMap
from pathlib import Path
from typing import Any, Callable, Optional


def log_entry_and_exit(func: Callable[..., Any], logger=None) -> Callable[..., Any]:
    mylogger = logger or logging.getLogger(__name__)

    @functools.wraps(func)
    def wrapper(*uargs: Any, **kwargs: Any) -> Any:
        mylogger.info(f"Calling {func.__name__}")
        value = func(*uargs, **kwargs)
        mylogger.info(f"Finished {func.__name__}")
        return value

    return wrapper


def map_chain_as_str(amap) -> str:
    out = "**** " + str(amap) + "\n"
    if isinstance(amap, ChainMap):
        for cmap in amap.maps:
            out += f"** {cmap}\n"
    for key in amap.keys():
        v = amap[key]
        out += f"      {key}: {v}\n"
    return out


class Namespace:
    pass


def dict_to_namespace(adict: dict[str, Any]) -> Namespace:
    namespace = Namespace()
    for key, value in adict.items():
        setattr(namespace, key, value)
    return namespace


def namespace_to_dict(ns: Namespace | argparse.Namespace) -> dict[str, Any]:
    return vars(ns)


def get_arg(dct: dict[str:Any], *names: str, default=None, allow_none=False) -> Any:
    for name in names:
        if name in dct:
            return dct[name]
    if default is not None:
        return default
    if allow_none:
        return None
    raise KeyError(f"keys not found: {names}")


class ConfigLoader:
    def __init__(self, config_path: str | Path) -> None:
        self._config_path = Path(config_path)
        self._ok = False
        self._config: Optional[dict[str, Any]] = None
        self._caught: Optional[Exception] = None
        self._text: Optional[str] = None
        try:
            with open(config_path, "r") as f:
                self._text = f.read()
            # noinspection PyBroadException
            self._config = json.loads(self._text)
            self._ok = True
        except Exception as e:
            logging.getLogger(__name__).exception(f"Error loading {config_path}: {e}", stack_info=True, exc_info=True)
            self._caught = e

    def die_on_failure(self):
        if not self._ok:
            logging.getLogger(__name__).critical(f"FATAL Could not load {self._config_path.absolute()} {self._caught}.")
            exit(2)

    def ok(self):
        return self._ok

    def caught(self):
        return self._caught

    def text(self):
        return self._text

    def config(self) -> dict[str, Any]:
        if self._caught is not None:
            raise self._caught
        return self._config


if __name__ == "__main__":
    args = argparse.Namespace(aa=1, bb='from args')
    vargs = vars(args)
    print(args, vargs)
    a = {1: "one", 2: "two", 3: "three", "bb": "lista"}
    b = {"a": "A", "b": "Blist"}
    c = ChainMap(a, b, vargs)
    print(map_chain_as_str(c))
    val = get_arg(c, "aa", "bb")
    print(val)
    val = get_arg(c, "axa", "bb")
    print(val)
    val = get_arg(c, "axa", "bxb", default="zz")
    print(val)
    val = get_arg(c, "axa", "bxb", allow_none=True)
    print(val)
