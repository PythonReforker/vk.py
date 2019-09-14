"""
A simple abstraction for build largest bots and sharing rules beetwen handlers.

Example usecase:

    You have a simple bot with admin and user commands[handlers],
    what to limit access to admin commands[handlers] you create a simple rule[named rule, rule] for passing him
    in message_handler decorator. If you have a really big count of commands, you need write this:

    .. code-block:: python3
        @dp.message_handler(is_admin=True)
        async def some(msg, data):
            ...

    repeatedly. We appreciate your time and we create blueprints for this simple cases.

    But! If you have a largest bot with a lof of handlers, you need a simple, and more powerful
    tool for register handlers.
    Blueprints registering looks like that:

    .. code-block:: python3
        blueprint = Blueprint(...)
        dp.setup_blueprint(blueprint)

    It`s easy!

"""
import typing
from abc import ABC
from abc import abstractmethod
from collections import namedtuple

from vk.bot_framework.dispatcher.rule import BaseRule
from vk.types import BotEvent as Event

HandlerInBlueprint = namedtuple(
    "HandlerInBlueprint", "coro event_type rules named_rules"
)


class AbstractBlueprint(ABC):
    @abstractmethod
    def message_handler(
        self,
        *rules: typing.Tuple[typing.Type[BaseRule]],
        **named_rules: typing.Dict[str, typing.Any]
    ):
        """
        Register a message handler in blueprint.
        :param rules:
        :param named_rules:
        :return:
        """

    @abstractmethod
    def event_handler(
        self,
        event_type: Event,
        *rules: typing.Tuple[typing.Type[BaseRule]],
        **named_rules: typing.Dict[str, typing.Any]
    ):
        """
        Register a event handler in blueprint.
        :param event_type:
        :param rules:
        :param named_rules:
        :return:
        """


class Blueprint(AbstractBlueprint):
    def __init__(
        self,
        *rules: typing.Tuple[typing.Type[BaseRule]],
        **named_rules: typing.Dict[str, typing.Any]
    ):
        self.default_rules = rules
        self.default_named_rules = named_rules

        self.handlers: typing.List[HandlerInBlueprint] = []

    def message_handler(
        self,
        *rules: typing.Tuple[typing.Type[BaseRule]],
        **named_rules: typing.Dict[str, typing.Any]
    ):
        def decorator(coro: typing.Callable):
            nonlocal rules, named_rules

            rules = list(rules)
            rules.extend(self.default_rules)
            named_rules.update(self.default_named_rules)

            self.handlers.append(
                HandlerInBlueprint(coro, Event.MESSAGE_NEW, rules, named_rules)
            )

        return decorator

    def event_handler(
        self,
        event_type: Event,
        *rules: typing.Tuple[typing.Type[BaseRule]],
        **named_rules: typing.Dict[str, typing.Any]
    ):
        def decorator(coro: typing.Callable):
            nonlocal rules, named_rules

            rules = list(rules)
            rules.extend(self.default_rules)
            named_rules.update(self.default_named_rules)

            self.handlers.append(
                HandlerInBlueprint(coro, event_type, rules, named_rules)
            )

        return decorator
