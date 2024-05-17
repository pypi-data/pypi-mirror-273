from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RevaGetDataAtAddressRequest(_message.Message):
    __slots__ = ("address", "symbol", "size")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    address: str
    symbol: str
    size: int
    def __init__(self, address: _Optional[str] = ..., symbol: _Optional[str] = ..., size: _Optional[int] = ...) -> None: ...

class RevaGetDataAtAddressResponse(_message.Message):
    __slots__ = ("address", "data", "symbol", "type", "incoming_references", "outgoing_references", "size")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INCOMING_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    OUTGOING_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    address: str
    data: bytes
    symbol: str
    type: str
    incoming_references: _containers.RepeatedScalarFieldContainer[str]
    outgoing_references: _containers.RepeatedScalarFieldContainer[str]
    size: int
    def __init__(self, address: _Optional[str] = ..., data: _Optional[bytes] = ..., symbol: _Optional[str] = ..., type: _Optional[str] = ..., incoming_references: _Optional[_Iterable[str]] = ..., outgoing_references: _Optional[_Iterable[str]] = ..., size: _Optional[int] = ...) -> None: ...

class RevaDataListRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RevaDataListResponse(_message.Message):
    __slots__ = ("address", "symbol", "type", "size", "incoming_references", "outgoing_references")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    INCOMING_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    OUTGOING_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    address: str
    symbol: str
    type: str
    size: int
    incoming_references: _containers.RepeatedScalarFieldContainer[str]
    outgoing_references: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, address: _Optional[str] = ..., symbol: _Optional[str] = ..., type: _Optional[str] = ..., size: _Optional[int] = ..., incoming_references: _Optional[_Iterable[str]] = ..., outgoing_references: _Optional[_Iterable[str]] = ...) -> None: ...

class RevaStringListRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RevaStringListResponse(_message.Message):
    __slots__ = ("address", "symbol", "value", "incoming_references", "outgoing_references")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    INCOMING_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    OUTGOING_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    address: str
    symbol: str
    value: str
    incoming_references: _containers.RepeatedScalarFieldContainer[str]
    outgoing_references: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, address: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[str] = ..., incoming_references: _Optional[_Iterable[str]] = ..., outgoing_references: _Optional[_Iterable[str]] = ...) -> None: ...
