import aiohttp

from vk import VK
from vk.exceptions import APIErrorDispatcher


class TestVK:
    def test_vk_values(self, vk, vk_token):
        assert vk.loop is not None
        assert vk.access_token is vk_token
        assert isinstance(vk.client, aiohttp.ClientSession)
        assert isinstance(vk.error_dispatcher, APIErrorDispatcher)
        assert vk.client.closed is False
        assert VK.get_current() is not None
        assert VK.get_current() is vk
