# =============================================================================
# Mini Project 2: Rush Hour
# This is the Library file, which contains all methods that will serve on 
# solving the questions of Mini-Project 2 of Artificial Intelligent COMP 472
# =============================================================================

from heapq import *
import itertools
from datetime import datetime
import copy
from time  import time

class GameEngine:
    
    '''
    This class contains the methods for extracting features such as puzzles, fuels ext.
    We implement also some preprocessing step in order to make the search algorithms easier
    to build.
    inputs:
        input_file: the path of your file that contains puzzles
        select_game: (default 'all') if you want to run one game in particular.
    '''
    
    def __init__(self, input_file = 'input.txt', select_game = 'all'):
        self.input_file = input_file
        self.select_game = select_game
        
    def read_file(self):
        
        """
        Method for reading a file and extract the puzzle and the fuel for each game.
        Raises
        ------
        ValueError
            If the game is not correct (contains not enough cars, or spaces).
        Returns
        -------
        dict_games (dictionnary)
            Dictionnary that contains all the puzzles of the input_file.
        dict_fuel (dictionnary)
            Dictionnary that contains all the fuel of the puzzles.
        """
        
        dict_games = dict()
        tot_fuel = list()
        index = 1
        dict_fuel = dict()
        cars = list()
        fuel = list()
        f = open(self.input_file, 'r')
        content_clean = [game for game in f.read().split('\n') if not game.startswith('#') and game != '']
        for game in content_clean:
            if len(game.split(' ')[0]) != 36:
                raise ValueError("the game number: {} contains not 36 places".format(index))
            dict_games['Game' + ' ' + str(index)] = game.split(' ')[0]
            
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


    def print_results(self, method, game, start, end, finishing_state, state_counter, ambulance, heuristic, index_a, solution, cars):
        
        """ given the final parameters after running the algorith, this method computes the necessary information and writes it to a file 
        Parameters
        ----------
        method : str
            the name of the used algorithm
        game : int
            the number of the game
        start : datetime
            timestamp at start of algorithm
        end : datetime
            timestamp at end of algorithm
        finishing_state : State
            State object of final state
        state_counter : int
            count of search path length
        ambulance : Car
            Car object corresponding to the ambulance
        heuristic : int
            number of used heuristic
        index_a : int
            index position of ambulance in horizontal_cars
        solution : boolean
            Boolean if solution has been found
        cars : List
            List of all cars
        """
        
        # Initialize the file, depending on the algorithm used
        if method == "ucs":
            file_sol = open(method + '-' + 'sol' + '-' + 'game' + game.split(" ")[1] + '.txt', 'w')
            file_search = open(method + '-' + 'search' + '-' + 'game' + game.split(" ")[1] + '.txt', 'w')
        else:
            file_sol = open(method + '-' + 'sol' + '-h' + str(heuristic[1]) + '-' + 'game' + game.split(" ")[1] + '.txt', 'w')
            file_search = open(method + '-' + 'search' + '-h' + str(heuristic[1]) + '-' + 'game' +  game.split(" ")[1] + '.txt', 'w')
        # Extract Fuel Levels
        fuel_levels = ""
        for car in cars:
            fuel_levels = fuel_levels + car.name + ": " + str(car.fuel) + " "

        if not solution:
                file_sol.write("No solution\n")
                file_search.write("No solution\n")
                file_sol.write(fuel_levels + "\n")
                file_sol.close()
                file_search.close()
                return

        current = finishing_state
        solution = ""
        solution_search = ""
        solution_path = ""
        solution_counter = 0
        # Create a solution string, by iteratively looking at the last move done by the algorithm and then calling the previous state.
        while current.parent is not None:
            solution_counter += 1
            if current.last_move[0].orientation == "H":
                if current.last_move[1] <= -1:
                    solution_path = current.last_move[0].name + " " + str(-1 * current.last_move[1]) + " left; " + solution_path
                    solution = current.last_move[0].name + " " + str(-1 * current.last_move[1]) + " left\t\t" + str(current.last_move[2]) + "\t" + str(current) + "\n" + solution
                else:
                    solution_path = current.last_move[0].name + " " + str(current.last_move[1]) +  " right; " + solution_path
                    solution = current.last_move[0].name + " " + str(current.last_move[1]) +  " right\t\t" + str(current.last_move[2]) + "\t"+ str(current) + "\n" + solution
            else:
                if current.last_move[1] <= -1:
                    solution_path = current.last_move[0].name + " " + str(-1 * current.last_move[1]) +  " up; " + solution_path
                    solution = current.last_move[0].name + " " + str(-1 * current.last_move[1]) +  " up\t\t" + str(current.last_move[2]) + "\t"+ str(current) + "\n"+ solution
                else:
                    solution_path = current.last_move[0].name + " " + str(current.last_move[1]) +  " down; " + solution_path
                    solution = current.last_move[0].name + " " + str(current.last_move[1]) +  " down\t\t" + str(current.last_move[2]) + "\t" + str(current) + "\n" + solution
            if method == 'A_star':
                solution_search = str(current.h + current.cost) + '\t' + str(current.cost) + '\t' + str(current.h) + '\t' + str(current) + "\n" + solution_search
            elif method == 'gbfs':
                 solution_search =  str(0) + '\t' + str(0) + '\t' + str(current.h) + '\t' + str(current) + "\n" + solution_search
            else:
                solution_search =  str(0) + '\t' + str(current.cost) + str(0) + '\t' + str(current) + "\n" + solution_search

            current = current.parent
        move_a = 5 - ambulance.y - finishing_state.offset[index_a] - ambulance.length + 1
        # Check if the ambulance has reached its goal yet. If not, move it to the goal and update the values
        if move_a > 0:
            solution_counter += 1
            finishing_state.offset[index_a] += move_a
            finishing_state = move_right(finishing_state, ambulance, heuristic, index_a, cars, move_a)
            actually_move_state(finishing_state)
            solution = solution + ambulance.name +  " " + str(move_a) + " right\t\t" + str(ambulance.fuel + finishing_state.fuel_offset[index_a]) + "\t" + str(current) + "\n"
            solution_path = solution_path + ambulance.name +  " " + str(move_a) + " right;"
        file_sol.write("Initial Board Configuration: " + str(current) + "\n\n")
        for item in current.state:
            file_sol.write(str(item).replace(", ", " ").replace("[", " ").replace("]", " ").replace("'", ""))
            file_sol.write('\n')
        file_sol.write("\n")
        file_sol.write("Car fuel available: " + fuel_levels + "\n")
        file_sol.write("Runtime: " + str((end - start).total_seconds()) + " seconds\n")
        file_sol.write("Search path length: " + str(state_counter) + " states\n")
        file_sol.write("Solution path length: " + str(solution_counter) + " moves\n")
        file_sol.write("Solution path: " + solution_path + '\n\n')        
        file_sol.write(solution)
        file_sol.write("\n")
        for item in finishing_state.state:
            file_sol.write(str(item).replace(", ", " ").replace("[", " ").replace("]", " ").replace("'", ""))
            file_sol.write('\n')

        file_search.write(solution_search)
        file_sol.close()
        file_search.close()

    def __str__(self):
        
        """
        Returns
        -------
        out : str
            Return the list of puzzles of the input_file.
        """
        
        dict_games, tot_fuel = self.read_file()
        out = ""
        for number, game in dict_games.items():
            out += f"Game n°{number}:\n"
            out += str(game).replace(", ", "").replace("[", "").replace("]", "").replace("'", "")
            out += '\n' 

        return out
                
    def extract_game(self, game):
        
        """
        Parameters
        ----------
        game : str
            the name of the game that we want to extract the puzzle.

        Returns
        -------
        board : list of int32
            puzzle of game name.
        """
        
        board = list()
        input_arrayed = [*self.read_file()[0][game]]
        for i in range(0, 6):
            board.append(input_arrayed[0 + 6 * i:6 + 6 * i])
        return board
    
    def extract_fuel(self, game):
        
        """
        Parameters
        ----------
        game : str
            the name of the game that we want to extract the fuel.

        Returns
        -------
        list of int32
            list of fuel for game name.
        """
        
        num = int(game.split(' ')[1])
        return GameEngine.read_file(self)[-1][num - 1]
    
    def PositionCar(self, board, fuel):
        
        """
        Parameters
        ----------
        board : list of int32
            puzzle of a game.
        fuel : list of int32
            list if fuel for the puzzle.

        Returns
        -------
        horizontal_cars : list of Car
            list that contains cars that are horizontal.
        vertical_cars : list of Car
            list that contains cars that are vertical.
        index_a : int32
            position of the ambulance.
        """
        
        horizontal_cars = list()
        vertical_cars = list()
        index = 0
        for j in range(0, 6):
            for i in range(0, 6):
                current = board[i][j]
                if current == '.':
                    continue
                if j < 5:
                    k = j
                    while k <= 5:
                        k += 1
                        if k > 5:
                            break
                        if not board[i][k] == current:
                            break
                        board[i][k] = '.'
                    if current == 'A':
                        index_a = len(horizontal_cars)
                    if k - j > 1:
                        horizontal_cars.append(Car(current, "H", k - j, i, j, 0, int(fuel[current])))
                if i <= 5:
                    k = i
                    while k <= 5:
                        k += 1
                        if k > 5:
                            break
                        if not board[k][j] == current:
                            break
                        board[k][j] = '.'
                    if k - i > 1:
                        vertical_cars.append(Car(current, "V", k - i, i, j, 0, int(fuel[current])))
                        
        for item in horizontal_cars:
            item.i = index
            index += 1
        for item in vertical_cars:
            item.i = index
            index += 1
                
        return horizontal_cars, vertical_cars, index_a


class State:

    '''
    This class contains the necessary logic to keep track of every search node aka State. 
    inputs:
        state : a 6x6 list, containing the current positions of all cars
        parent : State that refers to the previously visited State
        offset : List keeping track of the movements of each car
        fuel_offset : List keeping track of the used fuel for each car
        heuristic : Tupel containg information if a heuristic is used, the heuristic number and lambda
        g : int 0 or 1, whether or not the amount of past moves should be taken into account
        last_move : Tupel containing the information about the last moved car, the number of steps and the remaining fuel
        
    '''

    def __init__(self, state, parent, offset, fuel_offset, cars, heuristic=(1,4,1), g = 0, last_move=("Z", 0, 0)):
        self.last_move = last_move
        self.parent = parent
        self.offset = offset
        self.state = state
        self.fuel_offset = fuel_offset
        self.cars = cars
        self.cost = 0

        if heuristic[0] == 1:
            self.h = h(offset, self.cars, heuristic[1], heuristic[2])
        
        elif heuristic[0] == 0:
            self.h = 0
            
        if type(parent) == State:
            self.cost = parent.cost + 1
        
        if g == 1 and heuristic[0] == 1:
            self.score = self.h + self.cost
        elif g == 1 and heuristic[0] == 0:
            self.score = self.cost
        else:
            self.score = self.h
            
    def __deepcopy__(self, memodict={}):
        
        """
        ----------
        memodict : dictionnary, optional
            The default is {}.

        Returns
        -------
        copy_object : state
            Overloading the deepcopy method.
            Parameters.
        """
        
        copy_object = State()
        copy_object.value = self.value
        return copy_object
        
    # We define the comparison methods so that the heap has a basis to compare the different states
    
    def __eq__(self, other):
        return self.score == other.score

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __ge__(self, other):
        return self.score >= other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ne__(self, other):
        return not self.score == other.score

    def __str__(self):
        return  str(self.state).replace(" ", "").replace("'", "").replace(",", "").replace("[", "").replace("]", "")

class Car():

    '''
    This class is used to save all the information regarding the different car this includes:
    inputs:
        name : str which contains the letter as shown in the initial game board
        orientation : H or V whether the car is horizontal or vertical
        length : int, length of the car
        x : initial y location of the car (origin top left), with postive y going down
        y : initial x location of the car (origin top left)
    '''

    def __init__(self, name, orientation, length, x, y, i=0, fuel=100):
        if not isinstance(name, str):
            raise ValueError("The name needs to be a string.")
        if orientation not in ["H", "V"]:
            raise ValueError("The orientation needs to be either H or V.")
        if not isinstance(length, int):
            raise ValueError("The length needs to be an integer.")
        if not isinstance(fuel, int):
            raise ValueError("The fuel needs to be an integer.")
        self.name = name
        self.orientation = orientation
        self.length = length
        self.fuel = fuel
        self.x = x
        self.y = y
        self.i = i

    def __str__(self):
        return  self.name + ", " + self.orientation


# -------------- Implementation of the move methods --------------

def actually_move_state(state):
    car = state.last_move[0]
    num_steps = state.last_move[1]
    if car.orientation == "H":
        if num_steps > 0:
            actually_move_right(state)
        elif num_steps < 0:
            actually_move_left(state)
    elif car.orientation == "V":
        if num_steps > 0:
            actually_move_down(state)
        elif num_steps < 0:
            actually_move_up(state)
    else:
        print("Something is weird!")


def actually_move_right(state):
    new_fuel_offset = copy.deepcopy(state.fuel_offset)
    car = state.last_move[0]
    new_fuel_offset[car.i] = new_fuel_offset[car.i] - 1
    new_state = copy.deepcopy(state.state)
    num_steps = abs(state.last_move[1])
    for j in range(0, car.length):
        new_state[car.x][car.y + state.offset[car.i] + j] = car.name
    for j in range(0, num_steps):
        new_state[car.x][car.y + j + state.offset[car.i] - num_steps] = "."
    state.state = new_state
    state.fuel_offset = new_fuel_offset


def actually_move_left(state):
    new_fuel_offset = copy.deepcopy(state.fuel_offset)
    car = state.last_move[0]
    new_fuel_offset[car.i] = new_fuel_offset[car.i] - 1
    new_state = copy.deepcopy(state.state)
    num_steps = abs(state.last_move[1])
    for j in range(0, car.length):
        new_state[car.x][car.y + state.offset[car.i] + j] = car.name
    for j in range(0, num_steps):
        if not car.y + state.offset[car.i] + car.length + j >= 6:
            new_state[car.x][car.y + state.offset[car.i] + j + car.length] = "."
    state.state = new_state
    state.fuel_offset = new_fuel_offset


def actually_move_down(state):
    new_fuel_offset = copy.deepcopy(state.fuel_offset)
    car = state.last_move[0]
    new_fuel_offset[car.i] = new_fuel_offset[car.i] - 1
    new_state = copy.deepcopy(state.state)
    num_steps = abs(state.last_move[1])
    for j in range(0, car.length):
        new_state[car.x + state.offset[car.i] + j][car.y] = car.name
    for j in range(0, num_steps):
        new_state[car.x + j + state.offset[car.i] - num_steps][car.y] = "."
    state.state = new_state
    state.fuel_offset = new_fuel_offset


def actually_move_up(state):
    new_fuel_offset = copy.deepcopy(state.fuel_offset)
    car = state.last_move[0]
    new_fuel_offset[car.i] = new_fuel_offset[car.i] - 1
    num_steps = abs(state.last_move[1])
    new_state = copy.deepcopy(state.state)
    for j in range(0, car.length):
        new_state[car.x + state.offset[car.i] + j][car.y] = car.name
    for j in range(0, num_steps):
        if not car.x + state.offset[car.i] + car.length + j >= 6:
            new_state[car.x + state.offset[car.i] + car.length + j][car.y] = "."
    state.state = new_state
    state.fuel_offset = new_fuel_offset

def move_right(current_state, car, heuristic, i, cars, num_steps=1,g=0):
    new_offset = copy.deepcopy(current_state.offset)
    return State(current_state.state, current_state, new_offset, current_state.fuel_offset, cars, heuristic, g,
                 (car, num_steps, car.fuel + current_state.fuel_offset[i] - 1))


def move_left(current_state, car, heuristic, i, cars, num_steps=1, g=0):
    new_offset = copy.deepcopy(current_state.offset)
    return State(current_state.state, current_state, new_offset, current_state.fuel_offset, cars, heuristic, g,
                 (car, -1 * num_steps, car.fuel + current_state.fuel_offset[i] - 1))


def move_down(current_state, car, heuristic, i, cars, num_steps=1, g=0):
    new_offset = copy.deepcopy(current_state.offset)
    return State(current_state.state, current_state, new_offset, current_state.fuel_offset, cars,heuristic, g,
                 (car, num_steps, car.fuel + current_state.fuel_offset[i] - 1))


def move_up(current_state, car, heuristic, i, cars, num_steps=1, g=0):
    new_offset = copy.deepcopy(current_state.offset)
    return State(current_state.state, current_state, new_offset, current_state.fuel_offset, cars, heuristic, g,
                 (car, -1 * num_steps, car.fuel + current_state.fuel_offset[i] - 1))

def h(offset, cars, heuristic=1, alpha=1):
    """
    Parameters
    ----------
    state : board 
        board of the current puzzle.
    heuristic : int32, optional
        heuristic that you want to use (available = [1,2,3,4,5]). The default is 1.
    alpha : int32, optional
        weight for heuristic 3. The default is 1.

    Returns
    -------
    int32
        value of the heuristic.
    """
    
    value = 0
    ambu = None
    value = 0
    for car in cars:
        if car.name == 'A':
            ambu = car
    if heuristic == 5:
        if ambu.y + offset[ambu.i] == 4:
            return 1
        else:
            return 0
    for car in cars:
        if car == ambu:
            continue
        if car.orientation == "H":
            if car.x == 2 and car.y > ambu.y:
                if heuristic == 2:
                    value += car.length
                    continue
                value += 1
        else:
            if car.y > ambu.y + offset[ambu.i] and car.x + offset[car.i] <= 2 <= car.x + offset[car.i] + car.length - 1:
                value = value + 1
    if heuristic == 3:
        return value * alpha
    return value
            

class Rush_Hour_Search(GameEngine):
    
    '''
    This class will contain all the implementation of algorithms for the resolution of the Rush Hour problem
    '''
    
    def __init__(self, game, input_file = 'input.txt', select_game = 'all'):
        self.game = game
        self.input_file = input_file
        self.select_game = select_game
        GameEngine(self)
    
    def ucs(self, heuristic= (0,0,0)):
        
        """
        Parameters
        ----------
        heuristic : tuple of int32, optional
            Don't use heurisitc for the algorithm. The default is (0,0,0).

        Returns
        -------
        None. Call the print_result function to save result of the game.
        """
        
        start = datetime.now()
        fuel = self.extract_fuel(self.game)
        solution = True
        open_list = []
        closed_list = set()
        board = self.extract_game(self.game)
        state_board = copy.deepcopy(board)
        horizontal_cars = list()
        vertical_cars = list()
        horizontal_cars, vertical_cars, index_a = self.PositionCar(board, fuel)
        offset = [0] * (len(horizontal_cars) + len(vertical_cars))
        fuel_offset = [0] * (len(horizontal_cars) + len(vertical_cars))
        cars = horizontal_cars + vertical_cars
        current_state = State(state_board, None, offset, fuel_offset, cars, heuristic, g=1)
        # used to generate all children that can move
        while h(current_state.offset, cars, heuristic=1, alpha=1) > 0:
            if isinstance(current_state.parent, State):
                actually_move_state(current_state)
            # Generate all possible children
            for i in range(0, len(horizontal_cars)):
                car = horizontal_cars[i]
                if car.fuel + current_state.fuel_offset[i] <= 0:
                    continue
                if isinstance(current_state.parent, State):
                    if car.name == current_state.parent.last_move[0]:
                        continue
                for j in range(0, 4):
                    if not car.y + current_state.offset[i]-j == 0:
                        if current_state.state[car.x][car.y - 1 + current_state.offset[i] - j] == '.':
                            current_state.offset[i] = current_state.offset[i] - j - 1
                            if str(current_state.offset) not in closed_list:
                                heappush(open_list, move_left(current_state, car, heuristic, i, cars, g=1, num_steps=j + 1))
                            current_state.offset[i] = current_state.offset[i] + j + 1
                        else:
                            break
                    else:
                        break
                for j in range(0, 4):
                    if not car.y + car.length + current_state.offset[i]+j >= 6:
                        if current_state.state[car.x][car.y + car.length + current_state.offset[i] + j] == '.':
                            current_state.offset[i] = current_state.offset[i] + j + 1
                            if str(current_state.offset) not in closed_list:
                                heappush(open_list, move_right(current_state, car, heuristic, i, cars, g=1, num_steps=j + 1))
                            current_state.offset[i] = current_state.offset[i] - j - 1
                        else:
                            break
                    else:
                        break
            for i in range(len(horizontal_cars), len(vertical_cars) + len(horizontal_cars)):
                car = vertical_cars[i - len(horizontal_cars)]
                if car.fuel + current_state.fuel_offset[i] <= 0:
                    continue
                if isinstance(current_state.parent, State):
                    if car.name == current_state.parent.last_move[0]:
                        continue
                for j in range(0, 4):
                    if not car.x + current_state.offset[i]-j == 0:
                        if current_state.state[car.x - 1 + current_state.offset[i] - j][car.y] == '.':
                            current_state.offset[i] = current_state.offset[i] - j - 1
                            if str(current_state.offset) not in closed_list:
                                heappush(open_list, move_up(current_state, car, heuristic, i, cars, g=1, num_steps=j + 1))
                            current_state.offset[i] = current_state.offset[i] + j + 1
                        else:
                            break
                    else:
                        break
                for j in range(0, 4):
                    if not car.x + car.length + current_state.offset[i] + j >= 6:
                        if current_state.state[car.x + car.length + current_state.offset[i] + j][car.y] == '.':
                            current_state.offset[i] = current_state.offset[i] + j + 1
                            if str(current_state.offset) not in closed_list:
                                heappush(open_list, move_down(current_state, car, heuristic, i, cars, g=1, num_steps=j + 1))
                            current_state.offset[i] = current_state.offset[i] - j - 1
                        else:
                            break
                    else:
                        break
            closed_list.add(str(current_state.offset))
            if len(open_list) > 0:
                current_state = heappop(open_list)
            elif  h(current_state.offset, cars, heuristic=1, alpha=1) > 0:
                solution = False
                break
            
        self.print_results("ucs", self.game, start, datetime.now(), current_state, len(closed_list), horizontal_cars[index_a], heuristic, index_a,
                    solution, horizontal_cars + vertical_cars)
    
    def gbfs(self, heuristic=(1, 4, 1)):
        
        """
        Parameters
        ----------
        heuristic : tuple of int32, optional
            Select the heuristic that you want to use. The default is (1,4,1).

        Returns
        -------
        None. Call the print_result function to save result of the game.
        """
        
        start = datetime.now()
        fuel = self.extract_fuel(self.game)
        solution = True
        open_list = []
        closed_list = set()
        board = self.extract_game(self.game)
        state_board = copy.deepcopy(board)
        horizontal_cars = list()
        vertical_cars = list()
        horizontal_cars, vertical_cars, index_a = self.PositionCar(board, fuel)
        offset = [0] * (len(horizontal_cars) + len(vertical_cars))
        fuel_offset = [0] * (len(horizontal_cars) + len(vertical_cars))
        cars = horizontal_cars + vertical_cars
        current_state = State(state_board, None, offset, fuel_offset, cars, heuristic)
        
        while current_state.h > 0:
            if isinstance(current_state.parent, State):
                actually_move_state(current_state)
            # Generate all possible children
            for i in range(0, len(horizontal_cars)):
                car = horizontal_cars[i]
                if car.fuel + current_state.fuel_offset[i] <= 0:
                    continue
                if isinstance(current_state.parent, State):
                    if car.name == current_state.parent.last_move[0]:
                        continue
                for j in range(0, 4):
                    if not car.y + current_state.offset[i]-j == 0:
                        if current_state.state[car.x][car.y - 1 + current_state.offset[i] - j] == '.':
                            current_state.offset[i] = current_state.offset[i] - j - 1
                            if str(current_state.offset) not in closed_list:
                                heappush(open_list, move_left(current_state, car, heuristic, i, cars, num_steps=j + 1))
                            current_state.offset[i] = current_state.offset[i] + j + 1
                        else:
                            break
                    else:
                        break
                for j in range(0, 4):
                    if not car.y + car.length + current_state.offset[i]+j >= 6:
                        if current_state.state[car.x][car.y + car.length + current_state.offset[i] + j] == '.':
                            current_state.offset[i] = current_state.offset[i] + j + 1
                            if str(current_state.offset) not in closed_list:
                                heappush(open_list, move_right(current_state, car, heuristic, i, cars, num_steps=j + 1))
                            current_state.offset[i] = current_state.offset[i] - j - 1
                        else:
                            break
                    else:
                        break
            for i in range(len(horizontal_cars), len(vertical_cars) + len(horizontal_cars)):
                car = vertical_cars[i - len(horizontal_cars)]
                if car.fuel + current_state.fuel_offset[i] <= 0:
                    continue
                if isinstance(current_state.parent, State):
                    if car.name == current_state.parent.last_move[0]:
                        continue
                for j in range(0, 4):
                    if not car.x + current_state.offset[i]-j == 0:
                        if current_state.state[car.x - 1 + current_state.offset[i] - j][car.y] == '.':
                            current_state.offset[i] = current_state.offset[i] - j - 1
                            if str(current_state.offset) not in closed_list:
                                heappush(open_list, move_up(current_state, car, heuristic, i, cars, num_steps=j + 1))
                            current_state.offset[i] = current_state.offset[i] + j + 1
                        else:
                            break
                    else:
                        break
                for j in range(0, 4):
                    if not car.x + car.length + current_state.offset[i] + j >= 6:
                        if current_state.state[car.x + car.length + current_state.offset[i] + j][car.y] == '.':
                            current_state.offset[i] = current_state.offset[i] + j + 1
                            if str(current_state.offset) not in closed_list:
                                heappush(open_list, move_down(current_state, car, heuristic, i, cars, num_steps=j + 1))
                            current_state.offset[i] = current_state.offset[i] - j - 1
                        else:
                            break
                    else:
                        break
            closed_list.add(str(current_state.offset))
            if len(open_list) > 0:
                current_state = heappop(open_list)
            elif current_state.h > 0:
                solution = False
                break
        self.print_results('gbfs', self.game, start, datetime.now(), current_state, len(closed_list), horizontal_cars[index_a], heuristic, index_a,
                    solution, horizontal_cars + vertical_cars)


    def A_star(self, heuristic = (1,4,1)):
        
        """
        Parameters
        ----------
        heuristic : tuple of int32, optional
            Select the heuristic that you want to use. The default is (1,4,1).

        Returns
        -------
        None. Call the print_result function to save result of the game.
        """
        
        start = datetime.now()
        fuel = self.extract_fuel(self.game)
        solution = True
        open_list = []
        closed_list = set()
        board = self.extract_game(self.game)
        state_board = copy.deepcopy(board)
        horizontal_cars = list()
        vertical_cars = list()
        horizontal_cars, vertical_cars, index_a = self.PositionCar(board, fuel)
        offset = [0] * (len(horizontal_cars) + len(vertical_cars))
        fuel_offset = [0] * (len(horizontal_cars) + len(vertical_cars))
        cars = horizontal_cars + vertical_cars
        current_state = State(state_board, None, offset, fuel_offset, cars, heuristic, g=0)
        
        while current_state.h > 0:
            if isinstance(current_state.parent, State):
                actually_move_state(current_state)
            # Generate all possible children
            for i in range(0, len(horizontal_cars)):
                car = horizontal_cars[i]
                if car.fuel + current_state.fuel_offset[i] <= 0:
                    continue
                if isinstance(current_state.parent, State):
                    if car.name == current_state.parent.last_move[0]:
                        continue
                for j in range(0, 4):
                    if not car.y + current_state.offset[i]-j == 0:
                        if current_state.state[car.x][car.y - 1 + current_state.offset[i] - j] == '.':
                            current_state.offset[i] = current_state.offset[i] - j - 1
                            if str(current_state.offset) not in closed_list:
                                heappush(open_list, move_left(current_state, car, heuristic, i, cars, g=1, num_steps=j + 1))
                            current_state.offset[i] = current_state.offset[i] + j + 1
                        else:
                            break
                    else:
                        break
                for j in range(0, 4):
                    if not car.y + car.length + current_state.offset[i]+j >= 6:
                        if current_state.state[car.x][car.y + car.length + current_state.offset[i] + j] == '.':
                            current_state.offset[i] = current_state.offset[i] + j + 1
                            if str(current_state.offset) not in closed_list:
                                heappush(open_list, move_right(current_state, car, heuristic, i, cars, g=1, num_steps=j + 1))
                            current_state.offset[i] = current_state.offset[i] - j - 1
                        else:
                            break
                    else:
                        break
            for i in range(len(horizontal_cars), len(vertical_cars) + len(horizontal_cars)):
                car = vertical_cars[i - len(horizontal_cars)]
                if car.fuel + current_state.fuel_offset[i] <= 0:
                    continue
                if isinstance(current_state.parent, State):
                    if car.name == current_state.parent.last_move[0]:
                        continue
                for j in range(0, 4):
                    if not car.x + current_state.offset[i]-j == 0:
                        if current_state.state[car.x - 1 + current_state.offset[i] - j][car.y] == '.':
                            current_state.offset[i] = current_state.offset[i] - j - 1
                            if str(current_state.offset) not in closed_list:
                                heappush(open_list, move_up(current_state, car, heuristic, i, cars, g=1, num_steps=j + 1))
                            current_state.offset[i] = current_state.offset[i] + j + 1
                        else:
                            break
                    else:
                        break
                for j in range(0, 4):
                    if not car.x + car.length + current_state.offset[i] + j >= 6:
                        if current_state.state[car.x + car.length + current_state.offset[i] + j][car.y] == '.':
                            current_state.offset[i] = current_state.offset[i] + j + 1
                            if str(current_state.offset) not in closed_list:
                                heappush(open_list, move_down(current_state, car, heuristic, i, cars, g=1, num_steps=j + 1))
                            current_state.offset[i] = current_state.offset[i] - j - 1
                        else:
                            break
                    else:
                        break
            closed_list.add(str(current_state.offset))
            if len(open_list) > 0:
                current_state = heappop(open_list)
            elif current_state.h > 0:
                solution = False
                break
        self.print_results('A_star', self.game, start, datetime.now(), current_state, len(closed_list), horizontal_cars[index_a], heuristic, index_a,
                    solution, horizontal_cars + vertical_cars)
    
