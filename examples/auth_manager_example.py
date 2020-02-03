import asyncio

from vk import VK
from vk.utils.auth_manager import AuthManager


async def main():
    session = AuthManager(login="login", password="password")
    await session.authorize()
    token = session.access_token
    vk = VK(access_token=token).get_api()
    print(await vk.status.get())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
