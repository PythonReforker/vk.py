import aiohttp
import pytest

from vk import VK
from vk.exceptions import APIErrorDispatcher


@pytest.fixture
async def session(event_loop):
    return aiohttp.ClientSession(loop=event_loop)


@pytest.fixture
def vk(event_loop, session):
    return VK(None, loop=event_loop, client=session)  # noqa


class TestVK:
    def test_vk_values(self, vk):
        assert vk.loop is not None
        assert vk.access_token is None
        assert isinstance(vk.client, aiohttp.ClientSession)
        assert isinstance(vk.error_dispatcher, APIErrorDispatcher)
        assert vk.client.closed is False
        assert VK.get_current() is not None
        assert VK.get_current() is vk
