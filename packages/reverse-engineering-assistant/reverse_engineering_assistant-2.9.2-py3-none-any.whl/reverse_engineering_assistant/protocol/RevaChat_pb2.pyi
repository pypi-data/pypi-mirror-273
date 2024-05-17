from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RevaChatMessage(_message.Message):
    __slots__ = ("chatId", "message", "project", "programName")
    CHATID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    PROGRAMNAME_FIELD_NUMBER: _ClassVar[int]
    chatId: str
    message: str
    project: str
    programName: str
    def __init__(self, chatId: _Optional[str] = ..., message: _Optional[str] = ..., project: _Optional[str] = ..., programName: _Optional[str] = ...) -> None: ...

class RevaChatMessageResponse(_message.Message):
    __slots__ = ("chatId", "thought", "message")
    CHATID_FIELD_NUMBER: _ClassVar[int]
    THOUGHT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    chatId: str
    thought: str
    message: str
    def __init__(self, chatId: _Optional[str] = ..., thought: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
