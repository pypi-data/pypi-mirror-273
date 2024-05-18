import time

# Module
class TicTacToeAI:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_winner = None

    def print_board(self):
        for row in self.board[:-1]:
            print(" | ".join(row))
            print("-" * 9)
        print(" | ".join(self.board[-1]))
        print("\n")

    def available_moves(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]

    def empty_squares(self):
        return " " in (sq for row in self.board for sq in row)

    def num_empty_squares(self):
        return len(self.available_moves())

    def make_move(self, square, letter):
        if self.board[square[0]][square[1]] == " ":
            self.board[square[0]][square[1]] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind, col_ind = square
        row = self.board[row_ind]
        if all([s == letter for s in row]):
            return True
        col = [self.board[r][col_ind] for r in range(3)]
        if all([s == letter for s in col]):
            return True
        if row_ind == col_ind:
            diagonal1 = [self.board[i][i] for i in range(3)]
            if all([s == letter for s in diagonal1]):
                return True
        if row_ind + col_ind == 2:
            diagonal2 = [self.board[i][2 - i] for i in range(3)]
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def minimax(self, state, depth, max_player):
        if self.current_winner == "O":
            return {"position": None, "score": 1 * (depth + 1)}
        elif self.current_winner == "X":
            return {"position": None, "score": -1 * (depth + 1)}
        elif not self.empty_squares():
            return {"position": None, "score": 0}

        if max_player:
            best = {"position": None, "score": -float("inf")}
            letter = "O"
        else:
            best = {"position": None, "score": float("inf")}
            letter = "X"

        for possible_move in self.available_moves():
            self.make_move(possible_move, letter)
            sim_score = self.minimax(state, depth + 1, not max_player)
            self.board[possible_move[0]][possible_move[1]] = " "
            self.current_winner = None
            sim_score["position"] = possible_move

            if max_player:
                if sim_score["score"] > best["score"]:
                    best = sim_score
            else:
                if sim_score["score"] < best["score"]:
                    best = sim_score

        return best

    def get_ai_move(self):
        if self.num_empty_squares() == 9:
            square = (0, 0)
        else:
            time.sleep(0.3)  # Add a delay of 0.3 seconds before AI responds
            square = self.minimax(self.board, 0, True)["position"]
        return square

    def play(self):
        while True:
            self.board = [[" " for _ in range(3)] for _ in range(3)]
            self.current_winner = None
            self.print_board()
            letter = "X"
            while self.empty_squares():
                if letter == "O":
                    square = self.get_ai_move()
                    print(f"AI moves to position {square[0] * 3 + square[1] + 1}")
                else:
                    valid_square = False
                    while not valid_square:
                        user_input = input("Enter your move (1-9): ")
                        try:
                            val = int(user_input) - 1
                            row, col = val // 3, val % 3
                            if self.board[row][col] == " ":
                                valid_square = True
                                square = (row, col)
                            else:
                                print("Invalid move. Try again.")
                        except ValueError:
                            print("Invalid input. Enter a number between 1 and 9.")

                self.make_move(square, letter)
                if self.current_winner:
                    self.print_board()
                    if self.current_winner == "O":
                        print("AI wins!")
                    else:
                        print("You win!")
                    break
                letter = "O" if letter == "X" else "X"
                self.print_board()

            if not self.empty_squares() or self.current_winner:
                choice = input("Press 0 to start another game or any other key to exit: ")
                if choice == "0":
                    continue
                else:
                    break