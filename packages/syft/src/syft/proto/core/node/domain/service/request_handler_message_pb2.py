# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/core/node/domain/service/request_handler_message.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# syft absolute
from syft.proto.core.common import (
    common_object_pb2 as proto_dot_core_dot_common_dot_common__object__pb2,
)
from syft.proto.core.common import (
    recursive_serde_pb2 as proto_dot_core_dot_common_dot_recursive__serde__pb2,
)
from syft.proto.lib.python import dict_pb2 as proto_dot_lib_dot_python_dot_dict__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="proto/core/node/domain/service/request_handler_message.proto",
    package="syft.core.node.domain.service",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n<proto/core/node/domain/service/request_handler_message.proto\x12\x1dsyft.core.node.domain.service\x1a%proto/core/common/common_object.proto\x1a\'proto/core/common/recursive_serde.proto\x1a\x1bproto/lib/python/dict.proto"\xad\x01\n\x1bUpdateRequestHandlerMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12\x31\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32 .syft.core.common.RecursiveSerde\x12&\n\x07handler\x18\x03 \x01(\x0b\x32\x15.syft.lib.python.Dict\x12\x0c\n\x04keep\x18\x04 \x01(\x08"\xac\x01\n\x1cGetAllRequestHandlersMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12\x31\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32 .syft.core.common.RecursiveSerde\x12\x32\n\x08reply_to\x18\x03 \x01(\x0b\x32 .syft.core.common.RecursiveSerde"\xa9\x01\n$GetAllRequestHandlersResponseMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12\x31\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32 .syft.core.common.RecursiveSerde\x12\'\n\x08handlers\x18\x03 \x03(\x0b\x32\x15.syft.lib.python.Dictb\x06proto3',
    dependencies=[
        proto_dot_core_dot_common_dot_common__object__pb2.DESCRIPTOR,
        proto_dot_core_dot_common_dot_recursive__serde__pb2.DESCRIPTOR,
        proto_dot_lib_dot_python_dot_dict__pb2.DESCRIPTOR,
    ],
)


_UPDATEREQUESTHANDLERMESSAGE = _descriptor.Descriptor(
    name="UpdateRequestHandlerMessage",
    full_name="syft.core.node.domain.service.UpdateRequestHandlerMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="msg_id",
            full_name="syft.core.node.domain.service.UpdateRequestHandlerMessage.msg_id",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="address",
            full_name="syft.core.node.domain.service.UpdateRequestHandlerMessage.address",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="handler",
            full_name="syft.core.node.domain.service.UpdateRequestHandlerMessage.handler",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="keep",
            full_name="syft.core.node.domain.service.UpdateRequestHandlerMessage.keep",
            index=3,
            number=4,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=205,
    serialized_end=378,
)


_GETALLREQUESTHANDLERSMESSAGE = _descriptor.Descriptor(
    name="GetAllRequestHandlersMessage",
    full_name="syft.core.node.domain.service.GetAllRequestHandlersMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="msg_id",
            full_name="syft.core.node.domain.service.GetAllRequestHandlersMessage.msg_id",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="address",
            full_name="syft.core.node.domain.service.GetAllRequestHandlersMessage.address",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="reply_to",
            full_name="syft.core.node.domain.service.GetAllRequestHandlersMessage.reply_to",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=381,
    serialized_end=553,
)


_GETALLREQUESTHANDLERSRESPONSEMESSAGE = _descriptor.Descriptor(
    name="GetAllRequestHandlersResponseMessage",
    full_name="syft.core.node.domain.service.GetAllRequestHandlersResponseMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="msg_id",
            full_name="syft.core.node.domain.service.GetAllRequestHandlersResponseMessage.msg_id",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="address",
            full_name="syft.core.node.domain.service.GetAllRequestHandlersResponseMessage.address",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="handlers",
            full_name="syft.core.node.domain.service.GetAllRequestHandlersResponseMessage.handlers",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=556,
    serialized_end=725,
)

_UPDATEREQUESTHANDLERMESSAGE.fields_by_name[
    "msg_id"
].message_type = proto_dot_core_dot_common_dot_common__object__pb2._UID
_UPDATEREQUESTHANDLERMESSAGE.fields_by_name[
    "address"
].message_type = proto_dot_core_dot_common_dot_recursive__serde__pb2._RECURSIVESERDE
_UPDATEREQUESTHANDLERMESSAGE.fields_by_name[
    "handler"
].message_type = proto_dot_lib_dot_python_dot_dict__pb2._DICT
_GETALLREQUESTHANDLERSMESSAGE.fields_by_name[
    "msg_id"
].message_type = proto_dot_core_dot_common_dot_common__object__pb2._UID
_GETALLREQUESTHANDLERSMESSAGE.fields_by_name[
    "address"
].message_type = proto_dot_core_dot_common_dot_recursive__serde__pb2._RECURSIVESERDE
_GETALLREQUESTHANDLERSMESSAGE.fields_by_name[
    "reply_to"
].message_type = proto_dot_core_dot_common_dot_recursive__serde__pb2._RECURSIVESERDE
_GETALLREQUESTHANDLERSRESPONSEMESSAGE.fields_by_name[
    "msg_id"
].message_type = proto_dot_core_dot_common_dot_common__object__pb2._UID
_GETALLREQUESTHANDLERSRESPONSEMESSAGE.fields_by_name[
    "address"
].message_type = proto_dot_core_dot_common_dot_recursive__serde__pb2._RECURSIVESERDE
_GETALLREQUESTHANDLERSRESPONSEMESSAGE.fields_by_name[
    "handlers"
].message_type = proto_dot_lib_dot_python_dot_dict__pb2._DICT
DESCRIPTOR.message_types_by_name[
    "UpdateRequestHandlerMessage"
] = _UPDATEREQUESTHANDLERMESSAGE
DESCRIPTOR.message_types_by_name[
    "GetAllRequestHandlersMessage"
] = _GETALLREQUESTHANDLERSMESSAGE
DESCRIPTOR.message_types_by_name[
    "GetAllRequestHandlersResponseMessage"
] = _GETALLREQUESTHANDLERSRESPONSEMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UpdateRequestHandlerMessage = _reflection.GeneratedProtocolMessageType(
    "UpdateRequestHandlerMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _UPDATEREQUESTHANDLERMESSAGE,
        "__module__": "proto.core.node.domain.service.request_handler_message_pb2"
        # @@protoc_insertion_point(class_scope:syft.core.node.domain.service.UpdateRequestHandlerMessage)
    },
)
_sym_db.RegisterMessage(UpdateRequestHandlerMessage)

GetAllRequestHandlersMessage = _reflection.GeneratedProtocolMessageType(
    "GetAllRequestHandlersMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _GETALLREQUESTHANDLERSMESSAGE,
        "__module__": "proto.core.node.domain.service.request_handler_message_pb2"
        # @@protoc_insertion_point(class_scope:syft.core.node.domain.service.GetAllRequestHandlersMessage)
    },
)
_sym_db.RegisterMessage(GetAllRequestHandlersMessage)

GetAllRequestHandlersResponseMessage = _reflection.GeneratedProtocolMessageType(
    "GetAllRequestHandlersResponseMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _GETALLREQUESTHANDLERSRESPONSEMESSAGE,
        "__module__": "proto.core.node.domain.service.request_handler_message_pb2"
        # @@protoc_insertion_point(class_scope:syft.core.node.domain.service.GetAllRequestHandlersResponseMessage)
    },
)
_sym_db.RegisterMessage(GetAllRequestHandlersResponseMessage)


# @@protoc_insertion_point(module_scope)
