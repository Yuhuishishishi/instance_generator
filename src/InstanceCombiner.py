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
                # prefix the id
                # vehicle['vehicle_id'] = "{inst_id}_{old_id}".format(inst_id=inst_id,
                #                                                     old_id=vehicle['vehicle_id'])
            # # prefix the rehit matrix
            # rehit_matrix = j['rehit']
            # for id1 in rehit_matrix.keys():
            #     new_id = "{inst_id}_{test_id}".format(inst_id=inst_id, test_id=id1)
            #     rehit_matrix[new_id] = rehit_matrix.pop(id1)
            # for nest_dict in rehit_matrix.values():
            #     for id in nest_dict.keys():
            #         new_id = "{inst_id}_{test_id}".format(inst_id=inst_id, test_id=id)
            #         nest_dict[new_id] = nest_dict.pop(id)
            fat_json.append(j)

    return fat_json


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


def combine_two_instances():
    small_files = sorted(os.listdir("C:\Users\yuhuishi\PycharmProjects\instance_generator\instance\multiple\small_seed"))
    moderate_files = sorted(
        os.listdir("C:\Users\yuhuishi\PycharmProjects\instance_generator\instance\multiple\moderate_seed"))
    OUT_PATH = "C:\Users\yuhuishi\PycharmProjects\instance_generator\instance\multiple\moderate_moderate"
    for f1 in moderate_files:
        inst_id1 = f1.split("_")[0]
        for f2 in moderate_files:
            inst_id2 = f2.split("_")[0]
            if f1 == f2:
                continue
            # combine
            arg = {inst_id1: 0, inst_id2: 0}
            fat_json = combine_instances(**arg)
            with open(os.path.join(OUT_PATH, "{id1}_{id2}.tp3s".format(id1=inst_id1, id2=inst_id2)), 'wb') as f:
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
    combine_two_instances()
