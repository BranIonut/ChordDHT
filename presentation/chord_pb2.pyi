from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LogsResponse(_message.Message):
    __slots__ = ("log_line",)
    LOG_LINE_FIELD_NUMBER: _ClassVar[int]
    log_line: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, log_line: _Optional[_Iterable[str]] = ...) -> None: ...

class GetNodeInfoRequest(_message.Message):
    __slots__ = ("target_id",)
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    target_id: str
    def __init__(self, target_id: _Optional[str] = ...) -> None: ...

class GetNodeInfoResponse(_message.Message):
    __slots__ = ("node_id", "successor", "predecessor", "finger_table")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESSOR_FIELD_NUMBER: _ClassVar[int]
    PREDECESSOR_FIELD_NUMBER: _ClassVar[int]
    FINGER_TABLE_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    successor: str
    predecessor: str
    finger_table: _containers.RepeatedCompositeFieldContainer[FingerEntry]
    def __init__(self, node_id: _Optional[str] = ..., successor: _Optional[str] = ..., predecessor: _Optional[str] = ..., finger_table: _Optional[_Iterable[_Union[FingerEntry, _Mapping]]] = ...) -> None: ...

class FingerEntry(_message.Message):
    __slots__ = ("index", "finger_val")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    FINGER_VAL_FIELD_NUMBER: _ClassVar[int]
    index: str
    finger_val: str
    def __init__(self, index: _Optional[str] = ..., finger_val: _Optional[str] = ...) -> None: ...

class GetNodeStatsRequest(_message.Message):
    __slots__ = ("target_id",)
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    target_id: str
    def __init__(self, target_id: _Optional[str] = ...) -> None: ...

class GetNodeStatsResponse(_message.Message):
    __slots__ = ("fixes", "stabilization", "lookups", "join_time")
    FIXES_FIELD_NUMBER: _ClassVar[int]
    STABILIZATION_FIELD_NUMBER: _ClassVar[int]
    LOOKUPS_FIELD_NUMBER: _ClassVar[int]
    JOIN_TIME_FIELD_NUMBER: _ClassVar[int]
    fixes: str
    stabilization: str
    lookups: str
    join_time: str
    def __init__(self, fixes: _Optional[str] = ..., stabilization: _Optional[str] = ..., lookups: _Optional[str] = ..., join_time: _Optional[str] = ...) -> None: ...

class FindSuccessorRequest(_message.Message):
    __slots__ = ("target_id", "key")
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    target_id: str
    key: str
    def __init__(self, target_id: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class FindSuccessorResponse(_message.Message):
    __slots__ = ("successor_id",)
    SUCCESSOR_ID_FIELD_NUMBER: _ClassVar[int]
    successor_id: str
    def __init__(self, successor_id: _Optional[str] = ...) -> None: ...

class FindPredecessorRequest(_message.Message):
    __slots__ = ("target_id",)
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    target_id: str
    def __init__(self, target_id: _Optional[str] = ...) -> None: ...

class FindPredecessorResponse(_message.Message):
    __slots__ = ("predecessor_id",)
    PREDECESSOR_ID_FIELD_NUMBER: _ClassVar[int]
    predecessor_id: str
    def __init__(self, predecessor_id: _Optional[str] = ...) -> None: ...

class SetSuccessorRequest(_message.Message):
    __slots__ = ("target_id", "new_successor_id")
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_SUCCESSOR_ID_FIELD_NUMBER: _ClassVar[int]
    target_id: str
    new_successor_id: str
    def __init__(self, target_id: _Optional[str] = ..., new_successor_id: _Optional[str] = ...) -> None: ...

class SetSuccessorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetPredecessorRequest(_message.Message):
    __slots__ = ("target_id", "new_predecessor_id")
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_PREDECESSOR_ID_FIELD_NUMBER: _ClassVar[int]
    target_id: str
    new_predecessor_id: str
    def __init__(self, target_id: _Optional[str] = ..., new_predecessor_id: _Optional[str] = ...) -> None: ...

class SetPredecessorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NodeHasInformationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class NodeHasInformationResponse(_message.Message):
    __slots__ = ("information",)
    INFORMATION_FIELD_NUMBER: _ClassVar[int]
    information: str
    def __init__(self, information: _Optional[str] = ...) -> None: ...

class NotifyRequest(_message.Message):
    __slots__ = ("target_id", "sender_id")
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    target_id: str
    sender_id: str
    def __init__(self, target_id: _Optional[str] = ..., sender_id: _Optional[str] = ...) -> None: ...

class UpdateFingerTableRequest(_message.Message):
    __slots__ = ("target_id", "new_node_id", "index")
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    target_id: str
    new_node_id: str
    index: str
    def __init__(self, target_id: _Optional[str] = ..., new_node_id: _Optional[str] = ..., index: _Optional[str] = ...) -> None: ...

class UpdateFingerTableResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NotifyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetInfoRequest(_message.Message):
    __slots__ = ("target_id", "key")
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    target_id: str
    key: str
    def __init__(self, target_id: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class GetInfoResponse(_message.Message):
    __slots__ = ("information",)
    INFORMATION_FIELD_NUMBER: _ClassVar[int]
    information: str
    def __init__(self, information: _Optional[str] = ...) -> None: ...

class GetAllInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAllInfoResponse(_message.Message):
    __slots__ = ("info_line",)
    INFO_LINE_FIELD_NUMBER: _ClassVar[int]
    info_line: _containers.RepeatedCompositeFieldContainer[InfoLine]
    def __init__(self, info_line: _Optional[_Iterable[_Union[InfoLine, _Mapping]]] = ...) -> None: ...

class InfoLine(_message.Message):
    __slots__ = ("info_key", "info_val")
    INFO_KEY_FIELD_NUMBER: _ClassVar[int]
    INFO_VAL_FIELD_NUMBER: _ClassVar[int]
    info_key: str
    info_val: str
    def __init__(self, info_key: _Optional[str] = ..., info_val: _Optional[str] = ...) -> None: ...

class AddInfoRequest(_message.Message):
    __slots__ = ("info_key", "info")
    INFO_KEY_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    info_key: str
    info: str
    def __init__(self, info_key: _Optional[str] = ..., info: _Optional[str] = ...) -> None: ...

class AddInfoResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FixFingersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FixFingersResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StabilizeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StabilizeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RemoveInfoRequest(_message.Message):
    __slots__ = ("target_id", "info_key")
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    INFO_KEY_FIELD_NUMBER: _ClassVar[int]
    target_id: str
    info_key: str
    def __init__(self, target_id: _Optional[str] = ..., info_key: _Optional[str] = ...) -> None: ...

class RemoveInfoResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
