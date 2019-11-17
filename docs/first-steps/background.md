## Задачи "за кадром".
В этом разделе документации я постараюсь рассказать Вам, почему так называемые `Background Task` или "задачи в фоне" могут помочь Вам при написании приложений.

### Для чего это нужно?
В первую очередь, они нужны для того чтобы сделать какую-то работу чуть позже, чем сейчас.
Например у нас есть бот в группе, который принимает картинки от пользователей, что-то делает с ними, а после отправляет какой-то ответ.
Очевидно, что "какая-то работа с картинкой", это либо её сохранение, либо модификация, либо анализ.
Пример того, как должен работать этот бот:

```
- Пользователь: подать заявку <фотография>
- Бот: Заявка принята! Ожидайте ответа после проверки фотографии!

            Спустя некоторое время...

- Бот: Мы проанализировали Вашу фотографию и узнали: <что-то>...
```

Как мы можем сделать это? Для работы с изображениями в Python, обычно используется библиотека PIL, а она, как мы знаем синхронная.
Пример функции обработки фотографии:

```python
def analyze_photo(photo):
    # do some operations that will block thread of execution.
    ...

```

И вызовем её в обработчике команды!

```python
@dp.message_handler(text="подать заявку")
async def handle_it(message: types.Message, data: dict):
    attachment = get_photo(message)
    if not attachment:
        return await message.answer("Вы не прислали фотографию!")
    await message.answer("Заявка принята! Ожидайте ответа после проверки фотографии!")
    some_info = analyze_photo(attachment)
    await message.answer("Мы проанализировали Вашу фотографию и узнали: <что-то>...")
```

Вроде как выглядит нормально, вполне себе обычная функция. Но есть одна проблема, на вызове `analyze_photo` наш бот будет только анализировать фотографию, а не отвечать другим пользователям - это проблема.
Но в `vk.py` мы имеем простой инструмент для решения этой проблемы!

```python
from vk import BackgroundTask
import asyncio

photos_info = {}

def analyze_photo(id, photo):
    # do some with photo
    ...
    info = ...(photo)
    photos_info[id] = info

@dp.message_handler(text="подать заявку")
async def handle_it(message: types.Message, data: dict):
    attachment = get_photo(message)
    if not attachment:
        return await message.answer("Вы не прислали фотографию!")
    await message.answer("Заявка принята! Ожидайте ответа после проверки фотографии!")

    async with BackgroundTask(analyze_photo, id=message.from_id, photo=attachment) as task:
        await task()

async def send_messages_with_info():
    while True:
        for k, v in photos_info.items():
            await vk.get_api().messages.send(peer_id=k, message=v, random_id=0)
            await asyncio.sleep(0.5)

if __name__ == '__main__':
    ...
    task_manager.add_task(send_messages_with_info)
```
Что делает данный код? Он делает тоже самое, что и тот код, конечно, в более длинной форме, но это помогло нам обрабатывать последующие сообщения от пользователей.
Как он это делает? Он запускает функции обработки фотографий в отдельном потоке, после помещает их в словарь, а другая корутина собирает их, и отправляет сообщения.