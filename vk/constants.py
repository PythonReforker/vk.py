"""
A file which contains all project constants.
"""
from vk.utils.json import AbstractJsonLibrary
from vk.utils.json import JsonLibrary

API_VERSION: str = "5.103"  # current api version https://vk.com/dev/versions
API_LINK: str = "https://api.vk.com/method/"  # link to access API

try:
    import orjson  # noqa
except ImportError:
    orjson = None

try:
    import ujson  # noqa
except ImportError:
    ujson = None

if not (ujson or orjson):
    import json
else:
    json = None

_JSONLIB: AbstractJsonLibrary = [lib for lib in [orjson, ujson, json] if lib][
    0
]  # noqa
JSON_LIBRARY = JsonLibrary(_JSONLIB)


def default_rules() -> dict:
    """
    Build and return dict of default handlers rules.
    :return:
    """
    from vk.bot_framework.rules.rules import (
        Commands,
        Text,
        Payload,
        ChatAction,
        DataCheck,
        MessageCountArgs,
        MessageArgsValidate,
        InPersonalMessages,
        InChat,
        FromBot,
        WithReplyMessage,
        WithFwdMessages,
        CountFwdMessages,
        Regex,
    )

    _default_rules: dict = {
        "commands": Commands,
        "text": Text,
        "payload": Payload,
        "chat_action": ChatAction,
        "data_check": DataCheck,
        "count_args": MessageCountArgs,
        "have_args": MessageArgsValidate,
        "in_chat": InChat,
        "in_pm": InPersonalMessages,
        "from_bot": FromBot,
        "with_reply_message": WithReplyMessage,
        "with_fwd_messages": WithFwdMessages,
        "count_fwd_messages": CountFwdMessages,
        "regex": Regex,
    }
    return _default_rules


def default_extensions() -> dict:
    """
    Build and return dict of default dispatcher extensions
    :return:
    """
    from vk.bot_framework.extensions import Polling

    _default_extensions: dict = {"polling": Polling}

    return _default_extensions
