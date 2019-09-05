from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher
from vk import types

import logging

logging.basicConfig(level="INFO")

bot_token = "123"
vk = VK(bot_token)
gid = 123
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)


@dp.message_handler(text="hello")
async def handle(message: types.Message, data: dict):
    await message.reply("hello!")


@dp.message_handler(chat_action=types.message.Action.chat_invite_user)
async def new_user(message: types.Message, data: dict):
    await message.reply("Hello, my friend!")


async def run():
    dp.run_polling()


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
