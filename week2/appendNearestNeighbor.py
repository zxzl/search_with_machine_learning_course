import argparse
from dataclasses import dataclass
from typing import List

import fasttext

parser = argparse.ArgumentParser()
parser.add_argument('--input')
parser.add_argument('--output')
parser.add_argument('--model')
parser.add_argument('--threshold', type=float)
args = parser.parse_args()

model = fasttext.load_model(args.model)

@dataclass
class Stats:
    total:int = 0
    over_threshold:int = 0
stats = Stats()

output: List[str] = []
with open(args.input, 'r') as f:
    for l in f.readlines():
        neighbors = model.get_nearest_neighbors(l)
        word = l.strip()
        neighbor_index = 1 if neighbors[0][1] == word else 0
        score, neighbor = neighbors[neighbor_index]
        stats.total += 1
        if score >= args.threshold:
            output.append(f"{word},{neighbor}")
            stats.over_threshold += 1

with open(args.output, 'w') as f:
    for o in output:
        f.write(o)
        f.write('\n')

print(stats)
