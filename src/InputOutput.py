import json
import pandas as pd
import sqlite3
from collections import namedtuple, defaultdict

SafetyMode = namedtuple('SafetyMode', 'id_, sub_id, rehit_id, speed')
TimingCategory = namedtuple('TimingCategory', 'prep, tat, analysis')


class Params:
    NUM_TEST = 0
    NUM_VEHICLE = 0
    VEHICLE_RATE = 0
    COMP_DENSE = 0  # 0 - SPARSE, 1 - NORMAL, 2 - DENSE
    WINDOW_LENGTH = 1  # 1 times the average duration
    COMP_FACTOR = 0.0  # probability a compatibility will fail
    SEED_PROG = [0, ]  # seed program to use in sampling
    SAFETY_LIB = 0


class Info:
    TEST_MODE = {}
    COMP_MAT = {}
    MODE_TIMING = defaultdict(list)
    SUB_CAT_FREQ = {}


class ConfigReader:
    def __init__(self, config_path):
        self.config_path = config_path

    def read_config(self):
        with open(self.config_path, 'rb') as config_file:
            data = json.load(config_file)

            # parse the config file
            Params.NUM_TEST = data['num_test']
            Params.NUM_VEHICLE = data['num_vehicle']
            Params.VEHICLE_RATE = data['vehicle_rate']
            Params.COMP_DENSE = data['comp_dense']
            Params.WINDOW_LENGTH = data['window_length']
            Params.COMP_FACTOR = data['comp_factor']
            Params.SEED_PROG = data['seed_prog']
            Params.SAFETY_LIB = data['safety_lib']


class GenInfoReader:
    def __init__(self, db_path):
        self.db_path = db_path

    def read_db(self):
        conn = sqlite3.connect(self.db_path)

        # safety mode
        q = """SELECT * FROM SafetyTest
        JOIN Subcategory
        ON subcategoryID=Subcategory.ID
        JOIN RehitCategory
        ON rehitCategoryId=RehitCategory.id
        JOIN RehitCategoryPositioning
        ON rehitCategoryPositioningId=RehitCategoryPositioning.id"""
        df_safety_mode = pd.read_sql_query(q, conn)
        modes = map(lambda x: SafetyMode(id_=x[0],
                                         sub_id=x[1]['subcategoryID'],
                                         rehit_id=x[1]['rehitCategoryId'],
                                         speed=x[1]['min_kph']),
                    df_safety_mode.iterrows())
        for m in modes:
            Info.TEST_MODE[m.id_] = m

        # compatibility rules
        q = """
        SELECT * FROM RehitRules WHERE libraryId=?
        """
        q2 = """
        SELECT * FROM RehitRules
        """
        if Params.SAFETY_LIB > 0:
            df_comp = pd.read_sql_query(q, conn, params=(Params.SAFETY_LIB,))
        else:
            df_comp = pd.read_sql_query(q2, conn)

        def max_cutoff(rehitid1, rehitid2):
            return df_comp[
                (df_comp['rehitCategoryId1'] == rehitid1) & (df_comp['rehitCategoryId2'] == rehitid2)] \
                .speedCutoff.max()

        def is_comp(rehitid1, rehitid2):
            cutoff = max_cutoff(rehitid1, rehitid2)
            if Info.TEST_MODE[rehitid1].speed <= cutoff:
                return True
            return False

        rehitid_list = df_safety_mode.rehitCategoryId.unique()
        for id1 in rehitid_list:
            for id2 in rehitid_list:
                Info.COMP_MAT[id1, id2] = is_comp(id1, id2)

        # timing categories
        q = """
        SELECT * FROM SafetyTestTiming
        JOIN TimingCategory ON SafetyTestTiming.timingCategoryId=TimingCategory.id
        ORDER BY safetyTestId
        """
        df_timing = pd.read_sql_query(q, conn)
        for _, d in df_timing.iterrows():
            safety_id = d['safetyTestId']
            prep = d['prep'] + d['rework'] + d['parts'] + d['vev']
            tat = d['tat']
            analysis = d['analysis'] + d['nonVev']
            Info.MODE_TIMING[safety_id].append(TimingCategory(
                prep=prep, tat=tat, analysis=analysis
            ))

        # distribution of tests
        q = """
        SELECT subcategoryID, count(1) AS cnt
        FROM ControlModelTestPairRequirements
        JOIN ProgramTests ON programTestId=ProgramTests.id
        JOIN SafetyTest ON ProgramTests.safetyTestId = SafetyTest.ID
        WHERE ProgramTests.programId IN (33,34,35,36,38,28,29)
        GROUP BY subcategoryID
        """
        df_test = pd.read_sql_query(q, conn)
        for _, d in df_test.iterrows():
            Info.SUB_CAT_FREQ[d['subcategoryID']] = d['cnt']


TestRequest = namedtuple('TestRequest', 'test_id, release, deadline, prep, tat, analysis, dur, rehit_id')
Vehicle = namedtuple('Vehicle', 'vehicle_id, release')


class OutputWriter:
    def __init__(self, output_path):
        self.output_path = output_path

    def write_instance(self, instance):
        with open(self.output_path, 'wb') as out:
            json.dump(instance.json_repr(), out)
