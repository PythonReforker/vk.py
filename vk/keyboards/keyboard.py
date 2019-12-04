import logging
import typing
from enum import Enum

from ..exceptions import KeyboardException
from vk.constants import JSON_LIBRARY

logger = logging.getLogger(__name__)


# Keyboards: https://vk.com/dev/bots_docs_3


class ButtonColor(Enum):
    PRIMARY = "primary"  # blue
    SECONDARY = "secondary"  # white
    NEGATIVE = "negative"  # red
    POSITIVE = "positive"  # green


class ButtonType(Enum):
    TEXT = "text"
    LOCATION = "location"
    VKPAY = "vkpay"
    VKAPPS = "open_app"


class Keyboard:
    def __init__(self, one_time: bool, inline: bool = False):
        """
        Create a keyboard object
        :param one_time:
        """
        self.one_time = one_time
        self.buttons = [[]]
        self.keyboard = {
            "one_time": one_time,
            "buttons": self.buttons,
            "inline": inline,
        }

    @staticmethod
    def generate_payload(payload: dict) -> str:
        if payload is None:
            payload = ""
        return payload

    def add_row(self):
        """

        :return:
        """
        if len(self.buttons) >= 10:
            raise KeyboardException("Max 10 rows")

        self.buttons.append([])

    def _add_button(self, action: dict) -> None:
        """

        :param action:
        :return:
        """
        current_row = self.buttons[-1]
        current_row.append(action)

    def add_text_button(
        self,
        text: str,
        color: ButtonColor = ButtonColor.PRIMARY,
        payload: dict = None,
    ):
        """

        :param text:
        :param color:
        :param payload:
        :return:
        """
        payload = self.generate_payload(payload)

        if not isinstance(color, ButtonColor):
            logger.warning("Invalid button color. Used 'PRIMARY'")
            color = ButtonColor.PRIMARY.value
        else:
            color = color.value

        if isinstance(text, str):
            if len(text) < 1:
                raise KeyboardException("Invalid text")
        else:
            raise KeyboardException("Invalid text")

        action = {
            "action": {
                "type": ButtonType.TEXT.value,
                "payload": payload,
                "label": text,
            },
            "color": color,
        }

        self._add_button(action)

    def add_location_button(self, payload: dict = None):
        """

        :param payload:
        :return:
        """

        payload = self.generate_payload(payload)

        action = {
            "action": {"type": ButtonType.LOCATION.value, "payload": payload}
        }

        self._add_button(action)

    def add_vkpay_button(self, hash: str, payload: dict = None):  # noqa
        """
        :param hash:
        :param payload:
        :return:
        """

        payload = self.generate_payload(payload)

        action = {
            "action": {
                "type": ButtonType.VKPAY.value,
                "payload": payload,
                "hash": hash,
            }
        }

        self._add_button(action)

    def add_vkapps_button(
        self, app_id: int, owner_id: int, label: str, payload: dict = None
    ):
        """

        :param app_id:
        :param owner_id:
        :param payload:
        :return:
        """
        payload = self.generate_payload(payload)

        action = {
            "action": {
                "type": ButtonType.VKAPPS.value,
                "app_id": app_id,
                "owner_id": owner_id,
                "payload": payload,
                "label": label,
            }
        }

        self._add_button(action)

    def get_keyboard(self) -> typing.AnyStr:
        """
        Get keyboard json to send.
        If keyboard is 'static', you can generate json once and send it every time.
        :return:
        """
        return JSON_LIBRARY.dumps(self.keyboard)

    @classmethod
    def get_empty_keyboard(cls: "Keyboard") -> typing.AnyStr:
        """

        :return:
        """
        keyboard = cls(one_time=True)  # noqa
        keyboard.keyboard["buttons"] = []
        return keyboard.get_keyboard()
