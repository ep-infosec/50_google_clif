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

set(CLIF_PYTHON_DIR "${CMAKE_CURRENT_SOURCE_DIR}/python")

# Set the additional module path to the CLIF CMake utilities and load them.
set(CMAKE_MODULE_PATH
  "${CMAKE_MODULE_PATH}"
  "${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules"
)
include(CLIFUtils)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include_directories(
    ${CLIF_SRC_DIR}
    ${CLIF_BIN_DIR}
)

set(PYCLIF "${CMAKE_CURRENT_SOURCE_DIR}/pyclif.py")
set(PYCLIF_PROTO "${CMAKE_CURRENT_SOURCE_DIR}/python/proto.py")
set(CLIF_MATCHER "${CMAKE_CURRENT_BINARY_DIR}/backend/clif-matcher")

file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/__init__.py"
  "import pkgutil; __path__ = pkgutil.extend_path(__path__, __name__)"
)

add_subdirectory("backend")
add_subdirectory("protos")
add_subdirectory("python")
add_subdirectory("testing")
