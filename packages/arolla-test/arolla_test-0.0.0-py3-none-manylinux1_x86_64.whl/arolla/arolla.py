# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Arolla Python API."""

from arolla.abc import abc as _abc
from arolla.expr import expr as _expr
from arolla.optools import optools as _optools
from arolla.s11n import s11n as _s11n
from arolla.testing import testing as _testing
from arolla.types import types as _types

#
# ABC
#

QTYPE = _abc.QTYPE
QType = _abc.QType

QValue = _abc.QValue
AnyQValue = _abc.AnyQValue

Expr = _abc.Expr

quote = _abc.ExprQuote


# `NOTHING` a type with no values. Otherwise, it's an uninhabited type.
NOTHING = _abc.NOTHING

# The main purpose of `unspecified` is to serve as a default value
# for a parameter in situations where the actual default value must be
# determined based on other parameters.
UNSPECIFIED = _abc.UNSPECIFIED
unspecified = _abc.unspecified

OPERATOR = _abc.OPERATOR

get_leaf_keys = _abc.get_leaf_keys

sub_by_fingerprint = _abc.sub_by_fingerprint
sub_by_name = _abc.sub_by_name
sub_leaves = _abc.sub_leaves
sub_placeholders = _abc.sub_placeholders


#
# TYPES
#

## QTypes

UNIT = _types.UNIT
BOOLEAN = _types.BOOLEAN
BYTES = _types.BYTES
TEXT = _types.TEXT
INT32 = _types.INT32
INT64 = _types.INT64
FLOAT32 = _types.FLOAT32
FLOAT64 = _types.FLOAT64
WEAK_FLOAT = _types.WEAK_FLOAT
SCALAR_SHAPE = _types.SCALAR_SHAPE

OPTIONAL_UNIT = _types.OPTIONAL_UNIT
OPTIONAL_BOOLEAN = _types.OPTIONAL_BOOLEAN
OPTIONAL_BYTES = _types.OPTIONAL_BYTES
OPTIONAL_TEXT = _types.OPTIONAL_TEXT
OPTIONAL_INT32 = _types.OPTIONAL_INT32
OPTIONAL_INT64 = _types.OPTIONAL_INT64
OPTIONAL_FLOAT32 = _types.OPTIONAL_FLOAT32
OPTIONAL_FLOAT64 = _types.OPTIONAL_FLOAT64
OPTIONAL_WEAK_FLOAT = _types.OPTIONAL_WEAK_FLOAT
OPTIONAL_SCALAR_SHAPE = _types.OPTIONAL_SCALAR_SHAPE

DENSE_ARRAY_UNIT = _types.DENSE_ARRAY_UNIT
DENSE_ARRAY_BOOLEAN = _types.DENSE_ARRAY_BOOLEAN
DENSE_ARRAY_BYTES = _types.DENSE_ARRAY_BYTES
DENSE_ARRAY_TEXT = _types.DENSE_ARRAY_TEXT
DENSE_ARRAY_INT32 = _types.DENSE_ARRAY_INT32
DENSE_ARRAY_INT64 = _types.DENSE_ARRAY_INT64
DENSE_ARRAY_FLOAT32 = _types.DENSE_ARRAY_FLOAT32
DENSE_ARRAY_FLOAT64 = _types.DENSE_ARRAY_FLOAT64
DENSE_ARRAY_WEAK_FLOAT = _types.DENSE_ARRAY_WEAK_FLOAT
DENSE_ARRAY_EDGE = _types.DENSE_ARRAY_EDGE
DENSE_ARRAY_TO_SCALAR_EDGE = _types.DENSE_ARRAY_TO_SCALAR_EDGE
DENSE_ARRAY_SHAPE = _types.DENSE_ARRAY_SHAPE

ARRAY_UNIT = _types.ARRAY_UNIT
ARRAY_BOOLEAN = _types.ARRAY_BOOLEAN
ARRAY_BYTES = _types.ARRAY_BYTES
ARRAY_TEXT = _types.ARRAY_TEXT
ARRAY_INT32 = _types.ARRAY_INT32
ARRAY_INT64 = _types.ARRAY_INT64
ARRAY_FLOAT32 = _types.ARRAY_FLOAT32
ARRAY_FLOAT64 = _types.ARRAY_FLOAT64
ARRAY_WEAK_FLOAT = _types.ARRAY_WEAK_FLOAT
ARRAY_EDGE = _types.ARRAY_EDGE
ARRAY_TO_SCALAR_EDGE = _types.ARRAY_TO_SCALAR_EDGE
ARRAY_SHAPE = _types.ARRAY_SHAPE

## Factory functions

unit = _types.unit
boolean = _types.boolean
bytes_ = _types.bytes_
text = _types.text
int32 = _types.int32
int64 = _types.int64
float32 = _types.float32
float64 = _types.float64
weak_float = _types.weak_float

optional_unit = _types.optional_unit
optional_boolean = _types.optional_boolean
optional_bytes = _types.optional_bytes
optional_text = _types.optional_text
optional_int32 = _types.optional_int32
optional_int64 = _types.optional_int64
optional_float32 = _types.optional_float32
optional_float64 = _types.optional_float64
optional_weak_float = _types.optional_weak_float
missing_unit = _types.missing_unit
present_unit = _types.present_unit
missing = _types.missing
present = _types.present

dense_array_unit = _types.dense_array_unit
dense_array_boolean = _types.dense_array_boolean
dense_array_bytes = _types.dense_array_bytes
dense_array_text = _types.dense_array_text
dense_array_int32 = _types.dense_array_int32
dense_array_int64 = _types.dense_array_int64
dense_array_float32 = _types.dense_array_float32
dense_array_float64 = _types.dense_array_float64
dense_array_weak_float = _types.dense_array_weak_float


array_unit = _types.array_unit
array_boolean = _types.array_boolean
array_bytes = _types.array_bytes
array_text = _types.array_text
array_int32 = _types.array_int32
array_int64 = _types.array_int64
array_float32 = _types.array_float32
array_float64 = _types.array_float64
array_weak_float = _types.array_weak_float

## Utilities

array = _types.array
as_expr = _types.as_expr
as_qvalue = _types.as_qvalue
dense_array = _types.dense_array
eval_ = _types.eval_
is_array_qtype = _types.is_array_qtype
is_dense_array_qtype = _types.is_dense_array_qtype
is_dict_qtype = _types.is_dict_qtype
is_namedtuple_qtype = _types.is_namedtuple_qtype
is_optional_qtype = _types.is_optional_qtype
is_scalar_qtype = _types.is_scalar_qtype
is_tuple_qtype = _types.is_tuple_qtype
literal = _types.literal
make_array_qtype = _types.make_array_qtype
make_dense_array_qtype = _types.make_dense_array_qtype
make_namedtuple_qtype = _types.make_namedtuple_qtype
make_optional_qtype = _types.make_optional_qtype
make_tuple_qtype = _types.make_tuple_qtype
namedtuple = _types.namedtuple
tuple_ = _types.tuple_

LambdaOperator = _types.LambdaOperator
OverloadedOperator = _types.OverloadedOperator

#
# EXPR
#

LeafContainer = _expr.LeafContainer
PlaceholderContainer = _expr.PlaceholderContainer
OperatorsContainer = _expr.OperatorsContainer
unsafe_operators_container = _expr.unsafe_operators_container
L = LeafContainer()
P = PlaceholderContainer()
M = OperatorsContainer()


#
# Public submodules
#
abc = _abc
optools = _optools
s11n = _s11n
testing = _testing
types = _types

# Functions that collide with Python builtins:
bytes = bytes_  # pylint: disable=redefined-builtin
eval = eval_  # pylint: disable=redefined-builtin
tuple = tuple_  # pylint: disable=redefined-builtin
