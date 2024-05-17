from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RevaSetCommentRequest(_message.Message):
    __slots__ = ("symbol_or_address", "comment")
    SYMBOL_OR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    symbol_or_address: str
    comment: str
    def __init__(self, symbol_or_address: _Optional[str] = ..., comment: _Optional[str] = ...) -> None: ...

class RevaSetCommentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
