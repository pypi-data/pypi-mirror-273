from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class RuntimeTaskType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RUNTIME_TASK_TYPE_UNSPECIFIED: _ClassVar[RuntimeTaskType]
    RUNTIME_TASK_TYPE_CREATE_IMPORT_PLAN: _ClassVar[RuntimeTaskType]
    RUNTIME_TASK_TYPE_APPLY_IMPORT_PLAN: _ClassVar[RuntimeTaskType]

RUNTIME_TASK_TYPE_UNSPECIFIED: RuntimeTaskType
RUNTIME_TASK_TYPE_CREATE_IMPORT_PLAN: RuntimeTaskType
RUNTIME_TASK_TYPE_APPLY_IMPORT_PLAN: RuntimeTaskType

class BaseTaskMetadata(_message.Message):
    __slots__ = ('run_id', 'shared_root', 'step_id', 'task_type')
    SHARED_ROOT_FIELD_NUMBER: _ClassVar[int]
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_TYPE_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    shared_root: str
    step_id: str
    task_type: RuntimeTaskType
    run_id: str
    def __init__(
        self,
        shared_root: _Optional[str] = ...,
        step_id: _Optional[str] = ...,
        task_type: _Optional[_Union[RuntimeTaskType, str]] = ...,
        run_id: _Optional[str] = ...,
    ) -> None: ...

class DataCatalog(_message.Message):
    __slots__ = ('datalake_uri', 'type', 'url')
    TYPE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    DATALAKE_URI_FIELD_NUMBER: _ClassVar[int]
    type: str
    url: str
    datalake_uri: str
    def __init__(
        self, type: _Optional[str] = ..., url: _Optional[str] = ..., datalake_uri: _Optional[str] = ...
    ) -> None: ...

class BaseRunnerInstructions(_message.Message):
    __slots__ = ('runtime_output_filepath',)
    RUNTIME_OUTPUT_FILEPATH_FIELD_NUMBER: _ClassVar[int]
    runtime_output_filepath: str
    def __init__(self, runtime_output_filepath: _Optional[str] = ...) -> None: ...
