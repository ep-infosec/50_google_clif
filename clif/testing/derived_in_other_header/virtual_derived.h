/*
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef CLIF_TESTING_DERIVED_IN_OTHER_HEADER_VIRTUAL_DERIVED_H_
#define CLIF_TESTING_DERIVED_IN_OTHER_HEADER_VIRTUAL_DERIVED_H_

#include <iostream>

#include "clif/testing/derived_in_other_header/virtual_base.h"

namespace clif_testing {
namespace derived_in_other_header {

class VirtualDerivedEmpty : public VirtualBaseEmpty {
 public:
  // Printing from constructor & destructor for simple external validation.
  VirtualDerivedEmpty() {
    std::cout << std::endl << "VirtualDerivedEmpty+" << std::endl;
  }
  ~VirtualDerivedEmpty() {
    std::cout << std::endl << "VirtualDerivedEmpty-" << std::endl;
  }
  int Get() const override { return 29852452; }
  int BaseGet(const VirtualBaseEmpty& base) { return Get() + base.Get(); }
};

}  // namespace derived_in_other_header
}  // namespace clif_testing

#endif  // CLIF_TESTING_DERIVED_IN_OTHER_HEADER_VIRTUAL_DERIVED_H_
