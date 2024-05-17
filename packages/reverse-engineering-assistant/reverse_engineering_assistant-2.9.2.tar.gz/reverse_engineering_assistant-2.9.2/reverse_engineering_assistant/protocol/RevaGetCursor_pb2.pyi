from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RevaGetCursorRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RevaGetCursorResponse(_message.Message):
    __slots__ = ("cursor_address", "symbol", "function")
    CURSOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    cursor_address: int
    symbol: str
    function: str
    def __init__(self, cursor_address: _Optional[int] = ..., symbol: _Optional[str] = ..., function: _Optional[str] = ...) -> None: ...
