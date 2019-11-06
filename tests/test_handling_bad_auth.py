from vk import VK


def add_error_handler(vk):
    vk.error_dispatcher.register_error_handler(5, error_handler)
    return None


async def error_handler(error):
    print(error)


async def test_auth():
    vk = VK("bad_token")
    add_error_handler(vk)
    await vk.api_request("status.get")
