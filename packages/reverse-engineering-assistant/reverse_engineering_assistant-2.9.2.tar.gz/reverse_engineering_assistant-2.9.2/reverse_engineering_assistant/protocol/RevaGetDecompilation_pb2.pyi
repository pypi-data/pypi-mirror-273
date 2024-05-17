import RevaVariable_pb2 as _RevaVariable_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RevaGetDecompilationRequest(_message.Message):
    __slots__ = ("function", "address")
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    function: str
    address: str
    def __init__(self, function: _Optional[str] = ..., address: _Optional[str] = ...) -> None: ...

class RevaGetDecompilationResponse(_message.Message):
    __slots__ = ("address", "function", "function_signature", "incoming_calls", "outgoing_calls", "variables", "listing", "decompilation", "error_message")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    INCOMING_CALLS_FIELD_NUMBER: _ClassVar[int]
    OUTGOING_CALLS_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    LISTING_FIELD_NUMBER: _ClassVar[int]
    DECOMPILATION_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    address: int
    function: str
    function_signature: str
    incoming_calls: _containers.RepeatedScalarFieldContainer[str]
    outgoing_calls: _containers.RepeatedScalarFieldContainer[str]
    variables: _containers.RepeatedCompositeFieldContainer[_RevaVariable_pb2.RevaVariable]
    listing: str
    decompilation: str
    error_message: str
    def __init__(self, address: _Optional[int] = ..., function: _Optional[str] = ..., function_signature: _Optional[str] = ..., incoming_calls: _Optional[_Iterable[str]] = ..., outgoing_calls: _Optional[_Iterable[str]] = ..., variables: _Optional[_Iterable[_Union[_RevaVariable_pb2.RevaVariable, _Mapping]]] = ..., listing: _Optional[str] = ..., decompilation: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class RevaRenameFunctionVariableRequest(_message.Message):
    __slots__ = ("function_name", "old_name", "new_name")
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    OLD_NAME_FIELD_NUMBER: _ClassVar[int]
    NEW_NAME_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    old_name: str
    new_name: str
    def __init__(self, function_name: _Optional[str] = ..., old_name: _Optional[str] = ..., new_name: _Optional[str] = ...) -> None: ...

class RevaRenameFunctionVariableResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RevaGetFunctionListRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RevaGetFunctionListResponse(_message.Message):
    __slots__ = ("function_name", "function_signature", "entry_point", "incoming_calls", "outgoing_calls")
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    ENTRY_POINT_FIELD_NUMBER: _ClassVar[int]
    INCOMING_CALLS_FIELD_NUMBER: _ClassVar[int]
    OUTGOING_CALLS_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    function_signature: str
    entry_point: str
    incoming_calls: _containers.RepeatedScalarFieldContainer[str]
    outgoing_calls: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, function_name: _Optional[str] = ..., function_signature: _Optional[str] = ..., entry_point: _Optional[str] = ..., incoming_calls: _Optional[_Iterable[str]] = ..., outgoing_calls: _Optional[_Iterable[str]] = ...) -> None: ...
