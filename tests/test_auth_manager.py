from vk.utils.auth_manager import AuthManager


def test_auth_manager():
    manager = AuthManager("fake-login", "fake-password")
    assert manager.password == "fake-password"
    assert manager.login == "fake-login"

    another_manager = AuthManager("fake-login", "fake-password", 123, "123456")
    assert another_manager.password == "fake-password"
    assert another_manager.login == "fake-login"
    assert another_manager.app_id == 123
    assert another_manager.scope == "123456"
