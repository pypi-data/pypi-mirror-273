import logging
import threading
from enum import Enum
from typing import Any, Optional, Self


# NAGIOS return codes :
# https://nagios-plugins.org/doc/guidelines.html#AEN78

class Status(Enum):
    NODATA = (-1, 'grey', 'lightgrey',"💤")
    OK = (0, 'lime', 'lightgreen',"✅")
    UNKNOWN = (1, 'magenta', '#f1a7fe',"❓")
    MAINT = (2, 'cyan', '#e0ffff',"🔧")
    WARNING = (3, 'yellow', 'lightyellow',"🚧")
    CRITICAL = (4, 'red', '#ffc0cb',"🚨")

    def __init__(self, rank, fg, tint,emoji):
        self._rank = rank
        self._fg = fg
        self._bg = 'black'
        self._tint = tint
        self._emoji = emoji

    def __lt__(self, other: Self):
        return self._rank < other._rank

    def emoji(self)->str:
        return self._emoji

    def style(self) -> str:
        return f'color:{self._fg};background-color:{self._bg};'

    def tint(self) -> str:
        return f'background-color:{self._tint};'

    def is_ok(self) -> bool:
        return self == Status.OK

    def is_bad(self) -> bool:
        return self._rank > 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name!r}"

    def html_color(self) -> str:
        return self._fg


class StatusSummation:
    def __init__(self, initial: list[Status] | dict[Any, Status] | None = None, name: Optional[str] = None) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._name = name if name else "???"
        self._imap: dict[Any, Status] = {}
        self._message = None
        self._lock = threading.Lock()
        self._cached_worst: Optional[Status] = None
        if initial:
            self.add_bulk(initial)

    def as_dict(self) -> dict[Any, Status]:
        with self._lock:
            return self._imap.copy()

    def copy_from(self, other: Self):
        with self._lock:
            with other._lock:
                self._message = other._message
                self._imap = other._imap.copy()
                self._message = other._message
                self._cached_worst = other._cached_worst

    def message(self) -> str:
        return self._message

    def set_message(self, msg: str) -> None:
        with self._lock:
            self._message = msg

    def name(self) -> str:
        return self._name

    def add_from(self, other: Self, tag: Optional[str] = None, copy_message: bool = True) -> None:
        if tag is None:
            tag = other.name()
        if copy_message and other._message:
            self._message = other._message
        self.add(other.worst(), tag=tag)

    def add_bulk(self, bulk: list[Status] | dict[Any, Status]):
        if isinstance(bulk, list):
            for pair in enumerate(bulk):
                self.add(pair[1], tag=str(pair[0]))
        elif isinstance(bulk, dict):
            for k, v in bulk.items():
                self.add(v, tag=k)

    def reset(self):
        with self._lock:
            self._imap.clear()
            self._message = None
            self._cached_worst = None

    def add(self, status: Status, tag: Optional[str] = None, message: Optional[str] = None) -> None:
        assert isinstance(status, Status)
        with self._lock:
            if tag is None:
                if message is None:
                    tag = str(len(self._imap))
                else:
                    tag = message
            self._imap[tag] = status
            self._cached_worst = None
            if message:
                self._message = message

    def remove(self, tag: Any) -> None:
        with self._lock:
            if tag in self._imap:
                self._imap.pop(tag)

    def worst(self, default=Status.OK) -> Status:
        with self._lock:
            if self._cached_worst:
                return self._cached_worst
            lst = self._imap.values()
            if len(lst) == 0:
                w = default
            else:
                w = max(lst)
                # if w == Status.NODATA:
                #     w = default
            self._cached_worst = w
            return w
