from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher, get_group_id
from vk import types

import logging

logging.basicConfig(level="INFO")

bot_token = "123"
vk = VK(bot_token)
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk)


@dp.message_handler(text="hello")
async def handle(message: types.Message, data: dict):
    await message.reply("hello!")


@dp.message_handler(chat_action=types.message.Action.chat_invite_user)
async def new_user(message: types.Message, data: dict):
    await message.reply("Hello, my friend!")


async def run():
    dp.run_polling(await get_group_id(vk))


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
