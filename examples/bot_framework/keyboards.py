import logging

from vk import types
from vk import VK
from vk.bot_framework import Dispatcher
from vk.keyboards import ButtonColor
from vk.keyboards import Keyboard
from vk.utils import TaskManager

logging.basicConfig(level="INFO")

bot_token = "123"
vk = VK(bot_token)
gid = 123
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)

keyboard = Keyboard(one_time=False)
keyboard.add_text_button("Hello, my friend!", payload={"hello": "world"})
keyboard.add_text_button("Another text", color=ButtonColor.SECONDARY)


@dp.message_handler(payload={"hello": "world"})
async def handle_event(message: types.Message, data: dict):
    await message.reply("Hello :)")


@dp.message_handler(text="get")
async def get_keyboard(message: types.Message, data: dict):
    await message.answer(":)", keyboard=keyboard.get_keyboard())


@dp.message_handler(text="off")
async def off_keyboard(message: types.Message, data: dict):
    await message.answer("Ok.", keyboard=keyboard.get_empty_keyboard())


async def run():
    dp.run_polling()


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
