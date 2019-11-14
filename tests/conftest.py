import os

import pytest

from vk import VK


@pytest.fixture(scope="session")
def vk_token():
    return os.environ.get("VK_TOKEN")


@pytest.fixture(scope="session")
def vk_login():
    return os.environ.get("VK_LOGIN")


@pytest.fixture(scope="session")
def vk_password():
    return os.environ.get("VK_PASSWORD")


@pytest.fixture(scope="session")
def vk(vk_token):
    return VK(vk_token)  # noqa
