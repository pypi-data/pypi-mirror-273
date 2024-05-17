from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RevaHandshakeRequest(_message.Message):
    __slots__ = ("inferenceHostname", "inferencePort")
    INFERENCEHOSTNAME_FIELD_NUMBER: _ClassVar[int]
    INFERENCEPORT_FIELD_NUMBER: _ClassVar[int]
    inferenceHostname: str
    inferencePort: int
    def __init__(self, inferenceHostname: _Optional[str] = ..., inferencePort: _Optional[int] = ...) -> None: ...

class RevaHandshakeResponse(_message.Message):
    __slots__ = ("extensionHostname", "extensionPort")
    EXTENSIONHOSTNAME_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONPORT_FIELD_NUMBER: _ClassVar[int]
    extensionHostname: str
    extensionPort: int
    def __init__(self, extensionHostname: _Optional[str] = ..., extensionPort: _Optional[int] = ...) -> None: ...
