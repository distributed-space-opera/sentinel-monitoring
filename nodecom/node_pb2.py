# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: node.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nnode.proto\x12\x06stream\"&\n\x14proposeLeaderRequest\x12\x0e\n\x06termid\x18\x01 \x01(\t\")\n\x15proposeLeaderResponse\x12\x10\n\x08response\x18\x01 \x01(\t\"\'\n\x13updateLeaderRequest\x12\x10\n\x08leaderip\x18\x01 \x01(\t\"&\n\x14updateLeaderResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\"\x17\n\x15GetListOfNodesRequest\")\n\x16GetListOfNodesResponse\x12\x0f\n\x07nodeips\x18\x01 \x03(\t2\xfd\x01\n\x11NodeCommunication\x12K\n\x0cupdateLeader\x12\x1b.stream.updateLeaderRequest\x1a\x1c.stream.updateLeaderResponse\"\x00\x12N\n\rproposeLeader\x12\x1c.stream.proposeLeaderRequest\x1a\x1d.stream.proposeLeaderResponse\"\x00\x12K\n\x08GetNodes\x12\x1d.stream.GetListOfNodesRequest\x1a\x1e.stream.GetListOfNodesResponse\"\x00\x42\x13\n\x0forg.node.protosP\x01\x62\x06proto3')



_PROPOSELEADERREQUEST = DESCRIPTOR.message_types_by_name['proposeLeaderRequest']
_PROPOSELEADERRESPONSE = DESCRIPTOR.message_types_by_name['proposeLeaderResponse']
_UPDATELEADERREQUEST = DESCRIPTOR.message_types_by_name['updateLeaderRequest']
_UPDATELEADERRESPONSE = DESCRIPTOR.message_types_by_name['updateLeaderResponse']
_GETLISTOFNODESREQUEST = DESCRIPTOR.message_types_by_name['GetListOfNodesRequest']
_GETLISTOFNODESRESPONSE = DESCRIPTOR.message_types_by_name['GetListOfNodesResponse']
proposeLeaderRequest = _reflection.GeneratedProtocolMessageType('proposeLeaderRequest', (_message.Message,), {
  'DESCRIPTOR' : _PROPOSELEADERREQUEST,
  '__module__' : 'node_pb2'
  # @@protoc_insertion_point(class_scope:stream.proposeLeaderRequest)
  })
_sym_db.RegisterMessage(proposeLeaderRequest)

proposeLeaderResponse = _reflection.GeneratedProtocolMessageType('proposeLeaderResponse', (_message.Message,), {
  'DESCRIPTOR' : _PROPOSELEADERRESPONSE,
  '__module__' : 'node_pb2'
  # @@protoc_insertion_point(class_scope:stream.proposeLeaderResponse)
  })
_sym_db.RegisterMessage(proposeLeaderResponse)

updateLeaderRequest = _reflection.GeneratedProtocolMessageType('updateLeaderRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATELEADERREQUEST,
  '__module__' : 'node_pb2'
  # @@protoc_insertion_point(class_scope:stream.updateLeaderRequest)
  })
_sym_db.RegisterMessage(updateLeaderRequest)

updateLeaderResponse = _reflection.GeneratedProtocolMessageType('updateLeaderResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATELEADERRESPONSE,
  '__module__' : 'node_pb2'
  # @@protoc_insertion_point(class_scope:stream.updateLeaderResponse)
  })
_sym_db.RegisterMessage(updateLeaderResponse)

GetListOfNodesRequest = _reflection.GeneratedProtocolMessageType('GetListOfNodesRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETLISTOFNODESREQUEST,
  '__module__' : 'node_pb2'
  # @@protoc_insertion_point(class_scope:stream.GetListOfNodesRequest)
  })
_sym_db.RegisterMessage(GetListOfNodesRequest)

GetListOfNodesResponse = _reflection.GeneratedProtocolMessageType('GetListOfNodesResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETLISTOFNODESRESPONSE,
  '__module__' : 'node_pb2'
  # @@protoc_insertion_point(class_scope:stream.GetListOfNodesResponse)
  })
_sym_db.RegisterMessage(GetListOfNodesResponse)

_NODECOMMUNICATION = DESCRIPTOR.services_by_name['NodeCommunication']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017org.node.protosP\001'
  _PROPOSELEADERREQUEST._serialized_start=22
  _PROPOSELEADERREQUEST._serialized_end=60
  _PROPOSELEADERRESPONSE._serialized_start=62
  _PROPOSELEADERRESPONSE._serialized_end=103
  _UPDATELEADERREQUEST._serialized_start=105
  _UPDATELEADERREQUEST._serialized_end=144
  _UPDATELEADERRESPONSE._serialized_start=146
  _UPDATELEADERRESPONSE._serialized_end=184
  _GETLISTOFNODESREQUEST._serialized_start=186
  _GETLISTOFNODESREQUEST._serialized_end=209
  _GETLISTOFNODESRESPONSE._serialized_start=211
  _GETLISTOFNODESRESPONSE._serialized_end=252
  _NODECOMMUNICATION._serialized_start=255
  _NODECOMMUNICATION._serialized_end=508
# @@protoc_insertion_point(module_scope)