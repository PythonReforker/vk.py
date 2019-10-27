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
                data = await middleware.pre_process_event(event, data)
            except SkipHandler:
                logger.debug(
                    f"Middleware {middleware.__class__.__name__} skip handler!"
                )
                _skip_handler = True
                break  # skip other middlewares when middleware skip handler

        return _skip_handler, data

    async def trigger_post_process_middlewares(self):
        for middleware in self.middlewares:
            await middleware.post_process_event()


class AbstractMiddleware(ABC, MetaMixin):
    @abstractmethod
    async def pre_process_event(self, event, data: dict) -> dict:
        """
        Called before checking filters and execute handler
        :param event:
        :param data:
        :return: data
        """
        pass

    @abstractmethod
    async def post_process_event(self) -> None:
        """
        Called after handler
        :return:
        """
        pass


class BaseMiddleware(AbstractMiddleware, ABC):
    def __init__(self):
        self._manager = None
        self._configured = False

    def is_configured(self) -> bool:
        return self._configured
