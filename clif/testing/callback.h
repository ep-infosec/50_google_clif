/*
 * Copyright 2017 Google Inc.
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
#ifndef CLIF_TESTING_CALLBACK_H_
#define CLIF_TESTING_CALLBACK_H_

#include <functional>
#include <string>
#include <vector>

namespace cliff {
namespace testing {
typedef std::function<int(const std::vector<int>&, std::vector<int>*)>
    OldCallback;

typedef std::function<std::pair<int, std::vector<int>>(const std::vector<int>&)>
    NewCallback;

}  // namespace testing
}  // namespace cliff

// test for wrapping function with nonconst nonref function parameter
inline std::vector<int> FunctionNewStyleCallbackNonConstRef(
    const std::vector<int>& input, cliff::testing::NewCallback callback) {
  auto output = callback(input);
  return output.second;
}

// test for wrapping function with const reference function parameter
inline std::vector<int> FunctionNewStyleCallbackConstRef(
    const std::vector<int>& input,
    const cliff::testing::NewCallback& callback) {
  auto output = callback(input);
  return output.second;
}

// Intentionally create an overload for the function above, so that a lambda
// expression is generated.
inline std::vector<int> FunctionNewStyleCallbackConstRef(
    const std::vector<int>& input,
    const cliff::testing::NewCallback& callback, int) {
  auto output = callback(input);
  return output.second;
}

inline std::vector<int> Function(const std::vector<int>& input,
                          cliff::testing::OldCallback callback) {
  std::vector<int> output;
  callback(input, &output);
  return output;
}

inline std::function<int(int)> FunctionWithCallableReturn(
    std::function<int(int)> callback) {
  return callback;
}

inline std::function<int(int)> FunctionWithCallableReturn(
    std::function<int(int)> callback, int) {
  return callback;
}

inline void StringCallback(std::function<void(std::string)> f) { f("foo"); }

struct SelfCallback {
  explicit SelfCallback(std::function<void(SelfCallback*)>) {}
};

inline std::string LambdaCallback(std::function<std::string()> f) {
  return f();
}

#endif  // CLIF_TESTING_CALLBACK_H_
