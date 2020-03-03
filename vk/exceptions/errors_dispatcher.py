import asyncio
import logging
import typing

from vk.exceptions.errors import APIException, ErrorInfo

logger = logging.getLogger(__name__)

class APIErrorHandler:
    def __init__(self, error_code: int, handler: typing.Callable):
        self.handler: typing.Callable = handler
        self.error_code: int = error_code

    async def execute(self, error: ErrorInfo):
        """
        Execute error handler
        :param error:
        :return:
        """
        try:
            return await self.handler(error)
        except Exception:  # noqa
            logging.exception("Exception occured in error handler...: ")


class APIErrorDispatcher:
    from vk import VK
    DELAY = 0.34

    def __init__(self, vk: VK):
        """

        :param vk:
        """
        self.vk: self.VK = vk
        self._handlers: typing.List[APIErrorHandler] = []

        self._handlers.append(
            APIErrorHandler(6, self._to_many_requests_handler)
        )  # standard to many request handler

    async def _to_many_requests_handler(
            self, error: ErrorInfo
    ) -> typing.Dict:
        logger.debug("To many requests error handle..")
        await asyncio.sleep(self.DELAY)
        return await error.repeat_request_with_current()

    def error_handler(self, error_code: int):
        def decorator(coro: typing.Callable):
            self.register_error_handler(error_code, coro)

        return decorator

    def register_error_handler(self, error_code, coro):
        handler = APIErrorHandler(error_code, coro)
        self._handlers.append(handler)

    async def error_handle(
            self, json: typing.Dict,
            ignore_errors: bool = False,
            method_name: str = "",
            request_params: dict = {}
    ) -> typing.Union[typing.Dict, typing.NoReturn]:
        logger.debug("Some error from API handle..")
        error: dict = json["error"]
        logger.debug(f"Error data: {error}")

        code: int = error["error_code"]
        error_info: ErrorInfo = ErrorInfo(raw_error=error,
        method_name=method_name,
        request_params=request_params,
        vk=self.vk)
        if not ignore_errors:
            for handler in self._handlers:
                if handler.error_code == code:
                    return await handler.execute(error_info)

        msg: str = error["error_msg"]
        raise APIException(code, msg)
