# Первые шаги

В данной части документации будут описаны базовые методы работы с библиотекой (а также некоторые характерные особенности, о которых желательно знать при работе с vk.py).

!!! note
    Данная версия документации актуальна только для версии 1.0.0.

## Объект VK

```python
# project/main.py

from vk import VK

vk = VK("my-super-token")
```

Во-первых, `VK` это так называемый `объект с контекстом`. Это значит что однажды проинициализровав его, мы сможем получить его где угодно.
Большинство методов в библиотеке используют эту особенность, поэтому не приходится лишний раз передавать объект `VK`.

```python
# project/sub.py
from vk import VK

vk = VK.get_current()  # ВАЖНО: для того чтобы получить объект из контекста, код который
# инициализирует объект должен быть исполнен раньше, чем тот, который пытается его получить.
```

Лучше всего использовать это в таком виде:

```python
# project/sub2.py
from vk import VK

class ClassWhichWorksWithAPI:
    def __init__(self, vk: VK = None):
        self.vk = vk or VK.get_current()
        if self.vk is None:
            raise RuntimeError("Please, configure `VK` object for working with this class.")
```

!!! note
    Большинство объект в библиотеке являются объектами контекста (например все типы из `vk/types`!)


### Запросы к API

Исполнять запросы к API можно двумя (на самом деле 3-мя) способами. Рассмотрим оба.

Первый, и наверно самый простой метод:

```python
from vk import VK

vk = VK("my-super-token")

async def print_status():
    result: dict = await vk.api_request("status.get")
    print(result)
    # >>> {'text': 'hello there!'} or your status...

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_status())
```

В данном случае мы получаем простой ответ в виде словаря.

Есть другой, вероятно, более удобный, но пока он не доступен для работы со всеми методами.

```python
from vk import VK

vk = VK("my-super-token")
my_id = 123
api = vk.get_api()

async def print_result_of_message_send(peer_id: int):
    result = await api.messages.send(peer_id=peer_id, message="Hello!", random_id=0)
    print(result)
    # >>> response=1 (or not 1)

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_result_of_message_send(my_id))
```

В чём преимущество данного подхода? Вам возвращаются готовые объекты, с которыми Ваш редактор будет работать намного лучше, чем с "сырыми" словарями.
Помимо всего прочего, все доступные методы полностью типизированы, Вы будете знать все доступные параметры.

Ну и давайте я всё-таки расскажу Вам о 3-ем методе:

```python
from vk import VK

vk = VK("my-super-token")

async def print_status():
    result = await vk.execute_api_request("return API.status.get();")
    print(result)
    # >>> {'text': 'i wanna die...'}

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_status())
```

### Работа с ошибками

Эту тему я считаю довольно важной, ибо часто при работе с API VK мы сталкиваемся с ошибками, и их нам нужно как-то обрабатывать.
Здесь я постараюсь показать Вам почему такая обработка ошибок проще и лучше чем обычные `try-except` по всему коду.

Например, наш бот должен исключать участников из чата, но иногда бывает что наш бот не может этого делать, ну не дали права администратора и всё.
Что мы можем сделать чтобы наш бот не упал с ошибкой, а пользователь не расстроился ничего не получив? Конечно же "обернуть" вызов метода в `try-except`!
!!! note
    Даже если при вызове метода "выпадет" ошибка, наш бот все равно продолжит работу.

```python
from vk.exceptions import APIException
# some code...

try:
    await api.messages.remove_chat_user(...)
except APIException:
    await message.answer("Oops, something went wrong...")
```

Хорошо, это довольно приемлимый код, скажу больше - так и надо делать. Но в `vk.py` мы можем упростить даже эту задачу.

```python
from vk import VK
from vk import types

vk = VK("my-super-token")

@vk.error_dispatcher.error_handler(15)  # if I'm not mistaken..
async def error_handler(error: dict):
    message = types.Message.get_current()  # context object!
    await message.answer("Oops, something went wrong...")
    raise RuntimeError("Can't remove user in chat")  # so that we won't return control to handler (and won't get any undefined behaviour)

async def handler_in_bot(...):
    await api.messages.remove_chat_user(...)  # if error will occur, our handler handle it.
```

### Помимо всего прочего

Также, мы можем создавать объект `VK` "на лету" (ну, или не совсем).
Это может помочь если например нам нужно авторизоваться с помощью неизвестного токена, полученого из какого-либо источника:

```python
from vk import VK

async def main():
    async with VK.with_token("some-token") as vk:  # VK context object won't be changed!
        result = await vk.api_request("status.get")
        print(result)
```