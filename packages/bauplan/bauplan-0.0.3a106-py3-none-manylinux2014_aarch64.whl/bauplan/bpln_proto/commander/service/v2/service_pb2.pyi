from typing import (
    ClassVar as _ClassVar,
)
from typing import (
    Iterable as _Iterable,
)
from typing import (
    Mapping as _Mapping,
)
from typing import (
    Optional as _Optional,
)
from typing import (
    Union as _Union,
)

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class CodeIntelligenceError(_message.Message):
    __slots__ = ('message', 'traceback', 'type')
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TRACEBACK_FIELD_NUMBER: _ClassVar[int]
    type: str
    message: str
    traceback: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        type: _Optional[str] = ...,
        message: _Optional[str] = ...,
        traceback: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class CodeIntelligenceResponseMetadata(_message.Message):
    __slots__ = ('response_id', 'response_ts', 'status_code')
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    response_id: str
    response_ts: int
    def __init__(
        self,
        status_code: _Optional[int] = ...,
        response_id: _Optional[str] = ...,
        response_ts: _Optional[int] = ...,
    ) -> None: ...

class CodeIntelligenceDropTableResponse(_message.Message):
    __slots__ = ('data', 'error', 'metadata')
    DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    data: DropTableResponseData
    metadata: CodeIntelligenceResponseMetadata
    error: CodeIntelligenceError
    def __init__(
        self,
        data: _Optional[_Union[DropTableResponseData, _Mapping]] = ...,
        metadata: _Optional[_Union[CodeIntelligenceResponseMetadata, _Mapping]] = ...,
        error: _Optional[_Union[CodeIntelligenceError, _Mapping]] = ...,
    ) -> None: ...

class CreateImportPlanRequest(_message.Message):
    __slots__ = ('max_rows', 'search_string')
    SEARCH_STRING_FIELD_NUMBER: _ClassVar[int]
    MAX_ROWS_FIELD_NUMBER: _ClassVar[int]
    search_string: str
    max_rows: int
    def __init__(self, search_string: _Optional[str] = ..., max_rows: _Optional[int] = ...) -> None: ...

class CreateImportPlanResponse(_message.Message):
    __slots__ = ('job_id',)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class ApplyImportPlanRequest(_message.Message):
    __slots__ = ('branch', 'plan_yaml', 'table')
    PLAN_YAML_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    plan_yaml: str
    branch: str
    table: str
    def __init__(
        self, plan_yaml: _Optional[str] = ..., branch: _Optional[str] = ..., table: _Optional[str] = ...
    ) -> None: ...

class ApplyImportPlanResponse(_message.Message):
    __slots__ = ('job_id',)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class DropTableResponseData(_message.Message):
    __slots__ = ('branch_name', 'deleted')
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    DELETED_FIELD_NUMBER: _ClassVar[int]
    branch_name: str
    deleted: bool
    def __init__(self, branch_name: _Optional[str] = ..., deleted: bool = ...) -> None: ...

class DropTableRequest(_message.Message):
    __slots__ = ('branch_name', 'table_name')
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    branch_name: str
    table_name: str
    def __init__(self, branch_name: _Optional[str] = ..., table_name: _Optional[str] = ...) -> None: ...

class DropTableResponse(_message.Message):
    __slots__ = ('deleted', 'error')
    DELETED_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    deleted: bool
    error: str
    def __init__(self, deleted: bool = ..., error: _Optional[str] = ...) -> None: ...
