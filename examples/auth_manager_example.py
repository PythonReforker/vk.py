import asyncio

from vk import VK
from vk.utils.auth_manager import AuthManager


async def enter_captcha(url: str, sid: str) -> str:
    return input(f"Enter captcha from url {url} : ")


async def enter_confirmation_code() -> str:
    return input(f"Enter confirmation code: ")


async def main():
    session = AuthManager(login="login", password="password")
    session.enter_captcha = enter_captcha
    session.enter_confirmation_code = enter_confirmation_code
    await session.authorize()
    token = session.access_token
    vk = VK(access_token=token).get_api()
    print(await vk.status.get())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
