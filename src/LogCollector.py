import re
import os


def parse_log(dir):
    fields = ["inst_id", "num_test", "num_vehicle", "density", "num_seq", "iterations", "relax_obj_val",
              "cols_gen", "tardiness", "used_vehicle", "obj_val", "time_spent", "opt_gap"]
    data = []
    pat_num_test = re.compile(r'# tests read in: (\d+)')
    pat_num_vehicle = re.compile(r'# vehicles read in: (\d+)')
    pat_density = re.compile(r'Density: (\d+\.\d+)')
    pat_num_seq = re.compile(r'Total sequences: (\d+)')
    pat_num_iter = re.compile(r'Number of iterations: (\d+)')
    pat_num_cols = re.compile(r'Number of columns generated: (\d+)')
    pat_obj_val = re.compile(r'Obj val: (\d+\.\d+)')
    pat_relax_obj_val = re.compile(r'Relaxation obj val: (\d+\.\d+)')
    pat_tardiness = re.compile(r'Tardiness: (\d+\.\d+)')
    pat_used_vehicle = re.compile(r'Used vehicles: (\d+)')
    pat_time = re.compile(r'Time spent (\d+\.\d+)ms')
    pat_opt_gap = re.compile(r'Opt gap: ([\w.-]+)')
    pat_root_obj = re.compile(r'Root obj val: (\w+)')
    pat_best_bound = re.compile(r'Best bound: (\w+)')
    pat_nodes = re.compile(r'Nodes explored: (\w+)')
    pat = [pat_num_test, pat_num_vehicle, pat_density, pat_num_seq,
           pat_num_iter, pat_relax_obj_val, pat_num_cols, pat_tardiness, pat_used_vehicle,
           pat_obj_val, pat_time, pat_opt_gap, pat_root_obj, pat_best_bound, pat_nodes]
    for log in os.listdir(dir):
        if log.endswith(".log"):
            with open(os.path.join(dir, log), 'rb') as f:
                text = f.read()
            stats = [log.split("_")[0]]
            if text:
                for p in pat:
                    m = p.search(text)
                    if m:
                        stats.append(m.group(1))
                    else:
                        stats.append('-')
                data.append(','.join(stats))

    with open(os.path.join(dir, 'summary.csv'), 'wb') as f:
        f.write(','.join(fields))
        f.write('\n')
        f.write("\n".join(data))


def parse_multiple_log(dir):
    pat_num_test = re.compile(r'# tests read in: (\d+)')
    pat_num_vehicle = re.compile(r'# vehicles read in: (\d+)')
    pat_density = re.compile(r'Density: (\d+\.\d+)')
    pat_num_seq = re.compile(r'Total sequences: (\d+)')
    pat_num_iter = re.compile(r'Number of iterations: (\d+)')
    pat_num_cols = re.compile(r'Number of columns generated: (\d+)')
    pat_obj_val = re.compile(r'Obj val: (\d+\.\d+)')
    pat_relax_obj_val = re.compile(r'Relaxation obj val: (\d+\.\d+)')
    pat_tardiness = re.compile(r'Tardiness: (\d+\.\d+)')
    pat_used_vehicle = re.compile(r'Used vehicles: (\d+)')
    pat_time = re.compile(r'Time spent (\d+\.\d+)ms')
    pat_opt_gap = re.compile(r'Opt gap: ([\w.-]+)')

    fields = ["inst_id", "overlap", "total_num_test", "total_num_vehicle",
              "num_test1", "num_vehicle1", "density1", "num_test2", "num_vehicle2", "density2",
              "iterations", "relax_obj_val",
              "cols_gen", "obj_val", "time_spent", "opt_gap", "tardiness1", "used_vehicle1", "tardiness2", "used_vehicle2"]

    data = []
    for log in os.listdir(dir):
        if log.endswith(".log"):
            with open(os.path.join(dir, log), 'rb') as f:
                text = f.read()
            str_info = log.split("_")
            inst_id = str_info[0] + "_" + str_info[1]
            overlap = "".join(list(str_info[-1])[:-4])
            stats = [inst_id, overlap]
            num_test1, num_test2 = map(int, pat_num_test.findall(text))
            num_vehicle1, num_vehicle2 = map(int, pat_num_vehicle.findall(text))
            density_1, density_2 = pat_density.findall(text)
            stats.append(num_test1+num_test2)
            stats.append(num_vehicle1 + num_vehicle2)
            stats.extend([num_test1, num_vehicle1, density_1])
            stats.extend([num_test2, num_vehicle2, density_2])

            pat = [pat_num_iter, pat_relax_obj_val, pat_num_cols, pat_obj_val, pat_time, pat_opt_gap]
            for p in pat:
                m = p.search(text)
                if m:
                    stats.append(m.group(1))
                else:
                    stats.append('-')
            tardinss = pat_tardiness.findall(text)
            if not tardinss:
                tardinss = ["-"]*2
            stats.extend(tardinss)
            used_vehicle = pat_used_vehicle.findall(text)
            if not used_vehicle:
                used_vehicle = ["-"]*2
            stats.extend(used_vehicle)
            assert len(stats)==len(fields)
            data.append(','.join(map(str, stats)))

    with open(os.path.join(dir, 'summary.csv'), 'wb') as f:
        f.write(','.join(fields))
        f.write('\n')
        f.write("\n".join(data))


if __name__ == '__main__':
    log_dir = r'C:\Users\yuhuishi\Desktop\projects\TP3S_column_generation\logs\facility\large'
    parse_log(log_dir)
