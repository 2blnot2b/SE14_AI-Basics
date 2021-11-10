from tictactoe import *
import math
import time

def minimax(board):
    """
    Returns the optimal move for the agent based on all search tree possible.
    """

    # Evaluate if the game has ended
    if terminal(board):
        return None

    # Best possible move for the AI as X and as O
    opt_move = None

    def max_val(board, depth):
        """
        Return the highest possible value and the total searched leaf nodes.
        """

        # Always check the state of the board
        if terminal(board):
            return utility(board), depth+1

        # The worst possible starting value for finding the max value is the negative infinity (lowest value)
        val = -math.inf

        for move in moves(board):

            # Assigning the best/highest possible value from the possbile move left
            best_val, depth = min_val(result(board, move), depth)
            val = max(val, best_val)

        return val, depth+1

    def min_val(board, depth):
        """
        Return the lowest possible value and the total searched leaf nodes.
        """

        # Always check the state of the board
        if terminal(board):
            return utility(board), depth+1

        # The worst possible starting value for finding the minimum value is the positive infinity (highest value)
        val = math.inf

        for move in moves(board):

            # Assigning the best/lowest possible value from all possible move left
            best_val, depth = max_val(result(board, move), depth)
            val = min(val, best_val)

        return val, depth+1

    # AI is MAX player
    if player(board) == X:
        # Start counting the time complexity for minimax algorithm
        start = time.time()
        
        # Worst possible value for MAX player is "LOWEST VALUE"
        val = -math.inf

        for move in moves(board):

            # Choosing the best value for MAX player which is between the worst possible value and the value chosen by MIN player in each iteration
            best_val, depth = min_val(result(board, move), 0)

            # Compare the previous best value with the new value from the current iteration
            if best_val >= val:

                # Assigning best value and its related move as the most optimal move (or move) for the MAX player (or X) in each iteration
                val = best_val
                opt_move = move

        # Output describes one of the performance criterias of Minimax algorithm; Time complexity
        end = time.time()

        print(f"\n<<< MINIMAX Time Complexity 'O(b^m)': {round(end - start, 13)} >>>\n")
        print(f"<<< Total explored states: {depth} >>>")

    # AI is MIN player
    else:
        # Start counting the time complexity for minimax algorithm
        start = time.time()

        # Worst possible value for MIN player is "HIGHEST VALUE"
        val = math.inf
        for move in moves(board):

            # Choosing the best value for MIN player which is between the worst possible value and the value chosen by MAX player in each iteration
            best_val, depth = max_val(result(board, move), 0)

            # Compare the previous best value with the new value from the current iteration
            if best_val <= val:

                # Assigning best value and its related move as the most optimal move (or move) for the MIN player (or O) in each iteration
                val = best_val
                opt_move = move

        # Output describes one of the performance criterias of Minimax algorithm; Time complexity
        end = time.time()

        print(f"\n<<< MINIMAX Time Complexity 'O(b^m)': {round(end - start, 13)} >>>\n")
        print(f"<<< Total explored states: {depth} >>>")

    # Output is the most optimal move/move
    return opt_move
