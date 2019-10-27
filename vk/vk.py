"""
A part of library which represent a main object of VK API.
"""
import asyncio
import logging
import typing
from asyncio import AbstractEventLoop

try:
    from contextlib import asynccontextmanager
except ImportError:
    from async_generator import asynccontextmanager

from aiohttp import ClientSession

from vk.constants import API_LINK
from vk.constants import API_VERSION
from vk.constants import JSON_LIBRARY
from vk.exceptions import APIErrorDispatcher
from vk.methods import API
from vk.utils import ContextInstanceMixin

logger = logging.getLogger(__name__)

try:
    import uvloop  # noqa

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    uvloop = None


class VK(ContextInstanceMixin):
    """
    The main object of VKAPI, have basically methods to access in API.
    """

    def __init__(
        self,
        access_token: str,
        *,
        loop: AbstractEventLoop = None,
        client: ClientSession = None,
    ):

        """

        :param str access_token: access token of VK user/community for access to VK methods.
        :param AbstractEventLoop loop: asyncio event loop, uses in Task manager/dispatcher extensions/etc.
        :param ClientSession client: aiohttp client session
        """
        self.access_token: str = access_token
        self.loop: asyncio.AbstractEventLoop = loop if loop is not None else asyncio.get_event_loop()
        self.client: ClientSession = (
            client
            if client is not None and isinstance(client, ClientSession)
            else ClientSession(json_serialize=JSON_LIBRARY.dumps)
        )

        self.error_dispatcher: APIErrorDispatcher = APIErrorDispatcher(self)

        self.__api_object: API = self.__get_api()
        VK.set_current(self)

    async def _api_request(
        self,
        method_name: typing.AnyStr,
        params: dict = None,
        _raw_mode: bool = False,
        ignore_errors: bool = False,
    ) -> dict:
        """

        :param str method_name: method of name when need to call
        :param dict params: parameters with method
        :param bool _raw_mode: signal of return 'raw' response, or not (basically, returns response["response"])
        :param ignore_errors: signal of errors ignore
        :return:
        """
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        elif params is None or not isinstance(params, dict):
            params = {}

        params.update({"v": API_VERSION, "access_token": self.access_token})
        logger.debug(f"Params to send: {params}")
        async with self.client.post(API_LINK + method_name, data=params) as response:
            json: typing.Dict[str, typing.Any] = await response.json(
                loads=JSON_LIBRARY.loads
            )
            logger.debug(f"Method {method_name} called. Response from API: {json}")
            if "error" in json:
                return await self.error_dispatcher.error_handle(json, ignore_errors)

            if _raw_mode:
                return json

            return json["response"]

    async def api_request(
        self, method_name: str, params: dict = None, ignore_errors: bool = False
    ) -> dict:
        """
        Send api request to VK server
        :param method_name: method to execute
        :param params: parameters of method
        :param ignore_errors: signal of errors ignore
        :return:
        """
        return await self._api_request(
            method_name=method_name, params=params, ignore_errors=ignore_errors
        )

    async def execute_api_request(self, code: str) -> dict:
        """
        https://vk.com/dev/execute

        :param code: code for execute. Example: return API.status.get();
        :return:
        """
        return await self.api_request("execute", params={"code": code})

    def __get_api(self) -> API:
        """
        Get API class
        :return:
        """
        api = API(self)
        API.set_current(api)
        return api

    def get_api(self) -> API:
        """
        Get API class
        :return:
        """
        return self.__api_object

    @classmethod
    @asynccontextmanager
    async def with_token(cls, access_token: str):
        vk = cls(access_token=access_token)
        yield vk
        await vk.close()

    async def close(self) -> None:
        """
        Close aiohttp client session.
        :return:
        """
        if not self.client.closed:
            await self.client.close()

    def __del__(self):
        self.loop.create_task(self.close())
        self.loop.close()
