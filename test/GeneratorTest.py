import unittest

from Generator import InstanceGenerator
from InputOutput import Params, OutputWriter


class GeneratorTest(unittest.TestCase):
    SAMPLE_CONFIG = '../sample_config.json'
    DB_PATH = '../db/tp3s.db'
    OUT_PATH = './result.tp3s'

    def test_inst_gen(self):
        generator = InstanceGenerator(GeneratorTest.SAMPLE_CONFIG,
                                      GeneratorTest.DB_PATH)
        inst = generator.gen_instance()
        self.assertEqual(len(inst.tests), Params.NUM_TEST)
        self.assertEqual(len(inst.vehicles), Params.NUM_VEHICLE)
        self.assertEqual(len(inst.rehit), Params.NUM_TEST*Params.NUM_TEST)

    def test_output(self):
        generator = InstanceGenerator(GeneratorTest.SAMPLE_CONFIG,
                                      GeneratorTest.DB_PATH)
        inst = generator.gen_instance()
        out = OutputWriter(GeneratorTest.OUT_PATH)
        out.write_instance(inst)


if __name__ == '__main__':
    unittest.main()
