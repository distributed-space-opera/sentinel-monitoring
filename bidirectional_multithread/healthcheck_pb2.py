# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: healthcheck.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11healthcheck.proto\x12\x06stream\"!\n\x0fresourceRequest\x12\x0e\n\x06nodeip\x18\x01 \x01(\t\"\x14\n\x12healthCheckRequest\"\"\n\x10healthCheckReply\x12\x0e\n\x06status\x18\x01 \x01(\t2\xa2\x01\n\x12SentinelMonitoring\x12\x45\n\x0bhealthCheck\x12\x1a.stream.healthCheckRequest\x1a\x18.stream.healthCheckReply\"\x00\x12\x45\n\x0b\x63lientAlive\x12\x1a.stream.healthCheckRequest\x1a\x18.stream.healthCheckReply\"\x00\x42\x13\n\x0forg.node.protosP\x01\x62\x06proto3')



_RESOURCEREQUEST = DESCRIPTOR.message_types_by_name['resourceRequest']
_HEALTHCHECKREQUEST = DESCRIPTOR.message_types_by_name['healthCheckRequest']
_HEALTHCHECKREPLY = DESCRIPTOR.message_types_by_name['healthCheckReply']
resourceRequest = _reflection.GeneratedProtocolMessageType('resourceRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCEREQUEST,
  '__module__' : 'healthcheck_pb2'
  # @@protoc_insertion_point(class_scope:stream.resourceRequest)
  })
_sym_db.RegisterMessage(resourceRequest)

healthCheckRequest = _reflection.GeneratedProtocolMessageType('healthCheckRequest', (_message.Message,), {
  'DESCRIPTOR' : _HEALTHCHECKREQUEST,
  '__module__' : 'healthcheck_pb2'
  # @@protoc_insertion_point(class_scope:stream.healthCheckRequest)
  })
_sym_db.RegisterMessage(healthCheckRequest)

healthCheckReply = _reflection.GeneratedProtocolMessageType('healthCheckReply', (_message.Message,), {
  'DESCRIPTOR' : _HEALTHCHECKREPLY,
  '__module__' : 'healthcheck_pb2'
  # @@protoc_insertion_point(class_scope:stream.healthCheckReply)
  })
_sym_db.RegisterMessage(healthCheckReply)

_SENTINELMONITORING = DESCRIPTOR.services_by_name['SentinelMonitoring']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017org.node.protosP\001'
  _RESOURCEREQUEST._serialized_start=29
  _RESOURCEREQUEST._serialized_end=62
  _HEALTHCHECKREQUEST._serialized_start=64
  _HEALTHCHECKREQUEST._serialized_end=84
  _HEALTHCHECKREPLY._serialized_start=86
  _HEALTHCHECKREPLY._serialized_end=120
  _SENTINELMONITORING._serialized_start=123
  _SENTINELMONITORING._serialized_end=285
# @@protoc_insertion_point(module_scope)
