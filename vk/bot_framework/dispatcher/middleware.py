import logging
import typing
from abc import ABC
from abc import abstractmethod

from .handler import SkipHandler
from vk.utils.mixins import MetaMixin

logger = logging.getLogger(__name__)


class MiddlewareManager:
    def __init__(self, dispatcher):
        self.dp = dispatcher
        self.middlewares: typing.List[BaseMiddleware] = []

    def setup(self, middleware):
        if not isinstance(middleware, BaseMiddleware):
            raise RuntimeError("Middleware must be only instance of 'BaseMiddleware")

        if middleware.is_configured():
            raise RuntimeError("Middleware already configured!")

        if middleware.meta and middleware.meta.get("deprecated", False):
            logger.warning(
                f"This middleware (({middleware.__class__.__name__})) deprecated. Not recommended to use."
            )

        self.middlewares.append(middleware)
        logger.info(f"Middleware '{middleware.__class__.__name__}' successfully added!")

    async def trigger_pre_process_middlewares(self, event, data: dict):
        _skip_handler = False
        for middleware in self.middlewares:
            try:
                has = getattr(middleware, "pre_process_event", None)
                if has is None:
                    continue
                data = await middleware.pre_process_event(event, data)
            except SkipHandler:
                logger.debug(
                    f"Middleware {middleware.__class__.__name__} skip handler!"
                )
                _skip_handler = True
                break  # skip other middlewares when middleware skip handler

        return _skip_handler, data

    async def trigger_post_process_middlewares(self, result: typing.Any):
        """

        :param result: result of handler work
        :return:
        """
        for middleware in self.middlewares:
            has = getattr(middleware, "post_process_event", None)
            if has is None:
                continue
            try:
                await middleware.post_process_event(result)
            except SkipHandler:
                logger.debug(
                    f"Middleware {middleware.__class__.__name__} skip handler!"
                )
                break  # skip other middlewares when middleware skip handler


class AbstractMiddleware(ABC, MetaMixin):
    possible_hooks = ["pre_process_event", "post_process_event"]

    # you should override hooks.

    async def pre_process_event(self, event, data: dict) -> dict:
        """
        Called before checking filters and execute handler
        :param event:
        :param data:
        :return: data
        """
        pass

    async def post_process_event(self, result: typing.Any) -> None:
        """
        Called after handler
        :return:
        """
        pass


class BaseMiddleware(AbstractMiddleware, ABC):
    def __init__(self):
        self._configured: bool = False

    def is_configured(self) -> bool:
        return self._configured
