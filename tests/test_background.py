import asyncio
import time

import pytest

from vk import BackgroundTask

async_task_passed = False
sync_task_passed = False
some_task_passed = False


async def asynchronous_task(number: int):
    global async_task_passed
    await asyncio.sleep(number)
    async_task_passed = True
    return f"I slept {number} seconds..."


def synchronous_task(number: int):
    global sync_task_passed
    time.sleep(number)
    sync_task_passed = True
    return f"I slept {number} seconds..."


def some_task_with_kwargs(number: int, *, message: str):
    global some_task_passed
    some_task_passed = True
    return f"Number: {number}. Message: {message}"


class TestBackground:
    @pytest.mark.asyncio
    async def test_background_task(self):
        async with BackgroundTask(asynchronous_task, 1) as task:
            await task()
        await asyncio.sleep(2)
        assert async_task_passed

        async with BackgroundTask(synchronous_task, 1) as task:
            await task()
        await asyncio.sleep(2)
        assert sync_task_passed

        async with BackgroundTask(
            some_task_with_kwargs, 1, message="Hello!"
        ) as task:
            await task()

        assert some_task_passed
