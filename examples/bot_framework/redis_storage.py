import logging

from vk import types
from vk import VK
from vk.bot_framework import Dispatcher, get_group_id
from vk.bot_framework import Storage
from vk.bot_framework.storages import RedisStorage
from vk.utils import TaskManager

logging.basicConfig(level="INFO")

bot_token = "123"
vk = VK(bot_token)
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk)
redis_storage: RedisStorage = RedisStorage("redis://localhost", vk.loop)  # create redis
storage = Storage()  # create base storage for place any

dp.storage = storage


@dp.message_handler(text="hello")
async def handle_event(message: types.Message, data: dict):
    redis: RedisStorage = await dp.storage.get(
        "redis"
    )  # you have access to redis storage
    c = await redis.get("really_needed_counter", 0)  # equal API
    await message.answer(f"Hello! {c}")
    await redis.update("really_needed_counter", int(c) + 1)


async def run():
    dp.storage.place("redis", redis_storage)  # best practice
    dp.run_polling(await get_group_id(vk))


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
