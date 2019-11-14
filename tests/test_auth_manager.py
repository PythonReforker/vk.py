from vk.utils.auth_manager import AppID
from vk.utils.auth_manager import AppSecret
from vk.utils.auth_manager import AuthManager


def test_auth_manager(vk_login, vk_password):
    manager = AuthManager("fake-login", "fake-password")
    assert manager.password == "fake-password"
    assert manager.login == "fake-login"
    assert manager.client_secret == AppSecret.ANDROID.value
    assert manager.app_id == AppID.ANDORID.value

    another_manager = AuthManager("fake-login", "fake-password", 123, "123456")
    assert another_manager.password == "fake-password"
    assert another_manager.login == "fake-login"
    assert another_manager.app_id == 123
    assert another_manager.client_secret == "123456"

    if vk_login and vk_password:
        truthy_manager = AuthManager(vk_login, vk_password)
        token = truthy_manager.get_token()
        assert token
