from .google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatelessConversation(_message.Message):
    __slots__ = ("stateless_conversation_id", "responses", "system_prompt_name", "name", "username", "expose_username_to_grok", "disable_search", "enable_image_generation", "model_name", "x_posts_as_field")
    STATELESS_CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_PROMPT_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EXPOSE_USERNAME_TO_GROK_FIELD_NUMBER: _ClassVar[int]
    DISABLE_SEARCH_FIELD_NUMBER: _ClassVar[int]
    ENABLE_IMAGE_GENERATION_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    X_POSTS_AS_FIELD_FIELD_NUMBER: _ClassVar[int]
    stateless_conversation_id: str
    responses: _containers.RepeatedCompositeFieldContainer[StatelessResponse]
    system_prompt_name: str
    name: str
    username: str
    expose_username_to_grok: bool
    disable_search: bool
    enable_image_generation: bool
    model_name: str
    x_posts_as_field: bool
    def __init__(self, stateless_conversation_id: _Optional[str] = ..., responses: _Optional[_Iterable[_Union[StatelessResponse, _Mapping]]] = ..., system_prompt_name: _Optional[str] = ..., name: _Optional[str] = ..., username: _Optional[str] = ..., expose_username_to_grok: bool = ..., disable_search: bool = ..., enable_image_generation: bool = ..., model_name: _Optional[str] = ..., x_posts_as_field: bool = ...) -> None: ...

class StatelessResponse(_message.Message):
    __slots__ = ("sender", "message", "query", "query_type", "image_attachment", "x_post_ids")
    class Sender(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[StatelessResponse.Sender]
        HUMAN: _ClassVar[StatelessResponse.Sender]
        ASSISTANT: _ClassVar[StatelessResponse.Sender]
    UNKNOWN: StatelessResponse.Sender
    HUMAN: StatelessResponse.Sender
    ASSISTANT: StatelessResponse.Sender
    SENDER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    QUERY_TYPE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    X_POST_IDS_FIELD_NUMBER: _ClassVar[int]
    sender: StatelessResponse.Sender
    message: str
    query: str
    query_type: str
    image_attachment: ImageAttachment
    x_post_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, sender: _Optional[_Union[StatelessResponse.Sender, str]] = ..., message: _Optional[str] = ..., query: _Optional[str] = ..., query_type: _Optional[str] = ..., image_attachment: _Optional[_Union[ImageAttachment, _Mapping]] = ..., x_post_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ImageAttachment(_message.Message):
    __slots__ = ("image_bytes", "content_type")
    IMAGE_BYTES_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    image_bytes: bytes
    content_type: str
    def __init__(self, image_bytes: _Optional[bytes] = ..., content_type: _Optional[str] = ...) -> None: ...

class DeleteLoggedConversationsRequest(_message.Message):
    __slots__ = ("accounting_key",)
    ACCOUNTING_KEY_FIELD_NUMBER: _ClassVar[int]
    accounting_key: str
    def __init__(self, accounting_key: _Optional[str] = ...) -> None: ...
