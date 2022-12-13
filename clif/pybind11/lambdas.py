# Copyright 2021 Google LLC
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
"""Generates C++ lambda functions inside pybind11 bindings code."""

from typing import Generator, List, Optional, Set

from clif.protos import ast_pb2
from clif.pybind11 import function_lib
from clif.pybind11 import utils

I = utils.I

_NEEDS_INDEX_CHECK_METHODS = frozenset([
    '__getitem__#', '__setitem__#', '__delitem__#'
])


def generate_lambda(
    module_name: str, func_decl: ast_pb2.FuncDecl,
    codegen_info: utils.CodeGenInfo,
    class_decl: Optional[ast_pb2.ClassDecl] = None,
    first_unknown_default_index: int = -1,
    first_unknown_default_param: Optional[ast_pb2.ParamDecl] = None
) -> Generator[str, None, None]:
  """Entry point for generation of lambda functions in pybind11."""
  params_list = []
  for i, param in enumerate(func_decl.params):
    params_list.append(
        function_lib.Parameter(param, f'arg{i}', codegen_info))
  params_with_type = _generate_lambda_params_with_types(
      func_decl, params_list, class_decl)
  # @sequential, @context_manager
  func_name = func_decl.name.native.rstrip('#').rstrip('@')
  yield (f'{module_name}.{function_lib.generate_def(func_decl)}'
         f'("{func_name}", []({params_with_type}) {{')

  # Only throw ValueError when there are parameters with unknown default value
  # and users do not provide values for it.
  if (first_unknown_default_index != -1 and first_unknown_default_param and
      len(params_list) > first_unknown_default_index):
    yield I + (f'throw py::value_error("{func_decl.name.native}() argument '
               f'{first_unknown_default_param.name.native} needs a non-default '
               'value");')
  else:
    yield from _generate_lambda_body(
        func_decl, params_list, codegen_info, class_decl)
  is_member_function = (class_decl is not None)
  function_suffix = function_lib.generate_function_suffixes(
      func_decl, release_gil=False, is_member_function=is_member_function,
      first_unknown_default_index=first_unknown_default_index)
  yield f'}}, {function_suffix}'


def needs_lambda(
    func_decl: ast_pb2.FuncDecl, codegen_info: utils.CodeGenInfo,
    class_decl: Optional[ast_pb2.ClassDecl] = None) -> bool:
  if class_decl and _is_inherited_method(class_decl, func_decl):
    return True
  return (bool(func_decl.postproc) or
          func_decl.is_overloaded or
          _func_is_extend_static_method(func_decl, class_decl) or
          function_lib.func_has_vector_param(func_decl) or
          function_lib.func_has_set_param(func_decl) or
          _func_is_context_manager(func_decl) or
          _func_needs_index_check(func_decl) or
          _func_has_capsule_params(func_decl, codegen_info.capsule_types) or
          _func_needs_implicit_conversion(func_decl) or
          _func_has_pointer_params(func_decl) or
          function_lib.func_has_py_object_params(func_decl) or
          _func_has_status_params(func_decl, codegen_info.requires_status) or
          _func_has_status_callback(func_decl, codegen_info.requires_status) or
          func_decl.cpp_num_params != len(func_decl.params))


def generate_check_nullptr(
    func_decl: ast_pb2.FuncDecl, param_name: str) -> Generator[str, None, None]:
  yield I + f'if ({param_name} == nullptr) {{'
  yield I + I + (f'throw py::type_error("{func_decl.name.native}() '
                 f'argument {param_name} is not valid.");')
  yield I +'}'


def generate_cpp_function_return_post_process(
    func_decl: ast_pb2.FuncDecl, function_call_returns: str, self_param: str,
) -> Generator[str, None, None]:
  """Generates post process for returns values of cpp functions."""
  if func_decl.postproc == '->self':
    yield I + 'return self;'
  elif func_decl.name.native == '__enter__@':
    yield I + f'return py::cast({self_param}).release();'
  elif func_decl.name.native == '__exit__@':
    yield I + 'return py::none();'
  elif func_decl.postproc:
    assert '.' in func_decl.postproc
    module_name, method_name = func_decl.postproc.rsplit('.', maxsplit=1)
    # TODO: Port or reuse `clif::ImportFQName`.
    yield I + f'auto mod = py::module_::import("{module_name}");'
    yield I + ('py::object result_ = '
               f'mod.attr("{method_name}")({function_call_returns});')
    yield I + 'return result_;'
  elif function_call_returns:
    if len(func_decl.returns) > 1:
      yield I + f'return std::make_tuple({function_call_returns});'
    else:
      yield I + f'return {function_call_returns};'


def _generate_lambda_body(
    func_decl: ast_pb2.FuncDecl,
    params: List[function_lib.Parameter], codegen_info: utils.CodeGenInfo,
    class_decl: Optional[ast_pb2.ClassDecl] = None,
) -> Generator[str, None, None]:
  """Generates body of lambda expressions."""
  function_call = generate_function_call(func_decl, class_decl)
  params_str = ', '.join([p.function_argument for p in params])
  function_call_params = generate_function_call_params(func_decl, params_str)
  function_call_returns = generate_function_call_returns(
      func_decl, codegen_info.capsule_types)

  cpp_void_return = func_decl.cpp_void_return or not func_decl.returns

  # Generates void pointer check for parameters that are converted from non
  # pointers by code generator.
  for p in params:
    if p.check_nullptr:
      yield from generate_check_nullptr(func_decl, p.gen_name)
    yield from p.preprocess()

  if func_decl.name.native in _NEEDS_INDEX_CHECK_METHODS and class_decl:
    start_idx = 1 if func_decl.is_extend_method else 0
    assert len(params) >= start_idx + 1, ('sequential methods need at least '
                                          'one param')
    index = params[start_idx]
    self_param = (
        params[0].gen_name if func_decl.is_extend_method else 'self')
    yield I + (f'py::object length_function_ = py::cast({self_param})'
               '.attr("__len__");')
    yield I + 'if (length_function_.is_none()) {'
    yield I + I + (f'throw py::attribute_error("class {class_decl.name.native} '
                   f'defined {func_decl.name.native}, but does not define '
                   '`__len__` function.");')
    yield I +'}'
    yield I + (f'Py_ssize_t {index.gen_name}_ = ::clif::item_index('
               f'{index.gen_name}, py::cast<int>(length_function_()));')
    yield I + (f'if ({index.gen_name}_ < 0) {{')
    yield I + I + 'throw py::index_error("index out of range.");'
    yield I +'}'
    yield I + f'{index.gen_name} = {index.gen_name}_;'

  # Generates declarations of return values
  for i, r in enumerate(func_decl.returns):
    if i or cpp_void_return:
      yield I + f'{r.type.cpp_type} ret{i}{{}};'

  if not function_lib.func_keeps_gil(func_decl):
    yield I + 'PyThreadState* _save;'
    yield I + 'Py_UNBLOCK_THREADS'

  # Generates call to the wrapped function
  cpp_void_return = func_decl.cpp_void_return or not func_decl.returns
  if not cpp_void_return:
    ret0 = func_decl.returns[0]
    if not ret0.type.cpp_type:
      callback_cpp_type = function_lib.generate_callback_signature(ret0)
      yield I + (f'{callback_cpp_type} ret0 = '
                 f'{function_call}({function_call_params});')
    else:
      yield I + (f'{ret0.type.cpp_type} ret0 = '
                 f'{function_call}({function_call_params});')
  else:
    yield I + f'{function_call}({function_call_params});'

  if not function_lib.func_keeps_gil(func_decl):
    yield I + 'Py_BLOCK_THREADS'

  # Generates returns of the lambda expression
  self_param = 'self'
  if func_decl.is_extend_method and len(params):
    self_param = params[0].gen_name
  yield from generate_cpp_function_return_post_process(
      func_decl, function_call_returns, self_param)


def generate_function_call_params(
    func_decl: ast_pb2.FuncDecl, params_str: str) -> str:
  """Generates the parameters of function calls in lambda expressions."""
  # Ignore the return value of the function itself when generating pointer
  # parameters.
  stard_idx = 0
  if not func_decl.cpp_void_return and len(func_decl.returns):
    stard_idx = 1
  pointer_params_str = ', '.join(
      [f'&ret{i}' for i in range(stard_idx, len(func_decl.returns))])

  if params_str and pointer_params_str:
    return f'{params_str}, {pointer_params_str}'
  elif pointer_params_str:
    return pointer_params_str
  else:
    return params_str


def generate_function_call_returns(
    func_decl: ast_pb2.FuncDecl, capsule_types: Set[str],
    requires_status: bool = True) -> str:
  """Generates return values of cpp function."""
  all_returns_list = []
  for i, r in enumerate(func_decl.returns):
    if function_lib.is_bytes_type(r.type):
      all_returns_list.append(
          f'py::cast(ret{i}, py::return_value_policy::_return_as_bytes)')
    elif r.type.lang_type in capsule_types:
      all_returns_list.append(
          f'clif::CapsuleWrapper<{r.type.cpp_type}>(ret{i})')
    elif function_lib.is_status_param(r, requires_status):
      status_type = function_lib.generate_status_type(func_decl, r)
      all_returns_list.append(f'py::cast(({status_type})(std::move(ret{i})), '
                              'py::return_value_policy::_clif_automatic)')
    # When the lambda expression returns multiple values, we construct an
    # `std::tuple` with those return values. For uncopyable return values, we
    # need `std::move` when constructing the `std::tuple`.
    elif (len(func_decl.returns) > 1 and
          ('std::unique_ptr' in r.cpp_exact_type or not r.type.cpp_copyable)):
      all_returns_list.append(f'std::move(ret{i})')
    else:
      all_returns_list.append(f'ret{i}')
  return ', '.join(all_returns_list)


def _generate_lambda_params_with_types(
    func_decl: ast_pb2.FuncDecl,
    params: List[function_lib.Parameter],
    class_decl: Optional[ast_pb2.ClassDecl] = None) -> str:
  """Generates parameters and types in the signatures of lambda expressions."""
  params_list = [f'{p.cpp_type} {p.gen_name}' for p in params]
  if (class_decl and not func_decl.classmethod and
      not func_decl.is_extend_method and not func_decl.cpp_opfunction):
    params_list = [f'{class_decl.name.cpp_name} &self'] + params_list
  if func_decl.name.native == '__exit__@' and class_decl:
    params_list.append('py::args')
  return ', '.join(params_list)


def generate_function_call(
    func_decl: ast_pb2.FuncDecl,
    class_decl: Optional[ast_pb2.ClassDecl] = None) -> str:
  """Generates the function call underneath the lambda expression."""
  if (func_decl.classmethod or not class_decl or func_decl.is_extend_method or
      func_decl.cpp_opfunction):
    return func_decl.name.cpp_name
  else:
    method_name = func_decl.name.cpp_name.split('::')[-1]
    return f'self.{method_name}'


def _func_is_extend_static_method(
    func_decl: ast_pb2.FuncDecl,
    class_decl: Optional[ast_pb2.ClassDecl] = None) -> bool:
  return class_decl and func_decl.is_extend_method and func_decl.classmethod


def _func_has_pointer_params(func_decl: ast_pb2.FuncDecl) -> bool:
  num_returns = len(func_decl.returns)
  return num_returns >= 2 or (num_returns == 1 and func_decl.cpp_void_return)


def _func_has_status_params(func_decl: ast_pb2.FuncDecl,
                            requires_status: bool) -> bool:
  for p in func_decl.params:
    if function_lib.is_status_param(p, requires_status):
      return True
  for r in func_decl.returns:
    if function_lib.is_status_param(r, requires_status):
      return True
  return False


def _func_has_status_callback(func_decl: ast_pb2.FuncDecl,
                              requires_status: bool) -> bool:
  for r in func_decl.returns:
    if function_lib.is_status_callback(r, requires_status):
      return True
  return False


def _func_has_capsule_params(
    func_decl: ast_pb2.FuncDecl, capsule_types: Set[str]) -> bool:
  for p in func_decl.params:
    if p.type.lang_type in capsule_types:
      return True
  for r in func_decl.returns:
    if r.type.lang_type in capsule_types:
      return True
  return False


def _func_is_context_manager(func_decl: ast_pb2.FuncDecl) -> bool:
  return func_decl.name.native in ('__enter__@', '__exit__@')


def _func_needs_index_check(func_decl: ast_pb2.FuncDecl) -> bool:
  return func_decl.name.native in _NEEDS_INDEX_CHECK_METHODS


def _is_inherited_method(class_decl: ast_pb2.ClassDecl,
                         func_decl: ast_pb2.FuncDecl) -> bool:
  if class_decl.cpp_bases and not func_decl.is_extend_method:
    namespaces = func_decl.name.cpp_name.split('::')
    if (len(namespaces) > 1 and
        namespaces[-2] != class_decl.name.cpp_name.strip(':')):
      return True
  return False


def _func_needs_implicit_conversion(func_decl: ast_pb2.FuncDecl) -> bool:
  """Check if a function contains an implicitly converted parameter."""
  for param in func_decl.params:
    if (_extract_bare_type(param.cpp_exact_type) !=
        _extract_bare_type(param.type.cpp_type) and
        param.type.cpp_toptr_conversion and
        param.type.cpp_touniqptr_conversion):
      return True
  return False


def _extract_bare_type(cpp_name: str) -> str:
  # This helper function is not general and only meant
  # to be used in _func_needs_implicit_conversion.
  t = cpp_name.split(' ')
  if t[0] == 'const':
    t = t[1:]
  if t[-1] in {'&', '*'}:  # Minimum viable approach. To be refined as needed.
    t = t[:-1]
  return ' '.join(t)


def generate_return_value_cpp_type(
    func_decl: ast_pb2.FuncDecl, codegen_info: utils.CodeGenInfo) -> str:
  """Generates type for the return value of the C++ function."""
  ret0 = func_decl.returns[0]
  if function_lib.is_status_param(ret0, codegen_info.requires_status):
    return function_lib.generate_status_type(func_decl, ret0)
  elif function_lib.is_status_callback(ret0, codegen_info.requires_status):
    return function_lib.generate_status_type(func_decl,
                                             ret0.type.callable.returns[0])
  elif not ret0.type.cpp_type:
    return function_lib.generate_callback_signature(ret0)
  else:
    return ret0.type.cpp_type
