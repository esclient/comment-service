# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: comment.proto
# Protobuf Python Version: 6.31.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '',
    'comment.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rcomment.proto\x12\x07\x63omment\"]\n\x07\x43omment\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x11\n\tauthor_id\x18\x02 \x01(\x03\x12\x0c\n\x04text\x18\x03 \x01(\t\x12\x12\n\ncreated_at\x18\x04 \x01(\x03\x12\x11\n\tedited_at\x18\x05 \x01(\x03\"G\n\x14\x43reateCommentRequest\x12\x0e\n\x06mod_id\x18\x01 \x01(\x03\x12\x11\n\tauthor_id\x18\x02 \x01(\x03\x12\x0c\n\x04text\x18\x03 \x01(\t\"+\n\x15\x43reateCommentResponse\x12\x12\n\ncomment_id\x18\x01 \x01(\x03\"$\n\x12GetCommentsRequest\x12\x0e\n\x06mod_id\x18\x01 \x01(\x03\"I\n\x13GetCommentsResponse\x12\x0e\n\x06mod_id\x18\x01 \x01(\x03\x12\"\n\x08\x63omments\x18\x02 \x03(\x0b\x32\x10.comment.Comment\"*\n\x14\x44\x65leteCommentRequest\x12\x12\n\ncomment_id\x18\x01 \x01(\x03\"(\n\x15\x44\x65leteCommentResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"6\n\x12\x45\x64itCommentRequest\x12\x12\n\ncomment_id\x18\x01 \x01(\x03\x12\x0c\n\x04text\x18\x02 \x01(\t\"&\n\x13\x45\x64itCommentResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xc4\x02\n\x0e\x43ommentService\x12N\n\rCreateComment\x12\x1d.comment.CreateCommentRequest\x1a\x1e.comment.CreateCommentResponse\x12H\n\x0bGetComments\x12\x1b.comment.GetCommentsRequest\x1a\x1c.comment.GetCommentsResponse\x12N\n\rDeleteComment\x12\x1d.comment.DeleteCommentRequest\x1a\x1e.comment.DeleteCommentResponse\x12H\n\x0b\x45\x64itComment\x12\x1b.comment.EditCommentRequest\x1a\x1c.comment.EditCommentResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'comment_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_COMMENT']._serialized_start=26
  _globals['_COMMENT']._serialized_end=119
  _globals['_CREATECOMMENTREQUEST']._serialized_start=121
  _globals['_CREATECOMMENTREQUEST']._serialized_end=192
  _globals['_CREATECOMMENTRESPONSE']._serialized_start=194
  _globals['_CREATECOMMENTRESPONSE']._serialized_end=237
  _globals['_GETCOMMENTSREQUEST']._serialized_start=239
  _globals['_GETCOMMENTSREQUEST']._serialized_end=275
  _globals['_GETCOMMENTSRESPONSE']._serialized_start=277
  _globals['_GETCOMMENTSRESPONSE']._serialized_end=350
  _globals['_DELETECOMMENTREQUEST']._serialized_start=352
  _globals['_DELETECOMMENTREQUEST']._serialized_end=394
  _globals['_DELETECOMMENTRESPONSE']._serialized_start=396
  _globals['_DELETECOMMENTRESPONSE']._serialized_end=436
  _globals['_EDITCOMMENTREQUEST']._serialized_start=438
  _globals['_EDITCOMMENTREQUEST']._serialized_end=492
  _globals['_EDITCOMMENTRESPONSE']._serialized_start=494
  _globals['_EDITCOMMENTRESPONSE']._serialized_end=532
  _globals['_COMMENTSERVICE']._serialized_start=535
  _globals['_COMMENTSERVICE']._serialized_end=859
# @@protoc_insertion_point(module_scope)
