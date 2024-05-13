import platform
from abc import ABC, abstractmethod
from typing import Any, Type


class FunctionClass(ABC):
    def __new__(cls, *args, **kwargs) -> Any:
        instance = super().__new__(cls)
        return instance(*args, **kwargs)

    @abstractmethod
    def __call__(self, *args, **kwargs): ...


class is_sys(FunctionClass):
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MACOS = 'Darwin'

    def __new__(cls, os_name: str) -> bool:
        return super().__new__(cls, os_name)

    def __call__(self, os_name: str) -> bool:
        this_os_name = platform.system()
        if os_name == this_os_name:
            return True
        return False


def recursive_convert(data: list | tuple, to: Type) -> tuple | list:
    """Recursively convert the lists and tuples are nested within each other to only tuples or lists"""
    if isinstance(data, (list, tuple)):
        return to(recursive_convert(item, to=to) for item in data)
    return data
    