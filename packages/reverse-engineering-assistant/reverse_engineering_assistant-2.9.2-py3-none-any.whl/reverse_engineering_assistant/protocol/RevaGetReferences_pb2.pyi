from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RevaGetReferencesRequest(_message.Message):
    __slots__ = ("address_or_symbol",)
    ADDRESS_OR_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    address_or_symbol: str
    def __init__(self, address_or_symbol: _Optional[str] = ...) -> None: ...

class RevaGetReferencesResponse(_message.Message):
    __slots__ = ("references_to", "references_from")
    REFERENCES_TO_FIELD_NUMBER: _ClassVar[int]
    REFERENCES_FROM_FIELD_NUMBER: _ClassVar[int]
    references_to: _containers.RepeatedScalarFieldContainer[str]
    references_from: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, references_to: _Optional[_Iterable[str]] = ..., references_from: _Optional[_Iterable[str]] = ...) -> None: ...
