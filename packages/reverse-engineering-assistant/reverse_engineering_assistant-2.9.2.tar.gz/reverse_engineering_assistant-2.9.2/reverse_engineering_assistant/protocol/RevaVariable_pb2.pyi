from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RevaVariable(_message.Message):
    __slots__ = ("name", "storage", "data_type", "size")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    name: str
    storage: str
    data_type: str
    size: int
    def __init__(self, name: _Optional[str] = ..., storage: _Optional[str] = ..., data_type: _Optional[str] = ..., size: _Optional[int] = ...) -> None: ...
