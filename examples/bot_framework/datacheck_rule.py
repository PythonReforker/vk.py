from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher, rules
from vk.bot_framework import BaseMiddleware, SkipHandler
from vk import types

import logging

logging.basicConfig(level="INFO")

bot_token = "token"
vk = VK(bot_token)
gid = 123
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk, gid)


class MyMiddleware(BaseMiddleware):
    async def pre_process_event(self, event, data: dict):
        print("Called before handlers!")
        if event["type"] != "message_new":
            raise SkipHandler
        data["my_message"] = "hello, handler!"
        return data

    async def post_process_event(self):
        print("Called after handlers!")


@dp.message_handler(text="hello!", data_check={"my_message": "hello, handler!"})
async def handle(message: types.Message, data: dict):
    print(data["my_message"])  # hello, handler!
    await message.reply("Hello!")


async def run():
    dp.run_polling()


if __name__ == "__main__":
    dp.setup_middleware(MyMiddleware())  # setup middleware
    task_manager.add_task(run)
    task_manager.run()
