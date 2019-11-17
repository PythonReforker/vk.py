import typing
from enum import auto
from enum import Enum

import urllib3
from aiohttp import ClientSession

from vk.constants import API_VERSION
from vk.constants import JSON_LIBRARY
from vk.constants import JSONDecodeError
from vk.utils.mixins import ContextInstanceMixin


class ResponseErrorAction(Enum):
    NEED_VALIDATION = auto()


class ResponseValidation(typing.NamedTuple):
    status: bool
    action: ResponseErrorAction = None


class AppID(Enum):
    ANDORID = 2274003


class AppSecret(Enum):
    ANDROID = "hHbZxrka2uZ6jB1inYsH"


USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
)
AUTH_URL = "https://oauth.vk.com/token"


class AuthManager(ContextInstanceMixin):
    def __init__(
        self,
        login: str,
        password: str,
        app_id: typing.Union[int, AppID] = AppID.ANDORID,
        client_secret: typing.Union[str, AppSecret] = AppSecret.ANDROID,
    ):
        self._client = urllib3.PoolManager(headers={"User-Agent": USER_AGENT})
        self._async_client = ClientSession(headers={"User-Agent": USER_AGENT})
        if isinstance(app_id, AppID):
            app_id = app_id.value
        if isinstance(client_secret, AppSecret):
            client_secret = client_secret.value
        self.app_id = app_id
        self.client_secret = client_secret
        self.login = login
        self.password = password

    def get_token(self):
        return self._auth()

    async def get_token_async(self):
        return await self._auth_async()

    def _auth(self) -> str:
        fields = {
            "grant_type": "client_credentials",
            "client_id": self.app_id,
            "client_secret": self.client_secret,
            "username": self.login,
            "password": self.password,
            "2fa_supported": 1,
            "v": API_VERSION,
        }
        json = self._make_request(fields)
        validate_info = self._validate_response(json)
        if validate_info.status:
            return json["access_token"]
        else:
            if validate_info.action is ResponseErrorAction.NEED_VALIDATION:
                while True:
                    result = self._process_need_validation(json)
                    if "access_token" not in result:
                        continue
                    return result["access_token"]

    async def _auth_async(self) -> str:
        fields = {
            "grant_type": "client_credentials",
            "client_id": self.app_id,
            "client_secret": self.client_secret,
            "username": self.login,
            "password": self.password,
            "2fa_supported": 1,
            "v": API_VERSION,
        }
        json = await self._make_request_async(fields)
        validate_info = self._validate_response(json)
        if validate_info.status:
            return json["access_token"]
        else:
            if validate_info.action is ResponseErrorAction.NEED_VALIDATION:
                while True:
                    result = await self._process_need_validation_async(json)
                    if "access_token" not in result:
                        continue
                    return result["access_token"]

    def _process_need_validation(self, json: dict):
        """
        :param json:
        :return:
        """
        self._make_request({}, url=json["redirect_uri"])
        code = self.error_need_validation()
        fields = {
            "grant_type": "client_credentials",
            "client_id": self.app_id,
            "client_secret": self.client_secret,
            "username": self.login,
            "password": self.password,
            "2fa_supported": 1,
            "v": API_VERSION,
            "code": code,
        }
        json = self._make_request(fields)
        return json

    async def _process_need_validation_async(self, json: dict):
        await self._make_request_async({}, url=json["redirect_uri"])
        code = self.error_need_validation()
        fields = {
            "grant_type": "client_credentials",
            "client_id": self.app_id,
            "client_secret": self.client_secret,
            "username": self.login,
            "password": self.password,
            "2fa_supported": 1,
            "v": API_VERSION,
            "code": code,
        }
        json = await self._make_request_async(fields)
        return json

    def _validate_response(self, response: dict):
        """
        Validate response
        :param response:
        :return:
        """
        if "error" in response:
            if response["error"] == "need_validation":
                return ResponseValidation(
                    False, ResponseErrorAction.NEED_VALIDATION
                )
            else:
                raise NotImplementedError()
        else:
            return ResponseValidation(True)

    def error_need_validation(self) -> int:  # noqa
        """
        Override this if needed.
        :return:
        """
        code = input("Enter the code which you will receive: ")
        return int(code.strip())

    async def _make_request_async(
        self, fields: dict, method: str = "GET", url: str = AUTH_URL
    ):
        async with self._async_client.request(
            method=method, url=url, params=fields
        ) as resp:
            try:
                json = await resp.json()
            except JSONDecodeError:
                json = {}
        return json

    async def close_async(self):
        await self._async_client.close()

    def _make_request(
        self, fields: dict, method: str = "GET", url: str = AUTH_URL
    ) -> dict:
        """
        Make request to API.
        :param fields:
        :param method:
        :param url:
        :return:
        """
        response: urllib3.HTTPResponse = self._client.request(
            method, url, fields
        )
        try:
            json = JSON_LIBRARY.loads(response.data.decode("utf-8"))
        # TODO: add universal exception for json validation error.
        except JSONDecodeError:
            json = {}
        return json
