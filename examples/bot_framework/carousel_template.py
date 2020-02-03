from vk import VK
from vk.keyboards import Keyboard, Template
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


@dp.message_handler(text="show")
async def template_handler(message: types.Message, data: dict):
    keyboard = Keyboard(one_time=False)

    keyboard.add_text_button("Hello world!")
    keyboard.add_link_button(text="Link to Google", link="https://google.com")

    template_1 = Template(
        title="First title",
        description="First description",
        buttons=keyboard.buttons[0],
        photo_id="-191459391_457239025",
    )

    keyboard = Keyboard(one_time=False)
    keyboard.add_text_button("World hello!")
    keyboard.add_text_button("Wow, another button")

    template_2 = Template(
        title="Second title",
        description="Second description",
        buttons=keyboard.buttons[0],
        photo_id="-191459391_457239026",
    )

    carousel = Template.generate_template(template_1, template_2)
    await message.answer("Look on this templates!", template=carousel)


async def run():
    dp.run_polling(await get_group_id(vk))


if __name__ == "__main__":
    task_manager.add_task(run)
    task_manager.run(auto_reload=False)
