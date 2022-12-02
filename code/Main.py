# =============================================================================
# Mini Project 2: Rush Hours.
# Main code 
# =============================================================================

from MP2 import Rush_Hour_Search
from tqdm import tqdm

Games = ["Game " + str(i) for i in [1,48]]
heuristic = [(1,1,1), (1,2,1), (1,3,5), (1,4,1), (1,5,1)]
for game in tqdm(Games):
    for h in heuristic:
        r = Rush_Hour_Search(game , input_file = "games_file.txt")
        #r.ucs()
        r.A_star(heuristic = h)
        r.gbfs(heuristic = h)

