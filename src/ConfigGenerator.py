import json

OUT_FOLDER = '../config_files/'

CONFIG = {
    "num_test": 80,
    "num_vehicle": 80,
    "vehicle_rate": 5,
    "comp_dense": 0.8,
    "window_length": 2.0,
    "comp_factor": 1.0,
    "seed_prog": [
        33, 34, 35
    ],
    "safety_lib": 4
}


def main():
    # early stage
    # small size, small vehicle, dense incomp, tight deadline
    test_size = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 150, 200, 250, 300]
    dense = [0.8, 0.85, 0.9, 0.95]
    CONFIG['vehicle_rate'] = 4
    window_length = [1.0, 1.5, 2.0, 2.5]
    for size in test_size:
        for d in dense:
            for length in window_length:
                fname = "config_{testsize}_{vehiclesize}_{dense}_{length}.config".format(
                    testsize=size, vehiclesize=int(0.8*size), dense=d, length=length
                )
                CONFIG['num_test'] = size
                CONFIG['comp_dense'] = d
                CONFIG['window_length'] = length
                CONFIG['num_vehicle'] = int(0.8*size)
                with open(OUT_FOLDER + fname, 'wb') as f:
                    json.dump(CONFIG, f)






if __name__ == '__main__':
    main()
