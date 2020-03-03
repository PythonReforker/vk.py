from pydantic import BaseModel
import typing

class ErrorInfo(BaseModel):
    from vk import VK
    vk: VK
    method_name: str
    request_params: dict
    raw_error: dict

    def repeat_request(self, vk: VK = None, additional={}) -> typing.Coroutine:
        self.request_params.update(additional)
        return vk.api_request(self.method_name, self.request_params)
    
    def repeat_request_with_current(self, additional={}) -> typing.Coroutine:
        return self.repeat_request(self.vk, additional)
    
    class Config:
        arbitrary_types_allowed = True

class APIException(Exception):
    def __init__(self, code: int, text: str):
        self.code = code
        self.text = text
        self.message = f"[{self.code}] {self.text}"
        super().__init__(self.message)

 

class KeyboardException(Exception):
    pass
