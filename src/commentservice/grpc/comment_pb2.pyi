from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Comment(_message.Message):
    __slots__ = ("id", "author_id", "text", "created_at", "edited_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EDITED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    author_id: int
    text: str
    created_at: int
    edited_at: int
    def __init__(self, id: _Optional[int] = ..., author_id: _Optional[int] = ..., text: _Optional[str] = ..., created_at: _Optional[int] = ..., edited_at: _Optional[int] = ...) -> None: ...

class CreateCommentRequest(_message.Message):
    __slots__ = ("mod_id", "author_id", "text")
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    author_id: int
    text: str
    def __init__(self, mod_id: _Optional[int] = ..., author_id: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class CreateCommentResponse(_message.Message):
    __slots__ = ("comment_id",)
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    comment_id: int
    def __init__(self, comment_id: _Optional[int] = ...) -> None: ...

class GetCommentsRequest(_message.Message):
    __slots__ = ("mod_id",)
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    def __init__(self, mod_id: _Optional[int] = ...) -> None: ...

class GetCommentsResponse(_message.Message):
    __slots__ = ("mod_id", "comments")
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    comments: _containers.RepeatedCompositeFieldContainer[Comment]
    def __init__(self, mod_id: _Optional[int] = ..., comments: _Optional[_Iterable[_Union[Comment, _Mapping]]] = ...) -> None: ...

class DeleteCommentRequest(_message.Message):
    __slots__ = ("comment_id",)
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    comment_id: int
    def __init__(self, comment_id: _Optional[int] = ...) -> None: ...

class DeleteCommentResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class EditCommentRequest(_message.Message):
    __slots__ = ("comment_id", "text")
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    comment_id: int
    text: str
    def __init__(self, comment_id: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class EditCommentResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
