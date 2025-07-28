from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

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
