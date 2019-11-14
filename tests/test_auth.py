import pytest

from vk import VK


@pytest.mark.asyncio
async def bad_auth(bad_token: str):
    vk = VK(bad_token)
    await vk.api_request("status.get", {})
    return vk


@pytest.mark.asyncio
async def test_auth():
    with pytest.xfail():
        await bad_auth("bad_token")
