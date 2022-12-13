"""DO NOT TOUCH. Generated by slot_extractor."""
# from ../../python_runtime/v3_6/Include/object.h

#
# Copyright 2017 Google Inc.
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

PyNumberMethods = [
    'nb_add',
    'nb_subtract',
    'nb_multiply',
    'nb_remainder',
    'nb_divmod',
    'nb_power',
    'nb_negative',
    'nb_positive',
    'nb_absolute',
    'nb_bool',
    'nb_invert',
    'nb_lshift',
    'nb_rshift',
    'nb_and',
    'nb_xor',
    'nb_or',
    'nb_int',
    'nb_reserved',
    'nb_float',
    'nb_inplace_add',
    'nb_inplace_subtract',
    'nb_inplace_multiply',
    'nb_inplace_remainder',
    'nb_inplace_power',
    'nb_inplace_lshift',
    'nb_inplace_rshift',
    'nb_inplace_and',
    'nb_inplace_xor',
    'nb_inplace_or',
    'nb_floor_divide',
    'nb_true_divide',
    'nb_inplace_floor_divide',
    'nb_inplace_true_divide',
    'nb_index',
    'nb_matrix_multiply',
    'nb_inplace_matrix_multiply',
]
PySequenceMethods = [
    'sq_length',
    'sq_concat',
    'sq_repeat',
    'sq_item',
    'was_sq_slice',
    'sq_ass_item',
    'was_sq_ass_slice',
    'sq_contains',
    'sq_inplace_concat',
    'sq_inplace_repeat',
]
PyMappingMethods = [
    'mp_length',
    'mp_subscript',
    'mp_ass_subscript',
]
PyTypeObject = [
    'tp_name',
    'tp_basicsize',
    'tp_itemsize',
    'tp_dealloc',
    'tp_print',
    'tp_getattr',
    'tp_setattr',
    'tp_as_async',
    'tp_repr',
    'tp_as_number',
    'tp_as_sequence',
    'tp_as_mapping',
    'tp_hash',
    'tp_call',
    'tp_str',
    'tp_getattro',
    'tp_setattro',
    'tp_as_buffer',
    'tp_flags',
    'tp_doc',
    'tp_traverse',
    'tp_clear',
    'tp_richcompare',
    'tp_weaklistoffset',
    'tp_iter',
    'tp_iternext',
    'tp_methods',
    'tp_members',
    'tp_getset',
    'tp_base',
    'tp_dict',
    'tp_descr_get',
    'tp_descr_set',
    'tp_dictoffset',
    'tp_init',
    'tp_alloc',
    'tp_new',
    'tp_free',
    'tp_is_gc',
    'tp_bases',
    'tp_mro',
    'tp_cache',
    'tp_subclasses',
    'tp_weaklist',
    'tp_del',
    'tp_version_tag',
    'tp_finalize',
]
SIGNATURES = {  # c_slot_name: func_type
    'nb_add': ('O', 'O'),
    'nb_subtract': ('O', 'O'),
    'nb_multiply': ('O', 'O'),
    'nb_remainder': ('O', 'O'),
    'nb_divmod': ('O', 'O'),
    'nb_power': ('O', 'OO'),
    'nb_negative': ('O', ''),
    'nb_positive': ('O', ''),
    'nb_absolute': ('O', ''),
    'nb_bool': ('int', ''),
    'nb_invert': ('O', ''),
    'nb_lshift': ('O', 'O'),
    'nb_rshift': ('O', 'O'),
    'nb_and': ('O', 'O'),
    'nb_xor': ('O', 'O'),
    'nb_or': ('O', 'O'),
    'nb_int': ('O', ''),
    'nb_float': ('O', ''),
    'nb_inplace_add': ('O', 'O'),
    'nb_inplace_subtract': ('O', 'O'),
    'nb_inplace_multiply': ('O', 'O'),
    'nb_inplace_remainder': ('O', 'O'),
    'nb_inplace_power': ('O', 'OO'),
    'nb_inplace_lshift': ('O', 'O'),
    'nb_inplace_rshift': ('O', 'O'),
    'nb_inplace_and': ('O', 'O'),
    'nb_inplace_xor': ('O', 'O'),
    'nb_inplace_or': ('O', 'O'),
    'nb_floor_divide': ('O', 'O'),
    'nb_true_divide': ('O', 'O'),
    'nb_inplace_floor_divide': ('O', 'O'),
    'nb_inplace_true_divide': ('O', 'O'),
    'nb_index': ('O', ''),
    'nb_matrix_multiply': ('O', 'O'),
    'nb_inplace_matrix_multiply': ('O', 'O'),
    'sq_length': ('Py_ssize_t', ''),
    'sq_concat': ('O', 'O'),
    'sq_repeat': ('O', ['Py_ssize_t']),
    'sq_item': ('int', ['Py_ssize_t']),
    'sq_ass_item': ('O', ['Py_ssize_t', 'O']),
    'sq_contains': ('int', 'O'),
    'sq_inplace_concat': ('O', 'O'),
    'sq_inplace_repeat': ('O', ['Py_ssize_t']),
    'mp_length': ('Py_ssize_t', ''),
    'mp_subscript': ('O', 'O'),
    'tp_repr': ('O', ''),
    'tp_hash': ('long', ''),
    'tp_call': ('O', 'OO'),
    'tp_str': ('O', ''),
    'tp_getattro': ('O', 'O'),
    'tp_setattro': ('O', 'OO'),
    'tp_clear': ('int', ''),
    'tp_iter': ('O', ''),
    'tp_iternext': ('O', ''),
    'tp_is_gc': ('int', ''),
}
