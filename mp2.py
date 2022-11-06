import numpy as np
import itertools


class State:
    def __int__(self, state, parent, heuristic=1):
        self.parent = parent
        if heuristic == 1:
            self.score = Rush_Hour_Search.h1(state)
        elif heuristic == 2:
            self.score = Rush_Hour_Search.h2(state)
        else:
            self.score = Rush_Hour_Search.h3(state, 3)

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
            content_clean = [game for game in f.read().split('\n') if not game.startswith('#') and game != '']
            for game in content_clean:
                if len(game.split(' ')[0]) != 36:
                    raise ValueError("the game number: {} contains not 36 places".format(index))
                dict_games['Game' + str(index)] = game.split(' ')[0]
                
                index += 1
                
                for i in game: 
                    if i not in cars and i != '.' and i != ' ' and not i.isdigit():
                        cars.append(i)
                
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

    def extract_game(self, input):
        board = list()
        input_arrayed = [*input]
        for i in range(0,6):
            board.append(input_arrayed[0+6*i:6+6*i])
        return board
    
    def game_to_numbers(self, input):
        board = Rush_Hour_Search.extract_game(self, input)
        letters = ['.']
        for i in board:
            for j in i:
                if j not in letters:
                    letters.append(j)
            
        LtoN = {l:n for l,n in zip(letters, [i for i in range(0,len(letters))])}
        puzzle = np.zeros((6,6))
        for i in range(len(board)):
            for j in range(len(board[i])):
                puzzle[i,j] = LtoN[board[i][j]]
       
        
        return puzzle, LtoN

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
                for row in range(0, 6):
                    print(game[6 * row: 6 * (row + 1)])
                print('fuel: {}'.format(tot_fuel[count]))
                count += 1
                print("\n --------------------- \n")

    def h1(self, state):
        value = 0
        count = False
        counted = list()
        for i in range(0,6):
            current = state[2][i]
            if current == 'A':
                count = True
            elif count and current != '.' and current not in counted:
                value += 1
                counted.append(current)
        return value

    def h2(self, state):
        value = 0
        count = False
        for i in range(0, 6):
            current = state[2][i]
            if current == 'A':
                count = True
            elif count and current != '.':
                value += 1
        return value

    def h3(self, state, alpha=1):
        return alpha * self.h1(state)
   
    '''
    def UCS(self):
    def gbfs(self):
    '''
    
    def A_star(self, input):
        global puzzle
        puzzle, LtoN = Rush_Hour_Search.game_to_numbers(self, input)
        fuel = Rush_Hour_Search.read_file(self)[-1]
        
r = Rush_Hour_Search(select_game = 'all')
dict_games, dict_fuel = r.read_file()
#state = r.game_to_numbers(dict_games["Game2"])
#r.print()
r.A_star(dict_games["Game2"])
#print("score: " + str(r.h1(state)))
