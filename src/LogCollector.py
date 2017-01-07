import re
import os


def parse_log(dir):
    fields = ["num_test", "num_vehicle", "density", "num_seq", "iterations", "relax_obj_val",
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
            stats = []
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

    fields = ["num_test1", "num_test2", "total_num_test", "num_vehicle1", "num_vehicle2", "total_num_vehicle",
              "density1", "density2", "iterations", "relax_obj_val",
              "cols_gen", "obj_val", "time_spent", "opt_gap", "tardiness1", "tardiness2", "used_vehicle1", "used_vehicle2"]

    data = []
    for log in os.listdir(dir):
        if log.endswith(".log"):
            with open(os.path.join(dir, log), 'rb') as f:
                text = f.read()
            stats = []
            res = pat_num_test.findall(text)
            stats.extend(res)
            stats.append(sum(map(int, res)))
            res = pat_num_vehicle.findall(text)
            stats.extend(res)
            stats.append(sum(map(int, res)))
            res = pat_density.findall(text)
            stats.extend(res)
            pat = [pat_num_iter, pat_relax_obj_val, pat_num_cols, pat_obj_val, pat_time, pat_opt_gap]
            for p in pat:
                m = p.search(text)
                if m:
                    stats.append(m.group(1))
                else:
                    stats.append('-')
            stats.extend(pat_tardiness.findall(text))
            stats.extend(pat_used_vehicle.findall(text))
            assert len(stats)==len(fields)
            data.append(','.join(map(str, stats)))

    with open(os.path.join(dir, 'summary.csv'), 'wb') as f:
        f.write(','.join(fields))
        f.write('\n')
        f.write("\n".join(data))


if __name__ == '__main__':
    log_dir = r'C:\Users\yuhuishi\Desktop\projects\TP3S_column_generation\logs\multiple\small_small'
    parse_multiple_log(log_dir)
