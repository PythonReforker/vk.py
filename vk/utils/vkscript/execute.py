import ast
import functools
import inspect
import types
import typing

from vk.utils.vkscript.converter import Scope
from vk.utils.vkscript.converter import VKScriptConverter

if typing.TYPE_CHECKING:
    from vk import VK


# import once
@functools.lru_cache()
def _get_vk() -> typing.Type["VK"]:
    from vk import VK

    return VK


def execute(func: types.FunctionType):
    e = Execute()
    return e.decorate(func)


class Execute:
    _code = None
    _preprocessor = None
    _func = None

    def decorate(self, func):
        source = inspect.getsource(func)
        self._func = func
        self._code = ast.parse(source).body[0]
        return self

    def preprocessor(self, func):
        self._preprocessor = func

    def build(self, *args, **kwargs) -> str:
        if self._code.__class__ == ast.FunctionDef:
            globals_ = dict(self._func.__globals__)
            for i, argument in enumerate(self._code.args.args):
                if argument.arg in kwargs:
                    globals_[argument.arg] = kwargs[argument.arg]
                elif i < len(args):
                    globals_[argument.arg] = args[i]
                elif argument.arg.upper() == "API":
                    continue
                else:
                    raise TypeError(
                        f"missing required argument {argument.arg}"
                    )
            converter = VKScriptConverter(Scope(globals=globals_))
            return converter.convert_block(self._code.body)
        raise NotImplementedError()

    async def __call__(self, *args, **kwargs):
        if self._preprocessor is not None:
            return await self._preprocessor(*args, **kwargs)
        return await self.execute(*args, **kwargs)

    async def execute(self, *args, **kwargs):
        vk = _get_vk().get_current()
        code = self.build(*args, **kwargs)
        response = await vk.execute_api_request(code)
        return response

    e = execute
