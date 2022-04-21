import os
import json
import numpy as np
from glob import glob
from itertools import permutations


if __name__ == '__main__':
    mat0 = np.array([
        [0, 1, 2, 3, 4],
        [4, 0, 1, 2, 3],
        [3, 4, 0, 1, 2],
        [2, 3, 4, 0, 1],
        [1, 2, 3, 4, 0],
    ])
    best = [np.inf] * 20
    rng = np.random.default_rng(0)
    for idx in permutations(np.arange(5)):
        mat1 = mat0[:, idx]
        d = {}
        for mat in [mat1, mat1[:, ::-1]]:
            for i in range(5):
                for j in range(4):
                    key = (mat[i, j], mat[i, j+1])
                    if key not in d:
                        d[key] = 0
                    d[key] += 1
        val = list(sorted([_ for _ in d.values()])[::-1])
        # print(val)
        if val < best:
            best = val
            best_mat = mat1
    print(best)
    print(best_mat)
    """
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    [[0 1 3 2 4]
    [4 0 2 1 3]
    [3 4 1 0 2]
    [2 3 0 4 1]
    [1 2 4 3 0]]
    """

    cats = ['bodies', 'faces', 'objects', 'scenes', 'scrambled_objects']
    cat_orders = {}
    for cat in cats:
        stimuli = sorted(glob(os.path.join('stimuli', cat, '*.mp4')))
        assert len(stimuli) == 12

        dups = rng.choice(12, 5, replace=False)
        while True:
            dups_new_order = rng.choice(5, 5, replace=False)
            if np.all(dups_new_order != np.arange(5)):
                break
        to_remove = dups[dups_new_order]

        orders = []
        for run in range(5):
            order0 = [_ for _ in range(12) if _ != to_remove[run]]
            rng.shuffle(order0)
            order = []
            for item in order0:
                if item == dups[run]:
                    order.append(item)
                order.append(item)
            orders.append([stimuli[_] for _ in order])
        cat_orders[cat] = orders
        print(cat, dups, to_remove)
        # print(orders)

    mat = np.concatenate([best_mat, best_mat[:, ::-1]], axis=1)
    for run in range(5):
        start_time = 18
        blocks = mat[run]
        stimuli = []
        for bn, idx in enumerate(blocks):
            cat = cats[idx]
            for i in range(6):
                stimuli.append([cat_orders[cat][run].pop(), start_time, start_time + 3])
                start_time += 3
            if bn == 4:
                start_time += 18
        # print(stimuli)
        with open(f'runs/{run+1}.json', 'w') as f:
            json.dump(stimuli, f)
