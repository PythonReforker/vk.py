![vk.py](https://user-images.githubusercontent.com/28061158/63603699-cd51b980-c5d2-11e9-8a8f-06e1eef20afe.jpg)



# Welcome to vk.py 👋

![Version](https://img.shields.io/badge/version-0.6.0-blue.svg?cacheSeconds=2592000) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ](https://github.com/prostomarkeloff/vk.py/blob/master/LICENSE) [![Twitter: prostomarkeloff](https://img.shields.io/twitter/follow/prostomarkeloff.svg?style=social)](https://twitter.com/prostomarkeloff)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cac2f27aab0a41f993660a525c054bb5)](https://app.codacy.com/app/prostomarkeloff/vk.py?utm_source=github.com&utm_medium=referral&utm_content=prostomarkeloff/vk.py&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.org/prostomarkeloff/vk.py.svg?branch=master)](https://travis-ci.org/prostomarkeloff/vk.py)

> Fastest, scalable, fully asynchronous.



### 🏠 [Homepage](github.com/prostomarkeloff/vk.py)


## WARNING
This version of library won't be compatible with newer (1.0.0), if you wonna start new project, please use `dev` branch for it.

## Install

```sh
pip install https://github.com/prostomarkeloff/vk.py/archive/master.zip --upgrade
```

In requirements.txt:
```sh
# some stuff
https://github.com/prostomarkeloff/vk.py/archive/master.zip
```

Fast version with uvloop and ujson (only for *nix like OS):
```sh
pip https://github.com/prostomarkeloff/vk.py/archive/master.zip#egg=vk.py[fast]
```

With **ultra** handlers:
```sh
pip https://github.com/prostomarkeloff/vk.py/archive/master.zip#egg=vk.py[ultra]
```
More about it: [click](https://github.com/prostomarkeloff/uvkpy)

## Usage

A simple example
```python
from vk import VK
from vk.utils.task_manager import TaskManager
import logging

logging.basicConfig(level="INFO")
vk = VK(access_token=<TOKEN>)

async def status_get():
    resp = await vk.api_request("status.get")
    print(resp)

if __name__ == "__main__":
    task_manager = TaskManager(vk.loop)
    task_manager.add_task(status_get)
    task_manager.run()

```

You can find more examples [here](./examples)

Example of use bot framework, with docker integration [click](https://github.com/prostomarkeloff/vkpy-exam-bot)

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

## Alternatives

- Kutana. Bot engine for creating Telegram and VK bots
- VKBottle. Bot framework for VK bot development.
- VK_API. A simple library for accessing VK API.

And many other libraries...

## Author

👤 **prostomarkeloff**

* Twitter: [@prostomarkeloff](https://twitter.com/prostomarkeloff)
* Github: [@prostomarkeloff](https://github.com/prostomarkeloff)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/prostomarkeloff/vk.py/issues).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2019 [prostomarkeloff](https://github.com/prostomarkeloff).<br />
This project is [MIT](https://github.com/prostomarkeloff/vk.py/blob/master/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
