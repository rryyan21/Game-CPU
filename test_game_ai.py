import numpy as np
from typing import List, Tuple

class GameState:
    def __init__(self, board_size: int = 8):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size))
        
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Returns list of valid moves in current state."""
        valid_moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.is_valid_move(i, j):
                    valid_moves.append((i, j))
        return valid_moves
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """Checks if a move is valid."""
        # Example validation - customize based on game rules
        return self.board[row][col] == 0

    def make_move(self, row: int, col: int):
        """Executes a move and updates game state."""
        if self.is_valid_move(row, col):
            self.board[row][col] = 1
            return True
        return False

class GameAI:
    def __init__(self, search_depth: int = 3):
        self.search_depth = search_depth

    def evaluate_state(self, state: GameState) -> float:
        """Evaluates how good the current state is for the AI."""
        # Implement game-specific evaluation logic
        return np.sum(state.board)  # Simple example

    def minimax(self, state: GameState, depth: int, maximizing: bool) -> Tuple[float, Tuple[int, int]]:
        """Implements minimax algorithm for move selection."""
        if depth == 0:
            return self.evaluate_state(state), None

        valid_moves = state.get_valid_moves()
        if not valid_moves:
            return self.evaluate_state(state), None

        best_move = valid_moves[0]
        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                new_state = GameState(state.board_size)
                new_state.board = state.board.copy()
                new_state.make_move(*move)
                eval, _ = self.minimax(new_state, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_state = GameState(state.board_size)
                new_state.board = state.board.copy()
                new_state.make_move(*move)
                eval, _ = self.minimax(new_state, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def get_best_move(self, state: GameState) -> Tuple[int, int]:
        """Returns the best move for the current state."""
        _, best_move = self.minimax(state, self.search_depth, True)
        return best_move
    

# test code:
def print_board(board):
    """Pretty prints the game board"""
    for row in board:
        print(" ".join(["X" if cell == 1 else "." for cell in row]))
    print()

def main():
    # Create a new game state
    game = GameState(board_size=4)  # Using smaller board for demo
    ai = GameAI(search_depth=3)
    
    # Simulate a few moves
    print("Starting game board:")
    print_board(game.board)
    
    for i in range(5):  # Make 5 moves
        # Get AI's move
        best_move = ai.get_best_move(game)
        if best_move:
            row, col = best_move
            game.make_move(row, col)
            print(f"AI Move {i+1}: Placed at position ({row}, {col})")
            print_board(game.board)
        else:
            print("No valid moves available")
            break

if __name__ == "__main__":
    main()