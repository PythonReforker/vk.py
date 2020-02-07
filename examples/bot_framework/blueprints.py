import logging

from vk import types
from vk import VK
from vk.bot_framework import Dispatcher, get_group_id
from vk.bot_framework.dispatcher import Blueprint
from vk.types import BotEvent
from vk.utils import TaskManager

logging.basicConfig(level="DEBUG")

bot_token = "token"
vk = VK(bot_token)
task_manager = TaskManager(vk.loop)

dp = Dispatcher(vk)

bp = Blueprint()

other_bp = Blueprint(commands=["tested"])


@bp.message_handler(text="hello")
async def handler(message: types.Message, data: dict):
    await message.answer("hello my friend!")


@other_bp.message_handler()
async def handler_yes(message: types.Message, data: dict):
    await message.answer("Yes.")


@bp.event_handler(BotEvent.WALL_POST_NEW)
async def handler_reply_new(event, data: dict):
    print(event)


async def run():
    dp.setup_blueprint(bp)
    dp.setup_blueprint(other_bp)
    dp.run_polling(await get_group_id(vk))


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=False)
