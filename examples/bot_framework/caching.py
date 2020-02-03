import logging

from vk import types
from vk import VK
from vk.bot_framework import Dispatcher, get_group_id
from vk.bot_framework import Storage
from vk.bot_framework.addons.caching import cached_handler
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


@dp.message_handler(text="text")
@cached_handler(redis_storage, expire=20, for_specify_user=True)
async def test(msg: types.Message, data):
    resp = await redis_storage.get("hello", 0)
    await redis_storage.update("hello", int(resp) + 1)
    return await msg.cached_answer(f"{resp}")


async def run():
    dp.storage.place("redis", redis_storage)  # best practice
    dp.run_polling(await get_group_id(vk))


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
