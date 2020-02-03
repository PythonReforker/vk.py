import logging

from vk import types
from vk import VK
from vk.bot_framework import Dispatcher, get_group_id
from vk.utils import TaskManager

logging.basicConfig(level="INFO")

bot_token = "123"
vk = VK(bot_token)
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk)


async def arg_checker(arg: str, message: types.Message):
    # some asynchronous operation...
    # all async-validators accept message arg. example usecase:
    # user introduce bad password, you can answer user about his error
    # await message.answer("Bad password!")
    return True


@dp.message_handler(
    commands=["buy"], have_args=[lambda arg: arg.isdigit(), lambda arg: arg > 10]
)
async def handler(message: types.Message, data: dict):
    """
    Validate args. You may add to list lambda`s, or sync func`s with 1 arg (arg) and returned bool-like value.
    Or you can add to list async-validators (example usecase: you have 1 arg which signal of user id,
    you want check this user_id, but your database support only asynchronous calls... You can add asynchronous validators! -
    check example down).
    """
    await message.answer("Ok.")


@dp.message_handler(commands=["send"], have_args=[arg_checker])
async def async_arg_checker(message: types.Message, data: dict):
    await message.answer("Sending...")


@dp.message_handler(commands=["add"], count_args=2)
async def pretty_handler(message: types.Message, data: dict):
    """
    Not validate args. Only check len args (without command, =))
    """

    await message.answer("OK...")


async def run():
    dp.run_polling(await get_group_id(vk))


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
