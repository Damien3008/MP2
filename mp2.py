import numpy as np
import itertools

class Rush_Hour_Search:
    '''
    This class will contain all the implementations of algorithms for the resolution of the Rush Hour problem
    '''
    
    def __init__(self, input_file = 'input.txt', select_game = 'all'):
        self.input_file = input_file
        self.select_game = select_game
        
    def read_file(self):
        dict_games = dict()
        tot_fuel = list()
        index = 1
        dict_fuel = dict()
        cars = list()
        fuel = list()
        with open(self.input_file, 'r') as f:
            content_clean = [game for game in f.read().split('\n') if game[0] != '#']
            for game in content_clean:
                if len(game.split(' ')[0]) != 36:
                    raise ValueError("the game number: {} contains not 36 places".format(index))
                dict_games['Game' + str(index)] = game.split(' ')[0]
                
                index += 1
                
                for i in game: 
                    if i not in cars and i != '.' and i != ' ' and not i.isdigit():
                        cars.append(i)
                #print(len(game.split(' ')))
                
                if len(game.split(' ')) != 1:
                    for j in range(1, len(game.split(' '))):
                        for i in range(len(game.split(' ')[j]) - 1):
                            if len(game.split(' ')[j][i]) == 1 and game.split(' ')[j][i+1] == ' ':
                                dict_fuel[game.split(' ')[j][i]] = 100
                            else:
                                dict_fuel[game.split(' ')[j][i]] = game.split(' ')[j][i+1] 
                        
                        if len(dict_fuel) != len(cars):
                            for car in cars:
                                if car not in list(dict_fuel.keys()):
                                    dict_fuel[car] = 100
                
                else:
                    fuel = len(cars) * [100]
                    dict_fuel = {c: f for c, f in zip(cars, fuel)}
                
                tot_fuel.append(dict_fuel)
                cars, fuel = [], []
                dict_fuel = dict()
                    
            f.close()
        if self.select_game == 'all':
            return dict_games, tot_fuel
        else:
            return dict(itertools.islice(dict_games.items(), int(self.select_game) -1, int(self.select_game))), tot_fuel[int(self.select_game) -1: int(self.select_game)]
  
    
    def print(self):
        dict_games, tot_fuel = Rush_Hour_Search.read_file(self)
        count = 0
        if self.select_game == 'all':
            for index, game in dict_games.items():
                print('Game number: {}'.format(index))
                for row in range(0, 6):
                    print(game[6 * row: 6 * (row + 1)])
                print('fuel: {}'.format(tot_fuel[count]))
                count += 1
                print("\n --------------------- \n")
        else:
            print('Game number: {}'.format(int(self.select_game)))
            for index, game in dict_games.items():
                print('Game number: {}'.format(index))
                for row in range(0, 6):
                    print(game[6 * row: 6 * (row + 1)])
                print('fuel: {}'.format(tot_fuel[count]))
                count += 1
                print("\n --------------------- \n")
   
    '''
    def UCS(self):
    
    
    
    def GBFS(self):
    
        
    def A_star(self):
    '''
        
r = Rush_Hour_Search(select_game = '2')
dict_games, dict_fuel = r.read_file()
r.print()
