def generateSample():
    board = list([['.','.','.','.','.','.'],['.','.','.','.','.','.'],['.','.','.','.','.','.'],
                      ['.','.','.','.','.','.'],['.','.','.','.','.','.'],['.','.','.','.','.','.']])
    occupied = 2
    index_a = random.randint(0, 3)
    board[2][index_a:index_a+2] = ["A", 'A']
    num_cars = random.randint(8, 14)
    count = 0
    names = "BCDEFGHIJKLMNOP"
    while count < num_cars and occupied < 30:
        length = random.randint(2, 3)
        orientation = random.randint(0, 1)
        if orientation == 0:
            x = random.randint(0, 6 - length)
            y = random.randint(0, 5)
            free = True
            for i in range(0, length):
                if not board[x+i][y] == '.':
                    free = False
            if not free:
                continue
            for i in range(0,length):
                board[x+i][y] = names[count]
            count += 1
            occupied += length
        else:
            x = random.randint(0, 5)
            y = random.randint(0, 6 - length)
            if x == 2 and y > index_a:
                continue
            free = True
            for i in range(0, length):
                if not board[x][y+i] == '.':
                    free = False
            if not free:
                continue
            board[x][y:y + length] = [names[count]] * length
            count += 1
            occupied += length
    return board
