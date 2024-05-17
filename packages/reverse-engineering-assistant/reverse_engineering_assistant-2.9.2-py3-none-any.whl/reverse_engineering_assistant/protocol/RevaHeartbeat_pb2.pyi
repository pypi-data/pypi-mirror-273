from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RevaHeartbeatRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RevaHeartbeatResponse(_message.Message):
    __slots__ = ("extension_hostname", "extension_port", "inference_hostname", "inference_port", "project_name")
    EXTENSION_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_PORT_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_PORT_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    extension_hostname: str
    extension_port: int
    inference_hostname: str
    inference_port: int
    project_name: str
    def __init__(self, extension_hostname: _Optional[str] = ..., extension_port: _Optional[int] = ..., inference_hostname: _Optional[str] = ..., inference_port: _Optional[int] = ..., project_name: _Optional[str] = ...) -> None: ...
