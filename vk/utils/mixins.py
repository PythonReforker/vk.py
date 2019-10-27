"""
Author: https://github.com/aiogram/aiogram/blob/dev-2.x/aiogram/utils/mixins.py
"""
import contextvars
from typing import Type
from typing import TypeVar

T = TypeVar("T")


class ContextInstanceMixin:
    def __init_subclass__(cls, **kwargs):
        cls.__context_instance = contextvars.ContextVar("instance_" + cls.__name__)
        return cls

    @classmethod
    def get_current(cls: Type[T], no_error=True) -> T:
        if no_error:
            return cls.__context_instance.get(None)
        return cls.__context_instance.get()

    @classmethod
    def set_current(cls: Type[T], value: T):
        if not isinstance(value, cls):
            raise TypeError(
                f"Value should be instance of '{cls.__name__}' not '{type(value).__name__}'"
            )
        cls.__context_instance.set(value)


class MetaMixin:

    # default meta tags:
    # name: str
    # description: str
    # deprecated: bool

    # meta = {
    # "name": "My object which contain meta variable",
    # "description": "Oh... i don't know..",
    # "deprecated": False,
    # }

    meta = None  # information about object special for third-party-addons.
