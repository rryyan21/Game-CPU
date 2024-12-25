import numpy as np
from typing import List, Tuple

class GameState:
    def __init__(self, board_size: int = 4):
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
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            return False
        return self.board[row][col] == 0

    def make_move(self, row: int, col: int, player_value: int):
        """Executes a move and updates game state."""
        if self.is_valid_move(row, col):
            self.board[row][col] = player_value
            return True
        return False
    
    def check_winner(self) -> int:
        """Check if there's a winner. Returns player number or 0 for no winner."""
        # Check rows
        for row in self.board:
            if np.all(row == 1):
                return 1
            if np.all(row == 2):
                return 2

        # Check columns
        for col in self.board.T:
            if np.all(col == 1):
                return 1
            if np.all(col == 2):
                return 2

        # Check diagonals
        diag1 = np.diagonal(self.board)
        diag2 = np.diagonal(np.fliplr(self.board))
        if np.all(diag1 == 1) or np.all(diag2 == 1):
            return 1
        if np.all(diag1 == 2) or np.all(diag2 == 2):
            return 2

        return 0

class GameAI:
    def __init__(self, search_depth: int = 3):
        self.search_depth = search_depth

    def evaluate_state(self, state: GameState) -> float:
        """Evaluates how good the current state is for the AI."""
        winner = state.check_winner()
        if winner == 2:  # AI wins
            return 100
        elif winner == 1:  # Player wins
            return -100
        return 0

    def minimax(self, state: GameState, depth: int, maximizing: bool) -> Tuple[float, Tuple[int, int]]:
        """Implements minimax algorithm for move selection."""
        winner = state.check_winner()
        if winner == 2:
            return 100, None
        elif winner == 1:
            return -100, None
        elif depth == 0:
            return self.evaluate_state(state), None

        valid_moves = state.get_valid_moves()
        if not valid_moves:
            return 0, None

        best_move = valid_moves[0]
        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                new_state = GameState(state.board_size)
                new_state.board = state.board.copy()
                new_state.make_move(*move, 2)
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
                new_state.make_move(*move, 1)
                eval, _ = self.minimax(new_state, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def get_best_move(self, state: GameState) -> Tuple[int, int]:
        """Returns the best move for the current state."""
        _, best_move = self.minimax(state, self.search_depth, True)
        return best_move

def print_board(board):
    """Pretty prints the game board"""
    print("\n  0 1 2 3")  # Column numbers
    for i, row in enumerate(board):
        print(f"{i}", end=" ")  # Row numbers
        for cell in row:
            if cell == 0:
                print(".", end=" ")
            elif cell == 1:
                print("O", end=" ")  # Player
            else:
                print("X", end=" ")  # AI
        print()
    print()

def get_player_move(game_state: GameState) -> Tuple[int, int]:
    """Gets and validates player move."""
    while True:
        try:
            row = int(input("Enter row (0-3): "))
            col = int(input("Enter column (0-3): "))
            if game_state.is_valid_move(row, col):
                return row, col
            else:
                print("Invalid move! Cell is either occupied or out of bounds. Try again.")
        except ValueError:
            print("Please enter numbers between 0 and 3.")

def main():
    game = GameState(board_size=4)
    ai = GameAI(search_depth=3)
    
    print("\nWelcome to Tic-Tac-Toe!")
    print("You are O, AI is X")
    print("Enter row and column numbers to make your move.")
    print_board(game.board)
    
    while True:
        # Player's turn
        row, col = get_player_move(game)
        game.make_move(row, col, 1)
        print("\nYour move:")
        print_board(game.board)
        
        # Check if player won
        if game.check_winner() == 1:
            print("Congratulations! You won!")
            break
        
        # Check if board is full
        if not game.get_valid_moves():
            print("It's a tie!")
            break
            
        # AI's turn
        print("AI is thinking...")
        ai_move = ai.get_best_move(game)
        if ai_move:
            row, col = ai_move
            game.make_move(row, col, 2)
            print(f"AI moves at position ({row}, {col})")
            print_board(game.board)
            
            # Check if AI won
            if game.check_winner() == 2:
                print("AI wins! Better luck next time!")
                break
                
            # Check if board is full
            if not game.get_valid_moves():
                print("It's a tie!")
                break
        else:
            print("No valid moves available")
            break

    print("Game Over!")

if __name__ == "__main__":
    main()