from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VideoRequest(_message.Message):
    __slots__ = ("chunk", "action_type", "action")
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    chunk: bytes
    action_type: str
    action: str
    def __init__(self, chunk: _Optional[bytes] = ..., action_type: _Optional[str] = ..., action: _Optional[str] = ...) -> None: ...

class ProcessedVideoResponse(_message.Message):
    __slots__ = ("chunk", "detail")
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    chunk: bytes
    detail: str
    def __init__(self, chunk: _Optional[bytes] = ..., detail: _Optional[str] = ...) -> None: ...
