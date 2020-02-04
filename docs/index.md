![vk.py](https://user-images.githubusercontent.com/28061158/63603699-cd51b980-c5d2-11e9-8a8f-06e1eef20afe.jpg)



# WARNING:
> Dev branch was merged to master but 1.0.0 hasn't still been completed. Check `dev` branch.

# Welcome to vk.py 👋

![Version](https://img.shields.io/badge/version-0.6.0-blue.svg?cacheSeconds=2592000) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ](https://github.com/kesha1225/vk.py/blob/master/LICENSE)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cac2f27aab0a41f993660a525c054bb5)](https://app.codacy.com/app/kesha1225/vk.py?utm_source=github.com&utm_medium=referral&utm_content=prostomarkeloff/vk.py&utm_campaign=Badge_Grade_Dashboard)

> Extremely-fast, easy-to-use, ready for production. The asyncio based library for Python and Humans written to be efficient and reliable.



### 🏠 [Homepage](github.com/kesha1225/vk.py)


## Install

```sh
pip install https://github.com/kesha1225/vk.py/archive/master.zip --upgrade
```

Warning: this version really unstable and not recommended to use in production.


## Usage

Simple example with AuthManager

```python
import asyncio
import logging

from vk import VK
from vk.utils.auth_manager import AuthManager

logging.basicConfig(level="INFO")


async def main():
    session = AuthManager(login="login", password="password")
    await session.authorize()
    token = session.access_token
    vk = VK(access_token=token).get_api()
    print(await vk.status.get())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```


A simple example with token
```python
import logging

from vk import VK
from vk.utils.task_manager import TaskManager

logging.basicConfig(level="INFO")
vk = VK(access_token="token")


async def status_get():
    api = vk.get_api()
    resp = await api.status.get()
    print(resp)

if __name__ == "__main__":
    task_manager = TaskManager(vk.loop)
    task_manager.add_task(status_get)
    task_manager.run()

```

You can find more examples [here](./examples).



## Features

- Rich high-level API.
- Fully asynchronous. Based on asyncio and aiohttp.
- Bot framework out of-the-box.
- Fully typed, thanks to Pydantic.
- Compatible with PyPy.
- Have a lot of tools (in bot framework) out-of-the-box for creating largest and powerful applications [click](./vk/bot_framework/addons):
    * Caching
    * Blueprints
    * Cooldowns
    * FSM (WIP)
- Python -> VKScript converter (WIP). [try it](./vk/utils/vkscript)

## Alternatives

- Kutana. Bot engine for creating Telegram and VK bots
- VK_API. A simple library for accessing VK API.

And many other libraries...


## FAQ

This is only bot library? - No, this library could be used for acessing userapi or botapi without any troubles.

Where i can find the docs? - [Check it](https://kesha1225.github.io/vk.py).

How to use it? - You may check docs or see our [examples](./examples).

Why do you do it? - We are interesting to create the most used and easy-to-use library for Python.

When `1.0.0` will be released? - We don't know. We hope that it's moment will come to us ASAP. However, you can see current issues and help us.

## Author

👤 **prostomarkeloff**

* Github: [@prostomarkeloff](https://github.com/prostomarkeloff)


## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/prostomarkeloff/vk.py/issues).
Also you can check your [contributors guide](./CONTRIBUTING.md).

[Our contributors](./CONTRIBUTORS.txt).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2019 [prostomarkeloff](https://github.com/prostomarkeloff).<br />
This project is [MIT](https://github.com/kesha1225/vk.py/blob/master/LICENSE) licensed.

