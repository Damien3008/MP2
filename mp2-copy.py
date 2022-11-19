from heapq import *
import itertools
from datetime import datetime
import copy


class State:
    def __init__(self, state, parent, offset, fuel_offset, heuristic=1, last_move=("Z", 0, 0)):
        self.last_move = last_move
        self.parent = parent
        self.offset = offset
        self.state = state
        self.fuel_offset = fuel_offset
        if heuristic == 1:
            self.score = h(state, 1)
        elif heuristic == 2:
            self.score = h(state, 2)
        else:
            self.score = h(state, 3, 3)

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
        return str(self.state).replace(" ", "").replace("'", "").replace(",", "").replace("[", "").replace("]", "")


class Car:

    def __init__(self, name, orientation, length, x, y, fuel=100):
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

    def __str__(self):
        return  self.name + ", " + self.orientation


def print_results(start, end, finishing_state, state_counter, ambulance, heuristic, index_a, solution, cars):
    fuel_levels = ""
    for car in cars:
        fuel_levels = fuel_levels + car.name + ": " + str(car.fuel) + " "
    if not solution:
        print("no solution")
        print(fuel_levels + "\n")
        print(int(state_counter))
        return
    current = finishing_state
    solution = ""
    solution_path = ""
    solution_counter = 0

    while current.parent is not None:
        solution_counter += 1
        if current.last_move[0].orientation == "H":
            if current.last_move[1] == -1:
                solution_path = current.last_move[0].name + " left; " + solution_path
                solution = current.last_move[0].name + " left\t\t" + str(current.last_move[2]) + "\t" + str(current) + "\n" + solution
            else:
                solution_path = current.last_move[0].name + " right; " + solution_path
                solution = current.last_move[0].name + " right\t\t" + str(current.last_move[2]) + "\t"+ str(current) + "\n" + solution
        else:
            if current.last_move[1] == -1:
                solution_path = current.last_move[0].name + " up; " + solution_path
                solution = current.last_move[0].name + " up\t\t" + str(current.last_move[2]) + "\t"+ str(current) + "\n"+ solution
            else:
                solution_path = current.last_move[0].name + " down; " + solution_path
                solution = current.last_move[0].name + " down\t\t" + str(current.last_move[2]) + "\t" + str(current) + "\n" + solution
        current = current.parent
    move_a = 5 - ambulance.y - finishing_state.offset[index_a] - ambulance.length + 1
    while move_a > 0:
        solution_counter += 1
        finishing_state = move_right(finishing_state, ambulance, heuristic, index_a)
        solution = solution + ambulance.name + " right\t\t" + str(ambulance.fuel + finishing_state.fuel_offset[index_a]) + "\t" + str(current) + "\n"
        solution_path = solution_path + ambulance.name + " right; "
        move_a = move_a - 1
    print("Initial Board Configuration: " + str(current) + "\n")
    for item in current.state:
        print(str(item).replace(", ", "").replace("[", "").replace("]", "").replace("'", ""))
    print("\n")
    print(fuel_levels + "\n")
    print("Runtime: " + str((end - start).total_seconds()) + " seconds")
    print("Search path length: " + str(state_counter) + " states")
    print("Solution path length: " + str(solution_counter) + " moves")
    print("Solution path: " + solution_path)
    print("\n")
    print(solution)
    for item in finishing_state.state:
        print(str(item).replace(", ", "").replace("[", "").replace("]", "").replace("'", ""))


def h(state, heuristic=1, alpha=1):
    value = 0
    count = False
    counted = list()
    for i in range(0, 6):
        current = state[2][i]
        if current == 'A':
            count = True
        elif count and current != '.' and current not in counted:
            value += 1
            if not heuristic == 2:
                counted.append(current)
    if heuristic == 3:
        return value * alpha
    else:
        return value


def extract_game(input):
    board = list()
    input_arrayed = [*input]
    for i in range(0, 6):
        board.append(input_arrayed[0 + 6 * i:6 + 6 * i])
    return board


def move_right(current_state, car, heuristic, i):
    new_offset = copy.deepcopy(current_state.offset)
    new_offset[i] = new_offset[i] + 1
    new_state = copy.deepcopy(current_state.state)
    for j in range(0, car.length):
        new_state[car.x][car.y + 1 + current_state.offset[i] + j] = car.name
    new_state[car.x][car.y + current_state.offset[i]] = "."
    new_fuel_offset = copy.deepcopy(current_state.fuel_offset)
    new_fuel_offset[i] = new_fuel_offset[i] - 1
    return State(new_state, current_state, new_offset, new_fuel_offset, heuristic, (car, 1, car.fuel + new_fuel_offset[i]))


def move_left(current_state, car, heuristic, i):
    new_offset = copy.deepcopy(current_state.offset)
    new_offset[i] = new_offset[i] - 1
    new_state = copy.deepcopy(current_state.state)
    for j in range(0, car.length):
        new_state[car.x][car.y - 1 + current_state.offset[i] + j] = car.name
    if not car.y + current_state.offset[i] + car.length - 1 >= 6:
        new_state[car.x][car.y + current_state.offset[i] + car.length - 1] = "."
    new_fuel_offset = copy.deepcopy(current_state.fuel_offset)
    new_fuel_offset[i] = new_fuel_offset[i] - 1
    return State(new_state, current_state, new_offset, new_fuel_offset, heuristic, (car, -1, car.fuel + new_fuel_offset[i]))


def move_down(current_state, car, heuristic, i):
    new_offset = copy.deepcopy(current_state.offset)
    new_offset[i] = new_offset[i] + 1
    new_state = copy.deepcopy(current_state.state)
    for j in range(0, car.length):
        new_state[car.x + 1 + current_state.offset[i] + j][car.y] = car.name
    new_state[car.x + current_state.offset[i]][car.y] = "."
    new_fuel_offset = copy.deepcopy(current_state.fuel_offset)
    new_fuel_offset[i] = new_fuel_offset[i] - 1
    return State(new_state, current_state, new_offset,new_fuel_offset, heuristic, (car, 1, car.fuel + new_fuel_offset[i]))


def move_up(current_state, car, heuristic, i):
    new_offset = copy.deepcopy(current_state.offset)
    new_offset[i] = new_offset[i] - 1
    new_state = copy.deepcopy(current_state.state)
    for j in range(0, car.length):
        new_state[car.x - 1 + current_state.offset[i] + j][car.y] = car.name
    if not car.x + current_state.offset[i] + car.length - 1 >= 6:
        new_state[car.x + current_state.offset[i] + car.length - 1][car.y] = "."
    new_fuel_offset = copy.deepcopy(current_state.fuel_offset)
    new_fuel_offset[i] = new_fuel_offset[i] - 1
    return State(new_state, current_state, new_offset, new_fuel_offset, heuristic, (car, -1, car.fuel + new_fuel_offset[i]))


def gbfs(game, fuel, heuristic=1, alpha=1):
    start = datetime.now()
    solution = True
    cnt=0
    open_list = []
    closed_list = list()
    board = extract_game(game)
    state_board = copy.deepcopy(board)
    horizontal_cars = list()
    vertical_cars = list()
    index_a = 0
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
                    horizontal_cars.append(Car(current, "H", k - j, i, j, int(fuel[current])))
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
                    vertical_cars.append(Car(current, "V", k - i, i, j, int(fuel[current])))
    offset = [0] * (len(horizontal_cars) + len(vertical_cars))
    fuel_offset = [0] * (len(horizontal_cars) + len(vertical_cars))
    current_state = State(state_board, None, offset, fuel_offset, heuristic)
    while current_state.score > 0:
        # Generate all possible children
        for i in range(0, len(horizontal_cars)):
            car = horizontal_cars[i]
            if car.fuel + current_state.fuel_offset[i] <= 0:
                continue
            if not car.y + current_state.offset[i] == 0:
                if current_state.state[car.x][car.y - 1 + current_state.offset[i]] == '.':
                    child_state = move_left(current_state, car, heuristic, i)
                    if child_state.offset not in closed_list:
                        heappush(open_list, child_state)
                    else:
                        print(str(cnt))
                        cnt += 1
            if not car.y + car.length + current_state.offset[i] >= 6:
                if current_state.state[car.x][car.y + car.length + current_state.offset[i]] == '.':
                    child_state = move_right(current_state, car, heuristic, i)
                    if child_state.offset not in closed_list:
                        heappush(open_list, child_state)
                    else:
                        print(str(cnt))
                        cnt += 1
        for i in range(len(horizontal_cars), len(vertical_cars) + len(horizontal_cars)):
            car = vertical_cars[i - len(horizontal_cars)]
            if car.fuel + current_state.fuel_offset[i] <= 0:
                continue
            if not car.x + current_state.offset[i] == 0:
                if current_state.state[car.x - 1 + current_state.offset[i]][car.y] == '.':
                    child_state = move_up(current_state, car, heuristic, i)
                    if child_state.offset not in closed_list:
                        heappush(open_list, child_state)
                    else:
                        print(str(cnt))
                        cnt += 1
            if not car.x + car.length + current_state.offset[i] >= 6:
                if current_state.state[car.x + car.length + current_state.offset[i]][car.y] == '.':
                    child_state = move_down(current_state, car, heuristic, i)
                    if child_state.offset not in closed_list:
                        heappush(open_list, child_state)
                    else:
                        print(str(cnt))
                        cnt += 1
        closed_list.append(current_state.offset)
        if len(open_list) > 0:
            current_state = heappop(open_list)
        elif current_state.score > 0:
            solution = False
            break
    print_results(start, datetime.now(), current_state, len(closed_list), horizontal_cars[index_a], heuristic, index_a,
                  solution, horizontal_cars + vertical_cars)


class Rush_Hour_Search:
    '''
    This class will contain all the implementations of algorithms for the resolution of the Rush Hour problem
    '''

    def __init__(self, input_file='input2.txt', select_game='all'):
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
                # print(len(game.split(' ')))
                if len(game.split(' ')) != 1:
                    for j in range(1, len(game.split(' '))):
                        for i in range(len(game.split(' ')[j]) - 1):
                            if len(game.split(' ')[j][i]) == 1 and game.split(' ')[j][i + 1] == ' ':
                                dict_fuel[game.split(' ')[j][i]] = 100
                            else:
                                dict_fuel[game.split(' ')[j][i]] = game.split(' ')[j][i + 1]

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
            return dict(
                itertools.islice(dict_games.items(), int(self.select_game) - 1, int(self.select_game))), tot_fuel[
                                                                                                         int(self.select_game) - 1: int(
                                                                                                             self.select_game)]

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


r = Rush_Hour_Search(select_game='all')
dict_games, dict_fuel = r.read_file()
for a in range(0, len(dict_fuel)):
    print("\nGame " + str(a+1) + ": \n")
    gbfs(dict_games["Game" + str(a + 1)], dict_fuel[a])

