import unittest
from InputOutput import ConfigReader, Params, Info, GenInfoReader


class ConfigReaderTest(unittest.TestCase):
    SAMPLE_CONFIG = '../sample_config.json'

    def test_something(self):
        config_reader = ConfigReader(ConfigReaderTest.SAMPLE_CONFIG)
        config_reader.read_config()
        self.assertEqual(Params.NUM_TEST, 40)
        self.assertEqual(Params.NUM_VEHICLE, 20)
        self.assertEqual(Params.VEHICLE_RATE, 20)
        self.assertEqual(Params.COMP_DENSE, 1)
        self.assertEqual(Params.WINDOW_LENGTH, 2.0)
        self.assertEqual(Params.COMP_FACTOR, 1.0)
        self.assertSequenceEqual(Params.SEED_PROG, [33, 34, 35])


class GeneralInfoReaderTest(unittest.TestCase):
    DB_PATH = '../db/tp3s.db'

    def test_info_reader(self):
        reader = GenInfoReader(GeneralInfoReaderTest.DB_PATH)
        reader.read_db()
        self.assertEqual(124, len(Info.TEST_MODE))
        self.assertEqual(32 * 32, len(Info.COMP_MAT))
        self.assertEqual(len(Info.MODE_TIMING), 124)
        self.assertEqual(14, len(Info.SUB_CAT_FREQ))


if __name__ == '__main__':
    unittest.main()
