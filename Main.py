from MP2 import Rush_Hour_Search
from tqdm import tqdm

Games = ["Game " + str(i) for i in range(1,7)]
heuristic = [(1,1,1), (1,2,1), (1,3,5), (1,4,1)]
for game in tqdm(Games):
    for h in heuristic:
        r = Rush_Hour_Search(game , input_file = "input.txt")
        r.ucs(heuristic = h)
