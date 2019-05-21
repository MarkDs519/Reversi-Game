# Written by .......
# Student Id .......


def new_board():
    """
    This function creates a new 8 by 8 reversi board.
    :return: reversi board
    """
    # initiating the number of rows and columns
    rows = 8
    cols = 8
    # initiating an empty board for the time being
    board = []
    empty = 0
    # defining the stones
    black = 1
    white = 2
    # design the board based on the number of rows and columns
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(empty)    # insert zeros for every element initiating that the board is empty
        board.append(row)

    # defining the starting positions
    board[3][3] = white
    board[4][3] = black
    board[3][4] = black
    board[4][4] = white

    return board

def print_board(board):
    """
    This function allows displaying the board on the console
    :param board: the reversi board
    :return: a board to visualize
    """
    # initiating the number of rows and columns
    rows = 8
    cols = 8
    horizontal_border = '------+---+---+---+---+---+---+---+---'
    vertical_border = '  |   |   |   |   |   |   |   |   |'
    # designing the board
    for i in range(rows):
        print(vertical_border)
        print(i + 1, end=' ')
        for j in range(cols):
            print('| %s' % (board[i][j]), end=' ')
        print('|')
        print(vertical_border)
        print(horizontal_border)
    print('    a   b   c   d   e   f   g   h')

def score_board(board):
    """
    This function calculates the score of the players
    :param board: reversi board
    :return: score
    """
    # initiating the scores as 0 initially
    s1 = 0
    s2 = 0
    # initiating the stones
    black = 1
    white = 2
    # calculating the score
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == black:
                s1 += 1
            if board[x][y] == white:
                s2 += 1

    return (s1,s2)

def isValidCoordinate(x, y):
    """
    This function checks whether the coordinates entered are valid
    :param x: x coordinate
    :param y: y coordinate
    :return: boolean result
    """
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def enclosing(board, player, pos, direct):
    """
    This function takes checks whether putting a player's stone on
    a given position would enclose a straight line of opponent's stones in a given direction.
    :param board: reversi board
    :param player: the person playing
    :param pos: the position the player intends to place the stone
    :param direct: the direction in which the stone targets
    :return: boolean result
    """
    # picking out the x and y coordinates
    x_coordinate = pos[0]
    y_coordinate = pos[1]
    # selecting the x and y directions
    x_direction = direct[0]
    y_direction = direct[1]

    # Check for valid coordinates.
    if board[x_coordinate][y_coordinate] != 0 or not isValidCoordinate(x_coordinate, y_coordinate):
        return False
    # set the player marker on the board temporarily.
    board[x_coordinate][y_coordinate] = player
    # initiate the player and its opponent
    if player == 1:
        opponent = 2
    else:
        opponent = 1

    stones_to_change = []   # initiating an empty list to represent the number of stones to flip
    x, y = x_coordinate, y_coordinate

    # set the coordinates to the direction as initiated
    x += x_direction
    y += y_direction
    # check whether the new coordinates are valid or not. In addition, check if the new position contains the
    # opponents stone
    if isValidCoordinate(x, y) and board[x][y] == opponent:
        # if there is, move to the next cell
        x += x_direction
        y += y_direction
        # keep on checking the number of opponents stone
        while board[x][y] == opponent:
            x += x_direction
            y += y_direction
            # loop until we reach the end
            if not isValidCoordinate(x, y):  # break out of while loop, then continue in for loop
                break
        if board[x][y] == player:
            # go in the reverse direction now as we found all the stones of the opponent which needs to flip
            while True:
                x -= x_direction
                y -= y_direction
                # came back to the original position
                if x == x_coordinate and y == y_coordinate:
                    break
                # add the coordinates where the stones needs to be flipped
                stones_to_change.append([x, y])

    board[x_coordinate][y_coordinate] = 0
    # if no stones where flipped,then the length of the list will be 0.
    if len(stones_to_change) == 0:
        return False
    else:
        return True


def check_valid_move(board, player, x_coordinate, y_coordinate):
    """
    This function checks whether the move the player intends to make, is a valid move or not
    :param board: reversi board
    :param player: person playing the turn
    :param x_coordinate: x
    :param y_coordinate: y
    :return: boolean and a list of all possible valid moves
    """

    # Check for valid coordinates.
    if board[x_coordinate][y_coordinate] != 0 or not isValidCoordinate(x_coordinate, y_coordinate):
        return False

    # set the player marker on the board temporarily.
    board[x_coordinate][y_coordinate] = player
    # initiate the player and its opponent
    if player == 1:
        opponent = 2
    else:
        opponent = 1
    # all possible directions
    directions_list = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    stones_to_change = []
    # iterate over all the directions to seek all possible moves
    for xdirect, ydirect in directions_list:
        x, y = x_coordinate, y_coordinate
        x += xdirect
        y += ydirect
        # check whether the new coordinates are valid or not. In addition, check if the new position contains the
        # opponents stone
        if isValidCoordinate(x, y) and board[x][y] == opponent:
            x += xdirect
            y += ydirect
            if not isValidCoordinate(x, y):
                continue
            # keep on checking the number of opponents stone
            while board[x][y] == opponent:
                x += xdirect
                y += ydirect
                if not isValidCoordinate(x, y):
                    break
            if not isValidCoordinate(x, y):
                continue
            if board[x][y] == player:
                # now move in the reverse direction
                while True:
                    x -= xdirect
                    y -= ydirect
                    if x == x_coordinate and y == y_coordinate:
                        break
                    stones_to_change.append([x, y])

    board[x_coordinate][y_coordinate] = 0
    # If no stones were flipped, then it is not considered as a valid move
    if len(stones_to_change) == 0:
        return False
    return stones_to_change

def valid_moves(board, player):
    """
    This function returns all possible valid moves
    :param board: reversi board
    :param player: player
    :return: list of valid moves
    """
    # list containing all the possible moves
    list_of_valid_moves = []
    # loop through the board to find all the valid moves
    for i in range(len(board)):
        for j in range(len(board)):
            # if any valid moves are found then insert then in the list as a tuple
            if check_valid_move(board, player, i, j) is not False:
                list_of_valid_moves.append((i, j))
    return list_of_valid_moves

def next_state(board, player, pos):
    """
    This function checks if the position is valid and then makes the move
    :param board: reversi board
    :param player: player playing
    :param pos: position to put the stone
    :return: updated board and the opponent
    """
    # initiating the players
    if player == 1:
        opponent = 2
    else:
        opponent = 1

    x_cor = pos[0]
    y_cor = pos[1]
    # check if valid move
    is_valid_move = check_valid_move(board, player, x_cor, y_cor)
    if is_valid_move is False:
        return False
    # if it is a valid move, update the board and include the position of the new stone
    else:
        board[x_cor][y_cor] = player
        for x, y in is_valid_move:
            board[x][y] = player

    return (board, opponent)

def position(string):
    """
    This function takes a position of the cell in the board as a string and converts it as a coordinate.
    :param string: cell position
    :return: coordinate
    """
    # list of columns
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    # check whether the string is of length 2
    if len(string) == 2:
        char = string[0]
        # check whether the char is a decimal value or not, if it is, then return None
        if char.isdigit():
            return None
        else:
            number = string[1]
            # check whether the 2nd string value is a number or not
            if number.isdigit():
                number = int(number)
            else:
                return None
            # iterate over the alphabets to find the index of the character
            for i in range(len(cols)):
                # check if the co0ordinate is valid or not and also whether the character belongs in cols list
                if cols[i] == char and isValidCoordinate(number-1, i):
                    coordinate = (number-1, i)
                    return coordinate
    else:
        return None

def convert_all_possible_moves_to_string(all_possible_moves):
    """
    This function takes a list of all the moves and converts them into string patterns for easy visualization
    :param all_possible_moves: list of moves
    :return: cells positions in strings
    """
    # empty list to store all the cells positions
    moves_list = []
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    # iterate over the list and convert them into strings
    for moves in all_possible_moves:
        x = moves[0]
        y = moves[1]
        for i in range(len(cols)):
            if i == y:
                moves_list.append(cols[i]+str(x+1))
    return moves_list

def run_two_players():
    """
    This function allows the functionality of two players to play at once.
    :return:
    """
    print("YOU SELECTED MULTIPLAYER")
    print("")

    while True:
        # board
        reversi_board = new_board()
        # display the board
        print_board(reversi_board)
        # display the score
        print("Current score: ", score_board(reversi_board))
        print("")
        while True:
            # asking for user input
            player = input("Enter which players turn , or type q to end the game: ")
            while player != '1' and player != 'q' and player != '2':
                print("INCORRECT INPUT. PLEASE TRY AGAIN!")
                player = input("Enter which players turn , or type q to end the game: ")
            # if the player chooses to quit
            if player == 'q':
                print("You quit")
                break
            else:
                player = int(player)
                # all possible valid moves
                all_valid_moves = valid_moves(reversi_board, player)
                # convert the coordinates to strings for easy visualization
                moves = convert_all_possible_moves_to_string(all_valid_moves)
                print("All possible valid moves: ", moves)
                # if no valid moves left, then end the game and return the final score
                if len(all_valid_moves) == 0:
                    print("No more valid moves for either player. ")
                    break
                # drop a position in the board
                pos = input("Enter your position to drop the stone: ")
                coordinates = position(pos)
                # if the drop pos is not valid
                while not check_valid_move(reversi_board, player, coordinates[0], coordinates[1]):
                    print("Invalid Move. Try again!")
                    pos = input("Enter your position to drop the stone: ")
                    coordinates = position(pos)
                # if valid, place the move on the board
                stone_position = (coordinates[0], coordinates[1])
                # make the move
                updated_board, opponent = next_state(reversi_board, player, stone_position)
                # make the new updated board as the reversi board
                reversi_board = updated_board
                print_board(reversi_board)
                # display the score
                print("Score: ", score_board(reversi_board))
        # computation of the final score
        score = score_board(reversi_board)
        # return who won and who lost
        if score[0] > score[1]:
            print("Player 1 won the game with a score of %d to %d " % (score[0], score[1]))
        elif score[0] == score[1]:
            print("It's a tie.")
        else:
            print("Player 2 won the game with a score of %d to %d " % (score[1], score[0]))
        # requesting player if he/she wants to play the game again
        play_again = input("Do you want to play again? If yes, press y. If no, press n: ")
        if play_again == 'y':
            continue
        else:
            break


def is_corner(x, y):
    """
    Checking whether the coordinates are corner positions of the board
    :param x:
    :param y:
    :return:
    """
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def duplicate_board(board):
    """
    Make a copy of the board
    :param board: reversi board
    :return: duplicate board
    """
    board_copy = new_board()
    # copy all the cells of the new board to the duplicate board
    i = 0
    while i < len(board):
        j = 0
        while j < len(board):
            board_copy[i][j] = board[i][j]
            j += 1
        i += 1
    return board_copy

def find_best_move_computer(board, computer):
    """
    This function allows to find the best possible move for the computer
    :param board: reversi board
    :param computer: computer
    :return: best move
    """
    # compute all possible moves
    all_moves = valid_moves(board, computer)
    # if no valid moves left, return and invalid coordinate
    if len(all_moves) == 0:
        print("No more valid moves for either player. ")
        return (-1,-1)
    # iterate over the positions and check whether there are any corner positions. Corners are the best options.
    for x_cor, y_cor in all_moves:
        if is_corner(x_cor, y_cor):
            return (x_cor, y_cor)

    # initiate a best score
    best_score = -1
    # iterate over all the moves and store the best move for maximum score
    for x, y in all_moves:
        copy_of_board = duplicate_board(board)
        # make the move
        next_state(copy_of_board, computer, (x,y))
        score = score_board(copy_of_board)
        # check the current score with the previous score
        if score[1] > best_score:
            best_possible_move = (x, y)
            best_score = score[1]
    return best_possible_move


def run_single_player():
    """
    This function allows the player to play against the computer
    :return:
    """
    print("YOU SELECTED SINGLE PLAYER")
    print("")

    while True:
        # board
        reversi_board = new_board()
        # diplay the board
        print_board(reversi_board)
        # compute the current score
        print("Current score: ", score_board(reversi_board))
        print("")
        # initiate the player and the computer
        player_1 = 1
        computer = 2
        while True:
            # asking for user input
            player = input("Enter turn , or type q to end the game: ")
            while player != '1' and player != 'q' and player != '2':
                print("INCORRECT INPUT. PLEASE TRY AGAIN!")
                player = input("Enter which players turn , or type q to end the game: ")
            # if the player chooses to quit
            if player == 'q':
                print("You quit")
                break
            elif int(player) == player_1:
                player = int(player)
                # all possible valid moves
                all_valid_moves = valid_moves(reversi_board, player)
                # convert the coordinates to strings for easy visualization
                moves = convert_all_possible_moves_to_string(all_valid_moves)
                print("All possible valid moves: ", moves)
                # if no valid moves left, then end the game and return the final score
                if len(all_valid_moves) == 0:
                    print("No more valid moves for either player. ")
                    break
                # drop a position in the board
                pos = input("Enter your position to drop the stone: ")
                coordinates = position(pos)
                # if the drop pos is not valid
                while not check_valid_move(reversi_board, player, coordinates[0], coordinates[1]):
                    print("Invalid Move. Try again!")
                    pos = input("Enter your position to drop the stone: ")
                    coordinates = position(pos)
                # if valid, place the move on the board
                stone_position = (coordinates[0], coordinates[1])
                updated_board, opponent = next_state(reversi_board, player, stone_position)
                reversi_board = updated_board
                print_board(reversi_board)
                print("Score: ", score_board(reversi_board))
            # if it is the turn of the computer
            else:
                best_move = find_best_move_computer(reversi_board, computer)
                # if no possible moves, then break
                if best_move[0] == -1 and best_move[1] == -1:
                    break
                next_board, opponent = next_state(reversi_board, computer, best_move)
                reversi_board = next_board
                print_board(reversi_board)
                print("Score: ", score_board(reversi_board))
        # compute the score
        score = score_board(reversi_board)
        # find who won and who lost and also is it a tie
        if score[0] > score[1]:
            print("Player 1 won the game with a score of %d to %d " % (score[0], score[1]))
        elif score[0] == score[1]:
            print("It's a tie.")
        else:
            print("Computer won the game with a score of %d to %d " % (score[1], score[0]))
        # requesting player if he/she wants to play the game again
        play_again = input("Do you want to play again? If yes, press y. If no, press n: ")
        if play_again == 'y':
            continue
        else:
            break


def run():
    """This function allows to run the whole game"""
    print("WELCOME TO REVERSI")

    print("Choose which category you want to play in.")
    while True:
        try:
            category = int(input("Press 1 for single player and 2 for multiplayer: "))
        except ValueError:
            print("INCORRECT INPUT. PLEASE TRY AGAIN!")
            continue

        if category == 1:
            run_single_player()
            break
        else:
            run_two_players()
            break

if __name__ == "__main__":
     run()
