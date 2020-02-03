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


@dp.message_handler(with_fwd_messages=True, count_fwd_messages=3)
async def handle(message: types.Message, data: dict):
    await message.reply("Test!")


@dp.message_handler(with_reply_message=True)
async def handle_event(message: types.Message, data: dict):
    await message.reply("Hello!")


async def run():
    dp.run_polling(await get_group_id(vk))


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
