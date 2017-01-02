import unittest

from InstanceCombiner import combine_instances


class MyTestCase(unittest.TestCase):
    def test_combine_two_instances(self):
        fat_json = combine_instances(s1=100, s0=0)
        print fat_json


if __name__ == '__main__':
    unittest.main()
