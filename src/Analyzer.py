from InputOutput import GenInfoReader, Info


def main():
    # read in general information
    DB_PATH = '../db/tp3s.db'
    reader = GenInfoReader(DB_PATH)
    reader.read_db()

    # construct a symmetry 2d matrix
    mode_id_list = list(Info.TEST_MODE.keys())
    comp_mat_sym = {}
    for id1 in mode_id_list:
        for id2 in mode_id_list:
            if Info.COMP_MAT[id1, id2] or Info.COMP_MAT[id2, id1]:
                comp_mat_sym[id1, id2] = comp_mat_sym[id2, id1] = True
            else:
                comp_mat_sym[id1, id2] = comp_mat_sym[id2, id1] = False

    # set growth algorithm
    marked = [False]*len(mode_id_list)
    comp_sets = []

    while False in marked:
        idx = marked.index(False)
        seed = [mode_id_list[idx]]
        # find every test that is compatible to it
        comp_set = []
        while seed:
            seed_id = seed.pop()
            comp_set.append(seed_id)
            for id_ in mode_id_list:
                if comp_mat_sym[seed_id, id_] and not marked[id_]:
                    seed.append(id_)
                    marked[id_] = True
        else:
            comp_sets.append(comp_set)

    print comp_sets

if __name__ == "__main__":
    main()
