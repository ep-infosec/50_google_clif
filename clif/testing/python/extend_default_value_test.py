# Copyright 2020 Google LLC
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

from absl.testing import absltest

from clif.testing.python import extend_default_value


class ExtendDefaultValueTest(absltest.TestCase):

  def test_only_default_values(self):
    v1 = 10
    v2 = 100
    expected_value = v1 + v2
    abc = extend_default_value.Abc(v1)
    self.assertEqual(abc.get_value(), v1)
    abc.sum_and_set_values()
    self.assertEqual(abc.get_value(), expected_value)

  def test_one_default_value(self):
    v1 = 123
    v2 = 100
    expected_value = v1 + v2
    abc = extend_default_value.Abc(v1)
    self.assertEqual(abc.get_value(), v1)
    abc.sum_and_set_values(v1=v1)
    self.assertEqual(abc.get_value(), expected_value)

  def test_not_using_default_value(self):
    v1 = 123
    v2 = 456
    expected_value = v1 + v2
    abc = extend_default_value.Abc(v1)
    self.assertEqual(abc.get_value(), v1)
    abc.sum_and_set_values(v1=v1, v2=v2)
    self.assertEqual(abc.get_value(), expected_value)

  def test_pass_unique_ptr(self):
    abc = extend_default_value.Abc(64)
    kv = {9: 3, 7: 5}

    f = abc.pass_unique_ptr_kv
    res = f()
    self.assertEqual(res, 64 + 46 + 2)
    res = f(kv)
    self.assertEqual(res, 64 + 46 + 9 * 10 + 3 + 7 * 10 + 5 + 2)

    f = abc.pass_unique_ptr_kv_v
    res = f()
    self.assertEqual(res, 64 + 46 + 8)
    res = f(kv)
    self.assertEqual(res, 64 + 46 + 9 * 10 + 3 + 7 * 10 + 5 + 8)
    res = f(kv, 1)
    self.assertEqual(res, 64 + 46 + 9 * 10 + 3 + 7 * 10 + 5 + 1)

    f = abc.pass_unique_ptr_v_kv
    res = f()
    self.assertEqual(res, 64 + 46 + 4)
    res = f(7)
    self.assertEqual(res, 64 + 46 + 7)
    res = f(7, kv)
    self.assertEqual(res, 64 + 46 + 9 * 10 + 3 + 7 * 10 + 5 + 7)

    f = abc.pass_unique_ptr_v_kv_w
    res = f()
    self.assertEqual(res, 64 + 46 + 5 * 100 + 9)
    res = f(7)
    self.assertEqual(res, 64 + 46 + 7 * 100 + 9)
    res = f(7, kv)
    self.assertEqual(res, 64 + 46 + 9 * 10 + 3 + 7 * 10 + 5 + 7 * 100 + 9)
    res = f(7, kv, 8)
    self.assertEqual(res, 64 + 46 + 9 * 10 + 3 + 7 * 10 + 5 + 7 * 100 + 8)

  def test_default_value_in_constructor(self):
    expected_value = 10
    obj = extend_default_value.DefaultValueInConstructor()
    self.assertEqual(obj.value, expected_value)
    obj = extend_default_value.DefaultValueInConstructor(123)
    self.assertEqual(obj.value, 123)

  def test_nested_default_value(self):
    obj = extend_default_value.TestNestedDefaultValue.Inner(6)
    self.assertEqual(obj.get_value(), 6 + 70 + 800 + 3)
    self.assertEqual(obj.get_value(700), 6 + 70 + 700 + 3)


if __name__ == '__main__':
  absltest.main()
