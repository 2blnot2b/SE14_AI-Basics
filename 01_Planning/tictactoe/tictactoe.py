"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_turn = 0
    O_turn = 0

    # In an i x j matrix, i is the row and j is the column
    for i in board:
        for j in i:
            if j == X:
                X_turn += 1
            elif j == O:
                O_turn += 1

    # Whenever the game is not over or X is as many as O on the board
    if not terminal(board) and X_turn == O_turn:
        return X
    # O turn always second, so whenever X's are more than O's, its O's turn
    elif X_turn > O_turn:
        return O

    # Otherwise the game is over
    return None

def moves(board):
    """
    Returns set of all possible moves (i, j) available on the board.
    """

    # All possible moves saved in a sequence (dtype = set)
    sequence = set()

    # Iterating over each entries (ith row, jth col)
    for i in range(len(board)):
        for j in range(len(board)):

            # Only if the square is empty, we conclude it as a possible move
            if board[i][j] == EMPTY:
                sequence.add((i, j))
    return sequence

def result(board, move):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Assigning the first element of the set sequence to "i" which is the index for the row
    # and the second element to "j" which is for the col
    (i, j) = move

    # Checking for invalid input (move) or no more move possible!
    if move not in moves(board):
        raise ValueError("move not valid!")
    elif terminal(board):
        raise ValueError("Game's over!")
    elif i < len(board) and j < len(board) and board[i][j] == EMPTY:

        # The original board will be copied for analysis purpose by our algorithm
        result_board = copy.deepcopy(board)
        ply = player(board)

        # Then we assign both i and j to the player's board to be explored
        result_board[i][j] = ply
        return result_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Checking for winner in a horizontal line
    for row in range(len(board)):
        if board[row][0] == board[row][1] == board[row][2] != None:
            if board[row][0] == X:
                return X
            return O

    # Checking for winner in a vertical line
    for col in range(len(board)):
        if board[0][col] == board[1][col] == board[2][col] != None:
            if board[0][col] == X:
                return X
            return O

    # Checking for winner in a diagonal line:
    # Firstly, we check from top right to bot left
    if board[0][0] == board[1][1] == board[2][2] != None:
        if board[1][1] == X:
            return X
        return O

    # Secondly, we check from top right to bot left
    elif board[0][2] == board[1][1] == board[2][0] != None:
        if board[1][1] == X:
            return X
        return O

    # Otherwise, it's a draw!
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # We have a winner
    if winner(board) != None:
        return True

    # Checking for all filled squares to determine if the game is over or not
    for row in board:
        for col in row:
            if col == EMPTY:
                return False

    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # X won
    if winner(board) == X:
        return 1
    
    # O won
    elif winner(board) == O:
        return -1

    # Draw!
    return 0
