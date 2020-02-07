import logging

from vk import BackgroundTask
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


@dp.message_handler(text="hello")
async def handle_event(message: types.Message, data: dict):
    async with BackgroundTask(very_slow_operation, 5) as task:
        await task()
    await message.reply("Hello!")


def very_slow_operation(a: int):
    import time

    time.sleep(10)
    print(a + 10)


async def run():
    dp.run_polling(await get_group_id(vk))


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
