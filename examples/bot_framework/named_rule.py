from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher, get_group_id
from vk.bot_framework.dispatcher.rule import NamedRule

from vk import types

import logging

logging.basicConfig(level="INFO")

bot_token = "123"
vk = VK(bot_token)
VK.set_current(vk)
task_manager = TaskManager(vk.loop)
api = vk.get_api()

dp = Dispatcher(vk)


class Commands(NamedRule):
    key = "commands"

    """
    Own implementaion of commands rule.
    """

    def __init__(self, commands):
        self.commands = commands
        self.prefix = "!"

    async def check(self, message: types.Message, data: dict):
        text = message.text.lower()
        _accepted = False
        for command in self.commands:
            if text == f"{self.prefix}{command}":
                _accepted = True

        return _accepted


dp.setup_rule(Commands)  # bind


@dp.message_handler(commands=["t"])  # use
async def handle(message: types.Message, data: dict):
    await message.answer("hello!")


async def run():
    dp.run_polling(await get_group_id(vk))


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=True)
