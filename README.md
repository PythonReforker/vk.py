![vk.py](https://user-images.githubusercontent.com/28061158/63603699-cd51b980-c5d2-11e9-8a8f-06e1eef20afe.jpg)



# Welcome to vk.py 👋

![Version](https://img.shields.io/badge/version-0.6.0-blue.svg?cacheSeconds=2592000) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ](https://github.com/prostomarkeloff/vk.py/blob/master/LICENSE) [![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fprostomarkeloff%2Fvk.py.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fprostomarkeloff%2Fvk.py?ref=badge_shield)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cac2f27aab0a41f993660a525c054bb5)](https://app.codacy.com/app/prostomarkeloff/vk.py?utm_source=github.com&utm_medium=referral&utm_content=prostomarkeloff/vk.py&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.org/prostomarkeloff/vk.py.svg?branch=master)](https://travis-ci.org/prostomarkeloff/vk.py)

> Extremely-fast, easy-to-use, ready for production. The asyncio based library for Python and Humans written to be efficient and reliable.



### 🏠 [Homepage](github.com/prostomarkeloff/vk.py)


## Install

Install package from PyPi: (current version is 4 alpha of 1.0.0)

```sh
pip install vk.py==1.0.0a4 -U
```

Warning: this version really unstable and not recommended to use in production.


## Usage

A simple example
```python
from vk import VK
from vk.utils.task_manager import TaskManager
from vk.utils.auth_manager import AuthManager
import logging

logging.basicConfig(level="INFO")
auth = AuthManager("7999123456", "my-password")
vk = VK(access_token=auth.get_token())

async def status_get():
    resp = await vk.api_request("status.get")
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

Where i can find the docs? - [Check it](https://prostomarkeloff.github.io/vk.py).

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
This project is [MIT](https://github.com/prostomarkeloff/vk.py/blob/master/LICENSE) licensed.

