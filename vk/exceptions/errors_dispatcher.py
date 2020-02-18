import asyncio
import logging
import typing

from vk.exceptions.errors import APIException

logger = logging.getLogger(__name__)


class APIErrorHandler:
    def __init__(self, error_code: int, handler: typing.Callable):
        self.handler: typing.Callable = handler
        self.error_code: int = error_code

    async def execute(self, error: typing.Dict, request_params: typing.Dict):
        """
        Execute error handler
        :param request_params:
        :param error:
        :return:
        """
        try:
            return await self.handler(error, request_params)
        except Exception:  # noqa
            logging.exception("Exception occured in error handler...: ")


if typing.TYPE_CHECKING:
    from vk import VK


class APIErrorDispatcher:
    DELAY = 0.34

    def __init__(self, vk: "VK"):
        """

        :param vk:
        """
        self.vk: "VK" = vk
        self._handlers: typing.List[APIErrorHandler] = []

        self._handlers.append(
            APIErrorHandler(6, self._to_many_requests_handler)
        )  # standard to many request handler

    def _repeat_request(
            self, error: typing.Dict, additional: typing.Dict = None
    ) -> typing.Coroutine:
        additional = {} or additional
        method_name = None
        for param in error["request_params"]:
            key = param["key"]
            value = param["value"]
            if key == "method":
                method_name = value
                break
        return self.vk.api_request(
            method_name=method_name, params=additional
        )

    async def _to_many_requests_handler(
            self, error: typing.Dict
    ) -> typing.Dict:
        logger.debug("To many requests error handle..")
        await asyncio.sleep(self.DELAY)
        return await self._repeat_request(error)

    def error_handler(self, error_code: int):
        def decorator(coro: typing.Callable):
            self.register_error_handler(error_code, coro)

        return decorator

    def register_error_handler(self, error_code, coro):
        handler = APIErrorHandler(error_code, coro)
        self._handlers.append(handler)

    async def error_handle(
            self, json: typing.Dict, ignore_errors: bool = False, request_params: dict = None
    ) -> typing.Union[typing.Dict, typing.NoReturn]:
        logger.debug("Some error from API handle..")
        error: dict = json["error"]
        logger.debug(f"Error data: {error}")

        code: int = error["error_code"]
        if not ignore_errors:
            for handler in self._handlers:
                if handler.error_code == code:
                    return await handler.execute(error, request_params)

        msg: str = error["error_msg"]
        raise APIException(code, msg)
