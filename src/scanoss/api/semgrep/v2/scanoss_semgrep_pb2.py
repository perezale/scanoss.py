# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scanoss/api/semgrep/v2/scanoss-semgrep.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from scanoss.api.common.v2 import scanoss_common_pb2 as scanoss_dot_api_dot_common_dot_v2_dot_scanoss__common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,scanoss/api/semgrep/v2/scanoss-semgrep.proto\x12\x16scanoss.api.semgrep.v2\x1a*scanoss/api/common/v2/scanoss-common.proto\"\x96\x03\n\x0fSemgrepResponse\x12<\n\x05purls\x18\x01 \x03(\x0b\x32-.scanoss.api.semgrep.v2.SemgrepResponse.Purls\x12\x35\n\x06status\x18\x02 \x01(\x0b\x32%.scanoss.api.common.v2.StatusResponse\x1a\x43\n\x05Issue\x12\x0e\n\x06ruleID\x18\x01 \x01(\t\x12\x0c\n\x04\x66rom\x18\x02 \x01(\t\x12\n\n\x02to\x18\x03 \x01(\t\x12\x10\n\x08severity\x18\x04 \x01(\t\x1a\x64\n\x04\x46ile\x12\x0f\n\x07\x66ileMD5\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12=\n\x06issues\x18\x03 \x03(\x0b\x32-.scanoss.api.semgrep.v2.SemgrepResponse.Issue\x1a\x63\n\x05Purls\x12\x0c\n\x04purl\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12;\n\x05\x66iles\x18\x03 \x03(\x0b\x32,.scanoss.api.semgrep.v2.SemgrepResponse.File2\xb8\x01\n\x07Semgrep\x12Q\n\x04\x45\x63ho\x12\".scanoss.api.common.v2.EchoRequest\x1a#.scanoss.api.common.v2.EchoResponse\"\x00\x12Z\n\tGetIssues\x12\".scanoss.api.common.v2.PurlRequest\x1a\'.scanoss.api.semgrep.v2.SemgrepResponse\"\x00\x42\x31Z/github.com/scanoss/papi/api/semgrepv2;semgrepv2b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scanoss.api.semgrep.v2.scanoss_semgrep_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z/github.com/scanoss/papi/api/semgrepv2;semgrepv2'
  _SEMGREPRESPONSE._serialized_start=117
  _SEMGREPRESPONSE._serialized_end=523
  _SEMGREPRESPONSE_ISSUE._serialized_start=253
  _SEMGREPRESPONSE_ISSUE._serialized_end=320
  _SEMGREPRESPONSE_FILE._serialized_start=322
  _SEMGREPRESPONSE_FILE._serialized_end=422
  _SEMGREPRESPONSE_PURLS._serialized_start=424
  _SEMGREPRESPONSE_PURLS._serialized_end=523
  _SEMGREP._serialized_start=526
  _SEMGREP._serialized_end=710
# @@protoc_insertion_point(module_scope)