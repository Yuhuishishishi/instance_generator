import json
import os
import shutil

SMALL_PATH = "C:\Users\yuhuishi\PycharmProjects\instance_generator\instance\small"
MODERATE_PATH = "C:\Users\yuhuishi\PycharmProjects\instance_generator\instance\moderate"
LARGE_PATH = "C:\Users\yuhuishi\PycharmProjects\instance_generator\instance\large"


def instance_id_mark():
    # mark the small instance
    mark_instance_in_dir(SMALL_PATH, "s")

    # mark the moderate instance
    mark_instance_in_dir(MODERATE_PATH, "m")

    # mark the large instance
    mark_instance_in_dir(LARGE_PATH, "l")


def mark_instance_in_dir(dir, prefix):
    counter = 0
    files = sorted(os.listdir(dir))
    for f in files:
        if f.endswith(".tp3s") and f.startswith("_"):
            src_path = os.path.join(dir, f)
            new_name = "{prefix}{id_counter}{orig_name}".format(prefix=prefix,
                                                                id_counter=counter,
                                                                orig_name=f)
            dest_path = os.path.join(dir, new_name)
            shutil.move(src_path, dest_path)
            counter += 1


def combine_instances(**inst_time_shift):
    # combine several json into one
    fat_json = []
    for inst_id, time_shift in inst_time_shift.iteritems():
        # search for the json
        inst_json_path = search_for_inst_id(inst_id)
        assert inst_json_path
        with open(inst_json_path, 'rb') as f:
            j = json.load(f)[0]
            # j['inst_id'] = inst_id
            # shift the timing information
            tests = j['tests']
            vehicles = j['vehicles']
            for test in tests:
                release = test['release']
                deadline = test['deadline']
                release += time_shift
                deadline += time_shift
                # prefix the id
                # test["test_id"] = "{inst_id}_{old_id}".format(inst_id=inst_id,
                #                                               old_id=test["test_id"])
                test['deadline'] = deadline
                test['release'] = release
            for vehicle in vehicles:
                release = vehicle['release']
                release += time_shift
                vehicle['release'] = release
            fat_json.append(j)

    return fat_json


def get_horizon_length(inst_json):
    tests = inst_json['tests']
    vehicles = inst_json['vehicles']

    earlist_vehicle_release = min([v['release'] for v in vehicles])
    longest_test_dur = max([t['dur'] for t in tests])
    latest_test_deadline = max([t['deadline'] for t in tests])

    horizon_start = earlist_vehicle_release
    horizon_end = latest_test_deadline

    return horizon_end - horizon_start + longest_test_dur


def search_for_inst_id(inst_id):
    if inst_id.startswith("s"):
        target_dir = SMALL_PATH
    elif inst_id.startswith("m"):
        target_dir = MODERATE_PATH
    else:
        target_dir = LARGE_PATH
    for f in os.listdir(target_dir):
        id_sec = f.split("_")[0]
        if id_sec == inst_id:
            return os.path.join(target_dir, f)
    return


def combine_two_instances(path1, path2, out_path, overlap=1.0):
    created_inst = set()
    files_in_path1 = filter(lambda x: x.endswith('.tp3s'), os.listdir(path1))
    files_in_path2 = filter(lambda x: x.endswith('.tp3s'), os.listdir(path2))

    for f1 in files_in_path1:
        inst_id1 = f1.split("_")[0]
        for f2 in files_in_path2:
            inst_id2 = f2.split("_")[0]
            if f1 == f2:
                continue
            if (inst_id1, inst_id2) in created_inst \
                    or (inst_id2, inst_id1) in created_inst:
                continue
            else:
                created_inst.add((inst_id1, inst_id2))
            # compute the overlap
            inst_json_path = search_for_inst_id(inst_id1)
            with open(inst_json_path, 'rb') as f:
                j = json.load(f)[0]
            inst1_length = get_horizon_length(j)
            inst2_offset = inst1_length * (1 - overlap)

            # combine
            arg = {inst_id1: 0, inst_id2: inst2_offset}
            fat_json = combine_instances(**arg)
            with open(os.path.join(out_path, "{id1}_{id2}_overlap_{overlap}.tp3s".format(id1=inst_id1, id2=inst_id2,
                                                                                         overlap=overlap)), 'wb') as f:
                json.dump(fat_json, f)


def json_wrapper():
    folders = [SMALL_PATH, MODERATE_PATH, LARGE_PATH]
    for folder in folders:
        for f in os.listdir(folder):
            if not f.endswith("tp3s"):
                continue
            inst_id = f.split("_")[0]
            path = os.path.join(folder, f)
            with open(path, 'rb') as fopen:
                data = json.load(fopen)
                data['inst_id'] = inst_id
                wrapped = [data, ]
            with open(path, 'wb') as fopen:
                json.dump(wrapped, fopen)


if __name__ == '__main__':
    small_seed = "C:\Users\yuhuishi\PycharmProjects\instance_generator\instance\multiple\small_seed"
    moderate_seed = "C:\Users\yuhuishi\PycharmProjects\instance_generator\instance\multiple\moderate_seed"
    small_small_out = "C:\Users\yuhuishi\PycharmProjects\instance_generator\instance\multiple\small_small"
    moderate_moderate_out = "C:\Users\yuhuishi\PycharmProjects\instance_generator\instance\multiple\moderate_moderate"
    small_moderate_out = "C:\Users\yuhuishi\PycharmProjects\instance_generator\instance\multiple\small_moderate"
    overlap = [0.25, 0.5, 0.75, 1.0]

    # small + small
    map(lambda x: combine_two_instances(small_seed, small_seed, small_small_out, x),
        overlap)
    # small + moderate
    map(lambda x: combine_two_instances(small_seed, moderate_seed, small_moderate_out, x),
        overlap)
    # moderate + moderate
    map(lambda x: combine_two_instances(moderate_seed, moderate_seed, moderate_moderate_out, x),
        overlap)