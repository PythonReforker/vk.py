from .middleware import MiddlewareManager
from vk.utils import ContextInstanceMixin
from vk import VK
from vk import types

from vk.types.events.community.events_list import Event
from vk.utils.get_event import get_event_object

from .handler import Handler
from vk.longpoll import BotLongPoll

from ..callbackapi import callback_api

from ..rules.rules import Commands, Text

import typing
import logging

logger = logging.getLogger(__name__)


class Dispatcher(ContextInstanceMixin):
    def __init__(self, vk: VK, group_id: int):
        self.vk: VK = vk
        self.group_id: int = group_id
        self._hanlders: typing.List[Handler] = []
        self._middleware_manager: MiddlewareManager = MiddlewareManager(self)

        self._longpoll = BotLongPoll(self.group_id, self.vk)

    def _register_handler(self, handler: Handler):
        self._hanlders.append(handler)
        logger.debug(f"Handler '{handler.handler.__name__}' successfully added!")

    def register_message_handler(self, coro: typing.Callable, rules: typing.List):
        event_type = Event.MESSAGE_NEW
        handler = Handler(event_type, coro, rules)
        self._register_handler(handler)

    def message_handler(
            self, *rules, commands: typing.List[str] = None, text: str = None
    ):
        def decorator(coro: typing.Callable):
            primitive_rules: typing.List = []
            if commands:
                primitive_rules.append(Commands(commands))
            if text:
                primitive_rules.append(Text(text))
            self.register_message_handler(coro, list(rules) + primitive_rules)
            return coro

        return decorator

    def register_event_handler(
            self, coro: typing.Callable, event_type: Event, rules: typing.List
    ):
        handler = Handler(event_type, coro, rules=rules)
        self._register_handler(handler)

    def event_handler(self, event_type: Event, *rules):
        def decorator(coro: typing.Callable):
            self.register_event_handler(coro, event_type, list(rules))
            return coro

        return decorator

    def setup_middleware(self, middleware):
        self._middleware_manager.setup(middleware)
        logger.info(f"Middleware '{middleware.__class__.__name__}' successfully added!")

    async def _process_event(self, event: dict):
        _skip_handler = await self._middleware_manager.trigger_pre_process_middlewares(
            event
        )
        if not _skip_handler:
            ev = await get_event_object(event)
            for handler in self._hanlders:
                if handler.event_type.value == ev.type:
                    try:
                        await handler.execute_handler(ev.object)
                        break
                    except Exception as e:
                        logger.exception(
                            f"Error in handler ({handler.handler.__name__}):"
                        )

        await self._middleware_manager.trigger_post_process_middlewares()

    async def _process_events(self, events: typing.List[dict]):
        for event in events:
            self.vk.loop.create_task(self._process_event(event))

    async def run_polling(self):
        """
        Run polling.
        :return:
        """
        VK.set_current(self.vk)
        await self._longpoll._prepare_longpoll()
        while True:
            events = await self._longpoll.listen()
            if events:
                await self._process_events(events)

    def run_callback_api(self, host: str, port: int, confirmation_code: str, path: str):
        """

        :param host: Host string. Example: "0.0.0.0"
        :param port: port
        :param confirmation_code: callback api confirmation code
        :param path: url where VK send requests. Example: "my_bot"
        :return:
        """
        app = callback_api.get_app(self, confirmation_code)
        callback_api.run_app(app, host, port, path)
        logger.info("Callback API handler runned!")