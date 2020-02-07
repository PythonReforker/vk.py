import asyncio
import logging
import typing
from pydantic import BaseModel

from vk import VK
from vk.constants import API_VERSION
from vk.constants import JSON_LIBRARY
from vk.utils import mixins

from functools import reduce
from datetime import datetime
from enum import IntEnum, IntFlag
logger = logging.getLogger(__name__)


# https://vk.com/dev/using_longpoll

CHAT_START_ID = 2E9  # id с которого начинаются беседы


class VkLongpollMode(IntFlag):
    """ Дополнительные опции ответа

    `Подробнее в документации VK API
    <https://vk.com/dev/using_longpoll?f=1.+Подключение>`_
    """

    #: Получать вложения
    GET_ATTACHMENTS = 2

    #: Возвращать расширенный набор событий
    GET_EXTENDED = 2**3

    #: возвращать pts для метода `messages.getLongPollHistory`
    GET_PTS = 2**5

    #: В событии с кодом 8 (друг стал онлайн) возвращать
    #: дополнительные данные в поле `extra`
    GET_EXTRA_ONLINE = 2**6

    #: Возвращать поле `random_id`
    GET_RANDOM_ID = 2**7


DEFAULT_MODE = sum(VkLongpollMode)


class VkEventType(IntEnum):
    """ Перечисление событий, получаемых от longpoll-сервера.

    `Подробнее в документации VK API
    <https://vk.com/dev/using_longpoll?f=3.+Структура+событий>`__
    """

    #: Замена флагов сообщения (FLAGS:=$flags)
    MESSAGE_FLAGS_REPLACE = 1

    #: Установка флагов сообщения (FLAGS|=$mask)
    MESSAGE_FLAGS_SET = 2

    #: Сброс флагов сообщения (FLAGS&=~$mask)
    MESSAGE_FLAGS_RESET = 3

    #: Добавление нового сообщения.
    MESSAGE_NEW = 4

    #: Редактирование сообщения.
    MESSAGE_EDIT = 5

    #: Прочтение всех входящих сообщений в $peer_id,
    #: пришедших до сообщения с $local_id.
    READ_ALL_INCOMING_MESSAGES = 6

    #: Прочтение всех исходящих сообщений в $peer_id,
    #: пришедших до сообщения с $local_id.
    READ_ALL_OUTGOING_MESSAGES = 7

    #: Друг $user_id стал онлайн. $extra не равен 0, если в mode был передан флаг 64.
    #: В младшем байте числа extra лежит идентификатор платформы
    #: (см. :class:`VkPlatform`).
    #: $timestamp — время последнего действия пользователя $user_id на сайте.
    USER_ONLINE = 8

    #: Друг $user_id стал оффлайн ($flags равен 0, если пользователь покинул сайт и 1,
    #: если оффлайн по таймауту). $timestamp — время последнего действия пользователя
    #: $user_id на сайте.
    USER_OFFLINE = 9

    #: Сброс флагов диалога $peer_id.
    #: Соответствует операции (PEER_FLAGS &= ~$flags).
    #: Только для диалогов сообществ.
    PEER_FLAGS_RESET = 10

    #: Замена флагов диалога $peer_id.
    #: Соответствует операции (PEER_FLAGS:= $flags).
    #: Только для диалогов сообществ.
    PEER_FLAGS_REPLACE = 11

    #: Установка флагов диалога $peer_id.
    #: Соответствует операции (PEER_FLAGS|= $flags).
    #: Только для диалогов сообществ.
    PEER_FLAGS_SET = 12

    #: Удаление всех сообщений в диалоге $peer_id с идентификаторами вплоть до $local_id.
    PEER_DELETE_ALL = 13

    #: Восстановление недавно удаленных сообщений в диалоге $peer_id с
    #: идентификаторами вплоть до $local_id.
    PEER_RESTORE_ALL = 14

    #: Один из параметров (состав, тема) беседы $chat_id были изменены.
    #: $self — 1 или 0 (вызваны ли изменения самим пользователем).
    CHAT_EDIT = 51

    #: Изменение информации чата $peer_id с типом $type_id
    #: $info — дополнительная информация об изменениях
    CHAT_UPDATE = 52

    #: Пользователь $user_id набирает текст в диалоге.
    #: Событие приходит раз в ~5 секунд при наборе текста. $flags = 1.
    USER_TYPING = 61

    #: Пользователь $user_id набирает текст в беседе $chat_id.
    USER_TYPING_IN_CHAT = 62

    #: Пользователь $user_id записывает голосовое сообщение в диалоге/беседе $peer_id
    USER_RECORDING_VOICE = 64

    #: Пользователь $user_id совершил звонок с идентификатором $call_id.
    USER_CALL = 70

    #: Счетчик в левом меню стал равен $count.
    MESSAGES_COUNTER_UPDATE = 80

    #: Изменились настройки оповещений.
    #: $peer_id — идентификатор чата/собеседника,
    #: $sound — 1/0, включены/выключены звуковые оповещения,
    #: $disabled_until — выключение оповещений на необходимый срок.
    NOTIFICATION_SETTINGS_UPDATE = 114


class VkPlatform(IntEnum):
    """ Идентификаторы платформ """

    #: Неопознанный объект
    UNKNOWN = 0

    #: Мобильная версия сайта или неопознанное мобильное приложение
    MOBILE = 1

    #: Официальное приложение для iPhone
    IPHONE = 2

    #: Официальное приложение для iPad
    IPAD = 3

    #: Официальное приложение для Android
    ANDROID = 4

    #: Официальное приложение для Windows Phone
    WPHONE = 5

    #: Официальное приложение для Windows 8
    WINDOWS = 6

    #: Полная версия сайта или неопознанное приложение
    WEB = 7


class VkOfflineType(IntEnum):
    """ Выход из сети в событии :attr:`VkEventType.USER_OFFLINE` """

    #: Пользователь покинул сайт
    EXIT = 0

    #: Оффлайн по таймауту
    AWAY = 1


class VkMessageFlag(IntFlag):
    """ Флаги сообщений """

    #: Сообщение не прочитано.
    UNREAD = 1

    #: Исходящее сообщение.
    OUTBOX = 2

    #: На сообщение был создан ответ.
    REPLIED = 2**2

    #: Помеченное сообщение.
    IMPORTANT = 2**3

    #: Сообщение отправлено через чат.
    CHAT = 2**4

    #: Сообщение отправлено другом.
    #: Не применяется для сообщений из групповых бесед.
    FRIENDS = 2**5

    #: Сообщение помечено как "Спам".
    SPAM = 2**6

    #: Сообщение удалено (в корзине).
    DELETED = 2**7

    #: Сообщение проверено пользователем на спам.
    FIXED = 2**8

    #: Сообщение содержит медиаконтент
    MEDIA = 2 ** 9

    #: Сообщение в беседу через клиенты
    CHAT_FROM_CLIENT = 2 ** 13

    #: Отмена пометки как спам
    CANCEL_SPAM = 2 ** 15

    #: Приветственное сообщение от сообщества.
    HIDDEN = 2**16

    #: Сообщение удалено для всех получателей.
    DELETED_ALL = 2 ** 17

    #: Входящее сообщение не доставлено.
    NOT_DELIVERED = 2 ** 18

    #: Входящее сообщение в беседе
    IN_CHAT = 2 ** 19

    #: Неизвестный флаг
    NONAME_FLAG = 2 ** 20

    #: Ответ на сообщение
    REPLY_MSG = 2 ** 21


class VkPeerFlag(IntFlag):
    """ Флаги диалогов """

    #: Важный диалог
    IMPORTANT = 1

    #: Неотвеченный диалог
    UNANSWERED = 2


class VkChatSettings(IntFlag):
    """Пункты настроек в чате"""
    #: Могут приглашать только администраторы, иначе все участники
    INVITE_PERMISSION = 1

    #: Могут изменять закрепленное сообщение только администратор, иначе все участники
    PIN_PERMISSION = 4

    #: Могут редактировать заголовок только администратор, иначе все участники
    EDIT_TITLE_PERMISSION = 8

    #: Могут добавлять администраторов только администрация, иначе только создатель
    ADD_ADMIN_PERMISSION = 16


class VkChatEventType(IntEnum):
    """ Идентификатор типа изменения в чате """

    #: Изменилось название беседы
    TITLE = 1

    #: Сменилась обложка беседы
    PHOTO = 2

    #: Назначен новый администратор
    ADMIN_ADDED = 3

    #: Изменены настройки беседы
    SETTINGS_CHANGED = 4

    #: Закреплено сообщение
    MESSAGE_PINNED = 5

    #: Пользователь присоединился к беседе
    USER_JOINED = 6

    #: Пользователь покинул беседу
    USER_LEFT = 7

    #: Пользователя исключили из беседы
    USER_KICKED = 8

    #: С пользователя сняты права администратора
    ADMIN_REMOVED = 9

    #: Бот прислал клавиатуру
    KEYBOARD_RECEIVED = 11


MESSAGE_EXTRA_FIELDS = [
    'peer_id', 'timestamp', 'title', 'text', 'attachments', 'random_id'
]
MSGID = 'message_id'

EVENT_ATTRS_MAPPING = {
    VkEventType.MESSAGE_FLAGS_REPLACE: [MSGID, 'flags'] + MESSAGE_EXTRA_FIELDS,
    VkEventType.MESSAGE_FLAGS_SET: [MSGID, 'mask'] + MESSAGE_EXTRA_FIELDS,
    VkEventType.MESSAGE_FLAGS_RESET: [MSGID, 'mask'] + MESSAGE_EXTRA_FIELDS,
    VkEventType.MESSAGE_NEW: [MSGID, 'flags'] + MESSAGE_EXTRA_FIELDS,
    VkEventType.MESSAGE_EDIT: [MSGID, 'mask'] + MESSAGE_EXTRA_FIELDS,

    VkEventType.READ_ALL_INCOMING_MESSAGES: ['peer_id', 'local_id'],
    VkEventType.READ_ALL_OUTGOING_MESSAGES: ['peer_id', 'local_id'],

    VkEventType.USER_ONLINE: ['user_id', 'extra', 'timestamp', "app_id"],
    VkEventType.USER_OFFLINE: ['user_id', 'flags', 'timestamp', 'app_id'],

    VkEventType.PEER_FLAGS_RESET: ['peer_id', 'mask'],
    VkEventType.PEER_FLAGS_REPLACE: ['peer_id', 'flags'],
    VkEventType.PEER_FLAGS_SET: ['peer_id', 'mask'],

    VkEventType.PEER_DELETE_ALL: ['peer_id', 'local_id'],
    VkEventType.PEER_RESTORE_ALL: ['peer_id', 'local_id'],

    VkEventType.CHAT_EDIT: ['chat_id', 'self'],
    VkEventType.CHAT_UPDATE: ['type_id', 'peer_id', 'info'],

    VkEventType.USER_TYPING: ['user_id', 'flags'],
    VkEventType.USER_TYPING_IN_CHAT: ['user_id', 'chat_id'],
    VkEventType.USER_RECORDING_VOICE: ['peer_id', 'user_id', 'flags', 'timestamp'],

    VkEventType.USER_CALL: ['user_id', 'call_id'],

    VkEventType.MESSAGES_COUNTER_UPDATE: ['count'],
    VkEventType.NOTIFICATION_SETTINGS_UPDATE: ['sound', 'disabled_until']
}


def map_list_to_dict(lst: list, map_rule: typing.List[str]) -> dict:
    map_rule = map_rule[:len(lst)]
    return reduce(lambda acc, x: {**acc, x: lst.pop(0)}, map_rule, dict())


class Event(BaseModel):
    event_type: VkEventType
    user_id: int = None
    count: int = None
    peer_id: int = None
    timestamp: int = None
    offline_status: VkOfflineType = None
    messageflags: VkMessageFlag = None
    peerflags: VkPeerFlag = None
    chat_event_type: VkChatEventType = None
    chat_settings: VkChatSettings = None
    platform: VkPlatform = None
    text: str = None
    title: str = None
    attachments: dict = None
    random_id: int = None
    message_id: int = None
    sound: int = None
    disabled_until: int = None
    local_id: int = None
    chat_id: int = None
    app_id: int = None

    @classmethod
    def parse_list(cls, raw_list: list):
        event_type = VkEventType(raw_list.pop(0))
        map_rule = EVENT_ATTRS_MAPPING[event_type]
        obj = map_list_to_dict(raw_list, map_rule)
        if event_type in [VkEventType.USER_ONLINE, VkEventType.USER_OFFLINE]:
            obj['user_id'] *= -1
        if event_type == VkEventType.NOTIFICATION_SETTINGS_UPDATE:
            obj = obj.pop('sound')
        if "flags" in obj:
            flags = obj.pop("flags")
            if event_type == VkEventType.USER_OFFLINE:
                obj["offline_status"] = VkOfflineType(flags)
            elif event_type == VkEventType.PEER_FLAGS_REPLACE:
                obj["peerflags"] = VkPeerFlag(flags)
            else:
                obj["messageflags"] = VkMessageFlag(flags)
        if "mask" in obj:
            mask = obj.pop("mask")
            obj["messageflags"] = VkMessageFlag(mask)
        if "extra" in obj:
            obj["platform"] = VkPlatform(obj.pop("extra"))
        if "type_id" in obj:
            type_id = VkChatEventType(obj.pop("type_id"))
            info = obj.pop("info")
            obj["chat_event_type"] = type_id
            if type_id == VkChatEventType.ADMIN_ADDED:
                obj["admin_id"] = info
            elif type_id == VkChatEventType.SETTINGS_CHANGED:
                obj["chat_settings"] = VkChatSettings(info)
            elif type_id == VkChatEventType.MESSAGE_PINNED:
                obj["pinned_message_id"] = info
            elif type_id in [VkChatEventType.USER_JOINED,
                             VkChatEventType.USER_KICKED,
                             VkChatEventType.USER_LEFT,
                             VkChatEventType.ADMIN_REMOVED]:
                obj["user_id"] = info
        return cls(event_type=event_type, **obj)


class UserLongPoll(mixins.ContextInstanceMixin):
    def __init__(self, vk: VK):
        """

        :param vk:
        """
        self._vk: VK = vk
        self.server: typing.Optional[str] = None
        self.key: typing.Optional[str] = None
        self.ts: typing.Optional[str] = None

        self.ran = False

    @property
    def vk(self) -> VK:
        return self._vk

    async def _prepare_longpoll(self):
        await self._update_polling()

    async def _update_polling(self):
        """
        :return:
        """
        resp = await self.get_server()
        self.server = resp["server"]
        self.key = resp["key"]
        self.ts = resp["ts"]

        logger.debug(
            f"Update polling credentials. Server - {self.server}. Key - {self.key}. TS - {self.ts}"
        )

    async def get_server(self) -> dict:
        """
        Get polling server.
        :return:
        """
        resp = await self.vk.api_request(
            "messages.getLongPollServer"
        )
        return resp

    async def get_updates(self, key: str, server: str, ts: str) -> dict:
        """
        Get updates from VK.
        :param key:
        :param server:
        :param ts:
        :return:
        """
        async with self.vk.client.post(
            f"https://{server}?act=a_check&key={key}&ts={ts}&wait=20&mode={sum(VkLongpollMode)}"
        ) as response:
            resp = await response.json(loads=JSON_LIBRARY.loads)
            logger.debug(f"Response from polling: {resp}")
            return resp

    async def listen(self) -> typing.List[dict]:
        """

        :return: list of updates coming from VK
        """
        try:
            updates: typing.Optional[dict] = await self.get_updates(
                key=self.key, server=self.server, ts=self.ts
            )

            # Handle errors from vkontakte
            if updates.get("failed"):
                logger.debug(
                    f"Longpolling responded with failed: {updates['failed']}"
                )

                if updates["failed"] == 1:
                    self.ts: str = updates["ts"]
                elif updates["failed"] in (2, 3):
                    await self._update_polling()

                return []

            if "ts" not in updates or "updates" not in updates:
                raise Exception("Vkontakte responded with incorrect response")

            self.ts: str = updates["ts"]

            logger.debug(f"Got updates through polling: {updates['updates']}")

            return updates["updates"]

        except Exception:  # noqa
            logger.exception(
                "Received exception while polling... Sleeping 10 seconds..."
            )

            await asyncio.sleep(10)
            await self._update_polling()

            return []

    async def run(self) -> typing.AsyncGenerator[None, Event]:
        """

        :return: last update coming from VK
        """

        await self._prepare_longpoll()
        self.ran = True
        logger.info("Polling started!")

        while True:
            events = await self.listen()
            while events:
                event = events.pop()
                yield Event.parse_list(event)
