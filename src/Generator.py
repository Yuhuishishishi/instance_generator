from collections import defaultdict, namedtuple
from math import ceil
from InputOutput import Params, Vehicle, Info, TestRequest, ConfigReader, GenInfoReader
import random


class Instance(namedtuple('Instance', 'tests, vehicles, rehit')):
    def json_repr(self):
        rehit = defaultdict(dict)
        for first, second in self.rehit:
            rehit[str(first)][str(second)] = self.rehit[first, second]
        return dict(tests=[t._asdict() for t in self.tests],
                    vehicles=[v._asdict() for v in self.vehicles],
                    rehit=rehit)


class InstanceGenerator:
    def __init__(self, config_path, db_path):
        self.config_path = config_path
        self.db_path = db_path

        db_reader = GenInfoReader(self.db_path)
        db_reader.read_db()

    def gen_instance(self):
        # initialize the readers
        config_reader = ConfigReader(self.config_path)
        config_reader.read_config()

        random.seed(1024)

        # generate vehicles according to vehicle rate
        vehicle_remaining = Params.NUM_VEHICLE
        vehicle_list = []
        curr_day = 0
        vid = 0
        while vehicle_remaining > 0:
            for i in range(0, min(vehicle_remaining, Params.VEHICLE_RATE)):
                vehicle_list.append(Vehicle(vehicle_id=vid,
                                            release=curr_day))
                vid += 1
            curr_day += 5
            vehicle_remaining -= Params.VEHICLE_RATE

        # generate the deadlines
        # deadlines: MIN, FULL, LIVE DEPLOY START, LIVE DEPLOY END
        # average duration for tests
        total_dur = 0
        total_time_category = 0
        for time in Info.MODE_TIMING.itervalues():
            total_dur += sum(map(lambda x: x.prep + x.tat + x.analysis, time))
            total_time_category += len(time)
        avg_dur = float(total_dur) / total_time_category
        # standard deviation = 1 week
        min_deadline = ceil(random.gauss(Params.WINDOW_LENGTH * avg_dur, 5))
        full_deadline = min_deadline + ceil(random.gauss(Params.WINDOW_LENGTH * avg_dur, 5))
        live_start = full_deadline + 4 * 5
        live_deadline = live_start + ceil(random.gauss(Params.WINDOW_LENGTH * avg_dur, 5))
        deadline_map = {0: min_deadline, 1: full_deadline, 2: live_deadline, 3: live_start}

        # generate the tests
        test_list = []
        sub_id_sample = []
        sub_id_to_mode = defaultdict(list)
        map(lambda (k, val): sub_id_sample.extend([k] * val), Info.SUB_CAT_FREQ.iteritems())
        for _, v in Info.TEST_MODE.iteritems():
            sub_id_to_mode[v.sub_id].append(v)

        default_timing = None
        for l in Info.MODE_TIMING.values():
            if l:
                default_timing = l[:]
                break

        for i in range(0, Params.NUM_TEST):
            # sample the sub_id
            sub_id = random.choice(sub_id_sample)
            # sample the test mode
            mode = random.choice(sub_id_to_mode[sub_id])
            # sample the timing
            timing_list = Info.MODE_TIMING[mode.id_]
            if not timing_list:
                timing_list = default_timing

            timing = random.choice(timing_list)
            # sample the deadline
            deadline_id = random.randint(0, 2)
            if deadline_id < 2:
                release = 0
                deadline = deadline_map[deadline_id]
            else:
                release = deadline_map[3]
                deadline = deadline_map[2]
            # create the test
            test = TestRequest(test_id=i,
                               release=int(release),
                               deadline=int(deadline),
                               prep=timing.prep,
                               tat=timing.tat,
                               analysis=timing.analysis,
                               dur=timing.prep + timing.tat + timing.analysis,
                               rehit_id=mode.rehit_id)
            test_list.append(test)

        # construct the rehit matrix
        print Params.COMP_DENSE
        rehit = {}
        for t1 in test_list:
            tid1 = t1.test_id
            for t2 in test_list:
                tid2 = t2.test_id
                if tid1 == tid2:
                    rehit[tid1, tid2] = False
                else:
                    # simulate
                    rnd = random.random()
                    if rnd > Params.COMP_DENSE:
                        rehit[tid1, tid2] = True
                    else:
                        rehit[tid1,tid2] = False
                    # rehit[tid1, tid2] = Info.COMP_MAT[t1.rehit_id, t2.rehit_id]

        # create the instance
        inst = Instance(tests=test_list,
                        vehicles=vehicle_list,
                        rehit=rehit)
        return inst
