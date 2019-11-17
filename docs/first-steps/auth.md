## Авторизация

На данный момент библиотека поддерживает 2 метода авторизации: с помощью токена и с помощью логина и пароля.

### С помощью токена

```python
from vk import VK

my_awesome_token = "<Some token..>"
vk = VK(my_awesome_token)
```

### С помощью логина и пароля

```python
from vk import VK
from vk.utils.auth_manager import AuthManager

# Синхронно:
auth = AuthManager("7999123456", "my-password")
token = auth.get_token()
vk = VK(token)

# Асинхронно:
async def get_token_of_user(user_login: str, user_password: str):
    auth = AuthManager(user_login, user_password)
    return await auth.get_token_async()
```
