import json
import os
import shutil

SMALL_PATH = "/home/yuhui/Documents/tp3s/instance_generator/instance/small"
MODERATE_PATH = "/home/yuhui/Documents/tp3s/instance_generator/instance/moderate"
LARGE_PATH = "/home/yuhui/Documents/tp3s/instance_generator/instance/large"

def instance_id_mark():
    # mark the small instance
    mark_instance_in_dir(SMALL_PATH, "s")

    # mark the moderate instance
    mark_instance_in_dir(MODERATE_PATH, "m")

    # mark the large instance
    mark_instance_in_dir(LARGE_PATH, "l")


def mark_instance_in_dir(dir, prefix):
    counter = 0
    for f in os.listdir(dir):
        if f.endswith(".tp3s") and f.startswith("_"):
            src_path = os.path.join(dir, f)
            new_name = "{prefix}{id_counter}{orig_name}".format(prefix=prefix,
                                                                id_counter=counter,
                                                                orig_name=f)
            dest_path = os.path.join(dir, new_name)
            shutil.move(src_path, dest_path)
            counter += 1

def combine_two_instances(id1, id2):
    pass


def combine_instances(**inst_time_shift):
    # combine several json into one
    fat_json = []
    for inst_id, time_shift in inst_time_shift.iteritems():
        # search for the json
        inst_json_path = search_for_inst_id(inst_id)
        assert inst_json_path
        with open(inst_json_path, 'rb') as f:
            j = json.load(f)
            j['inst_id'] = inst_id
            # shift the timing information
            tests = j['tests']
            vehicles = j['vehicles']
            for test in tests:
                release = test['release']
                deadline = test['deadline']
                release += time_shift
                deadline += time_shift
                # prefix the id
                test["test_id"] = "{inst_id}_{old_id}".format(inst_id=inst_id,
                                                              old_id=test["test_id"])
                test['deadline'] = deadline
                test['release'] = release
            for vehicle in vehicles:
                release = vehicle['release']
                release += time_shift
                vehicle['release'] = release
                # prefix the id
                vehicle['vehicle_id'] = "{inst_id}_{old_id}".format(inst_id=inst_id,
                                                                    old_id=vehicle['vehicle_id'])
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
        if f.startswith(inst_id):
            return os.path.join(target_dir, f)
    return






if __name__ == '__main__':
    instance_id_mark()
