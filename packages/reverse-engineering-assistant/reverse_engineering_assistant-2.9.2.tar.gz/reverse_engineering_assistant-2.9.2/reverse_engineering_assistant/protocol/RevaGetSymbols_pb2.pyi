from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SymbolType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FUNCTION: _ClassVar[SymbolType]
    DATA: _ClassVar[SymbolType]
    LABEL: _ClassVar[SymbolType]
FUNCTION: SymbolType
DATA: SymbolType
LABEL: SymbolType

class RevaGetSymbolsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RevaSymbolRequest(_message.Message):
    __slots__ = ("address", "name")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    address: str
    name: str
    def __init__(self, address: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class RevaSymbolResponse(_message.Message):
    __slots__ = ("name", "address", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    address: str
    type: SymbolType
    def __init__(self, name: _Optional[str] = ..., address: _Optional[str] = ..., type: _Optional[_Union[SymbolType, str]] = ...) -> None: ...

class RevaGetSymbolsResponse(_message.Message):
    __slots__ = ("symbols",)
    SYMBOLS_FIELD_NUMBER: _ClassVar[int]
    symbols: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, symbols: _Optional[_Iterable[str]] = ...) -> None: ...

class RevaSetSymbolNameRequest(_message.Message):
    __slots__ = ("old_name_or_address", "new_name")
    OLD_NAME_OR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NEW_NAME_FIELD_NUMBER: _ClassVar[int]
    old_name_or_address: str
    new_name: str
    def __init__(self, old_name_or_address: _Optional[str] = ..., new_name: _Optional[str] = ...) -> None: ...

class RevaGetNewSymbolNameRequest(_message.Message):
    __slots__ = ("symbol_name",)
    SYMBOL_NAME_FIELD_NUMBER: _ClassVar[int]
    symbol_name: str
    def __init__(self, symbol_name: _Optional[str] = ...) -> None: ...

class RevaGetNewSymbolNameResponse(_message.Message):
    __slots__ = ("new_symbol_name",)
    NEW_SYMBOL_NAME_FIELD_NUMBER: _ClassVar[int]
    new_symbol_name: str
    def __init__(self, new_symbol_name: _Optional[str] = ...) -> None: ...

class RevaSetSymbolNameResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
