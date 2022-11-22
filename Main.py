from MP2 import Rush_Hour_Search
from tqdm import tqdm

for game in tqdm(["Game 1", "Game 2", "Game 3", "Game 4", "Game 5", "Game 6"]):
    r = Rush_Hour_Search(game)
    r.gbfs()

