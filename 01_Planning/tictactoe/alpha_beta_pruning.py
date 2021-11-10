from tictactoe import *
import math
import time

def alpha_beta_pruning(board):
    """
    Returns the optimal move for the agent by ignoring portions of the search tree that make no difference to the optimal move.
    """

    # Evaluate if the game has ended
    if terminal(board):
        return None

    # Alpha value or "at least"
    alpha = -math.inf

    # Beta value or "at most"
    beta = math.inf

    # Best possible move for the AI as X (MAX) or as O (MIN)
    opt_move = set()

    def max_alpha_beta(board, alpha, beta, depth):
        """
        Returns the highest possible value and the total searched leaf nodes.        
        """

        # Always check the state of the board
        if terminal(board):
            return utility(board), depth+1

        val = -math.inf
        for move in moves(board):

            # Searching for the "HIGH VALUE" for MAX
            best_val, depth = min_alpha_beta(result(board, move), alpha, beta, depth)
            val =  max(val, best_val)

             # Val represents the current "HIGH VALUE" from the above iteration and Beta represents the last chosen "LOW VALUE" of MIN player
            if val >= beta:
                return val, depth+1
            
            # If the current "HIGH VALUE" is lower than the "LOW VALUE", than find the best possible value between the current value and the Alpha value from last iteration
            alpha = max(alpha, val)
        return  alpha, depth+1

    def min_alpha_beta(board, alpha, beta, depth):
        """
        Returns the lowest possible value and the total searched leaf nodes.        
        """

        # Always check the state of the board
        if terminal(board):
            return utility(board), depth+1

        val = math.inf
        for move in moves(board):

            # Searching for the "LOW VALUE" for MIN
            best_val, depth = max_alpha_beta(result(board, move), alpha, beta, depth)
            val = min(val, best_val)

            # Val represents the current "LOW VALUE" from the above iteration and Alpha represents the last chosen "HIGH VALUE" of MAX player
            if val <= alpha:
                return val, depth+1

            # If the current "LOW VALUE" is higher than the "HIGH VALUE", than find the best possible value between the current value and the Beta value from last iteration
            beta = min(beta, val)
        return beta, depth+1

    # AI is MAX player
    if player(board) == X:

        # Start counting the time complexity for minimax algorithm
        start = time.time()

        # Worst possible value for a max player is negative infinity or the lowest value for MIN
        val = -math.inf

        for move in moves(board):

            # Choosing the best/highest value for MAX player based on the value chosen by MIN player in the last move
            best_val, depth = min_alpha_beta(result(board, move), alpha, beta, 0)

            # The value always comes with 1 specific move option and this will be the best possible move for the MAX player
            if best_val > val:
                val = best_val
                opt_move = move

        # Output describes one of the performance criterias of Alpha-Beta Pruning algorithm; Time complexity
        end = time.time()
        print(f"\n<<< Alpha-Beta Pruning Time Complexity 'O(b^m/2)': {round(end - start, 13)} >>>\n")
        print(f"<<< Total explored states: {depth} >>>")

    else: # AI is MIN player
        # Start counting the time complexity for minimax algorithm
        start = time.time()

        # Worst possible value for a max player is negative infinity or the highest value for MAX
        val = math.inf

        for move in moves(board):

            # Choosing the best/lowest value for MIN player based on the value chosen by MAX player in the last move
            best_val, depth = max_alpha_beta(result(board, move), alpha, beta, 0)

            # The value always comes with 1 specific move option and this will be the best possible move for the MIN player
            if best_val < val:
                val = best_val
                opt_move = move

        # Output describes one of the performance criterias of Alpha-Beta Pruning algorithm; Time complexity
        end = time.time()
        print(f"\n<<< Alpha-Beta Pruning Time Complexity 'O(b^m/2)': {round(end - start, 13)} >>>\n")
        print(f"<<< Total explored states: {depth} >>>")

    # Output is the most optimal move
    return opt_move
