from vk import VK
from vk.exceptions import APIException
from vk.types import Message
from vk.types import User
from vk.types.community import Community
from vk.utils import ContextInstanceMixin


class Validator(ContextInstanceMixin):
    def __init__(self, vk: VK = None):
        self._vk = vk if vk else VK.get_current()
        self._api = vk.get_api()
        self.validators_answers: dict = {
            "valid_vk_id": "",
            "positive_number": "",
            "valid_vk_group_id": "",
        }

    @property
    def vk(self):
        return self._vk

    @property
    def api(self):
        return self._api

    async def valid_vk_group_id(self, arg: str, message: Message):
        """
        Validate passed in message group_id or screenname.
        Just like 'valid_vk_id', but with group_id or screenname.

        If all good - append to data received response from VKAPI in field 'valid_vk_group_id_group'.
        :param arg:
        :param message:
        :return:
        """
        have_answer = self.validators_answers["valid_vk_group_id"]
        try:
            result = await self.vk.api_request(
                "groups.getById", {"group_id": arg}
            )
        except APIException:
            if have_answer:
                await message.answer(have_answer)
            return False
        if not result and have_answer:
            await message.answer(have_answer)
        if result:
            return {"valid_vk_group_id_group": Community(**result[0])}
        return result

    async def valid_vk_id(self, arg: str, message: Message):
        """
        Validate passed in message ID or screenname.
        This validator just search user in VK which have this ID or screenname.

        If all good - append to data received response from VKAPI in field 'valid_vk_id_user'.
        Example:

        @dp.message_handler(commands=["hello"], have_args=[validators.valid_vk_id])
        async def handle(message: types.Message, data: dict):
            usr: types.User = data["valid_vk_id_user"]
            await message.answer(usr.first_name)
        :param message:
        :param arg:
        :return:
        """

        have_answer = self.validators_answers["valid_vk_id"]
        try:
            result = await self.vk.api_request("users.get", {"user_ids": arg})
        except APIException:
            if have_answer:
                await message.answer(have_answer)
            return False
        if not result and have_answer:
            await message.answer(have_answer)
        if result:
            return {"valid_vk_id_user": User(**result[0])}
        return result

    async def positive_number(self, arg: str, message: Message):
        """
        Validate passed in message digit.
        If digit is positive - returns true.
        :param message:
        :param arg:
        :return:
        """
        have_answer = self.validators_answers["positive_number"]
        if not arg.isdigit():
            if have_answer:
                await message.answer(have_answer)
            return False
        if int(arg) <= 0:
            if have_answer:
                await message.answer(have_answer)
            return False
        return True
