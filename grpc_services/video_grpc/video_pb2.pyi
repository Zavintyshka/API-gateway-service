from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VideoRequest(_message.Message):
    __slots__ = ("chunk", "command")
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    chunk: bytes
    command: str
    def __init__(self, chunk: _Optional[bytes] = ..., command: _Optional[str] = ...) -> None: ...

class ProcessedVideoResponse(_message.Message):
    __slots__ = ("chunk", "detail")
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    chunk: bytes
    detail: str
    def __init__(self, chunk: _Optional[bytes] = ..., detail: _Optional[str] = ...) -> None: ...
