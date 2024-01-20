import time


class Sudoku:
    """
    A class to represent a Sudoku puzzle and solve it using a backtracking algorithm.

    Attributes:
    -----------
    board : list[list[int]]
        A 9x9 grid representing the Sudoku board, where 0 represents an empty cell.
    steps : int
        Counter to track the number of steps (recursive calls) taken to solve the puzzle.
    """

    def __init__(self, board):
        """
        Initializes the Sudoku object with a given board.

        Parameters:
        ----------
        board : list[list[int]]
            A 9x9 grid of integers representing the Sudoku puzzle.
            Here we're using nested lists to represent the grid.

        Raises:
        ------
        ValueError:
            If the input board is not a 9x9 grid of integers from 0 to 9.
        """
        if not self.is_valid_input(board):
            raise ValueError("Board must be a 9x9 grid of integers from 0 to 9.")
        self.board = board
        self.steps = 0

    def is_valid_input(self, board):
        """
        Checks if the given board is a valid 9x9 Sudoku grid.

        Parameters:
        ----------
        board : list[list[int]]
            The Sudoku board to be validated.

        Returns:
        -------
        bool
            True if the board is valid, False otherwise.
        """
        if len(board) != 9 or any(len(row) != 9 for row in board):
            return False
        return all(all(isinstance(num, int) and 0 <= num <= 9 for num in row) for row in board)

    def is_valid_move(self, row, col, num):
        """
        Checks if placing a number in a specified row and column is valid.

        Parameters:
        ----------
        row : int
            Row index where the number is to be placed.
        col : int
            Column index where the number is to be placed.
        num : int
            The number to be placed.

        Returns:
        -------
        bool
            True if the move is valid, False otherwise.
        """
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num or \
                    self.board[row - row % 3 + i // 3][col - col % 3 + i % 3] == num:
                return False
        return True

    def find_least_candidates_cell(self):
        """
        Finds the cell with the least number of possible candidates.

        Returns:
        -------
        tuple or None
            The row and column indices of the cell, or None if no empty cell is found.
        """
        min_candidates = 10
        cell = None
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    candidates = sum(self.is_valid_move(i, j, num) for num in range(1, 10))
                    if candidates < min_candidates:
                        min_candidates = candidates
                        cell = (i, j)
        return cell

    def solve(self):
        """
        Solves the Sudoku puzzle using a backtracking algorithm.

        We do this by:
        1. Selecting an empty cell with the least number of possible candidates.
        2. Place each valid number (1-9) in the selected cell.
        3. After placing a number, we call it recursively to solve the rest of the board.
        4. If the recursive call finds that the current board configuration leads to a dead-end,
           we backtrack it by resetting the cell to 0 (empty) and tries the next number.
        5. This process continues until either the board is successfully filled (solution found),
           or no solution exists with the current board configuration.
        6. If no solution is found, this might become an infinite loop...

        Returns:
        -------
        bool
            True if the puzzle is solved, False otherwise.
        """
        self.steps += 1
        cell = self.find_least_candidates_cell()
        if not cell:
            return True  # If no empty cell is found, the puzzle is solved

        row, col = cell
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True  # If the puzzle is solved, return True
                self.board[row][col] = 0  # Backtrack: reset the cell and try the next number

        return False  # If no number leads to a solution, return False

    def print_board(self):
        """
        Prints the current state of the Sudoku board using string formatting.
        """
        for i, row in enumerate(self.board):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")
            print(" ".join(str(num) if num != 0 else '.' for num in row[:3]) + " | " +
                  " ".join(str(num) if num != 0 else '.' for num in row[3:6]) + " | " +
                  " ".join(str(num) if num != 0 else '.' for num in row[6:]))

    def print_steps(self):
        """
        Prints the total number of steps taken to solve the Sudoku puzzle.
        """
        print(f"Total steps taken: {self.steps}")


# Example usage
board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
start = time.time()
sudoku = Sudoku(board)
if sudoku.solve():
    sudoku.print_board()
    sudoku.print_steps()
else:
    print("No solution exists")
print(time.time() - start)
