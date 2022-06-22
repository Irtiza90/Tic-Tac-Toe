from random import randint
from tkinter import messagebox
from functools import partial

from ui import UiManager, Turtle


class TicTacToe:
    def __init__(self):
        self.ui_manager = UiManager()
        self.ui_manager.setup_ui()

        self.board: list[list[str]] = [["", "", ""] for _ in range(3)]

        self.players = {
            1: {"name": "Player 1", "symbol": "O"},
            2: {"name": "Player 2", "symbol": "X"},
        }

        # Randomly gives someone a turn
        self.prvs_player = randint(1, 2)

        # Setting Up key binds
        self.generate_onclick_functions()

    def make_move(self, *_, turtle_to_move_towards: Turtle, ind_to_make_move_at: tuple) -> None:
        """
        Fires a Drawing event and draws a circle/cross(depending on the self.prvs_player)

        :param turtle_to_move_towards: a Turtle object that the drawing will be created at
        :param ind_to_make_move_at: a tuple object containing the row & col index(in self.board) for the current move
        :returns: None
        """
        if self.prvs_player == 2:
            current_player = self.players[1]
        else:
            current_player = self.players[2]

        coords_to_move_to: tuple[float, float] = turtle_to_move_towards.pos()

        # Adds the player_symbol to the board list
        self.board[ind_to_make_move_at[0]][ind_to_make_move_at[1]] = current_player["symbol"]

        if current_player["symbol"] == "O":
            self.ui_manager.drawing_turtle.draw_circle(coords_to_move_to)
            # changes the previous player
            self.prvs_player = 1

        else:
            self.ui_manager.drawing_turtle.draw_cross(coords_to_move_to)
            self.prvs_player = 2

        if self.did_game_end()["is_game_over"]:
            self.ui_manager.drawing_turtle.game_over = True
            str_to_ask = f"{self.players[self.prvs_player]['name']} Wins!\nWould You Like To Play Again?"

            if not messagebox.askyesno(title="Tic Tac Toe", message=str_to_ask):
                # if user says no we just exit the game
                quit()

            # else
            self.restart_game()

    def generate_onclick_functions(self):
        board_indexes = self.get_board_indexes()
        # change_onClick_methods
        # passes the turtles objects to make move_function so make_move can get then x and y cords

        funcs = [
            partial(
                self.make_move, turtle_to_move_towards=self.ui_manager.turtles[i], ind_to_make_move_at=board_indexes[i]
            ) for i in range(9)
        ]

        # applies the new Functions
        self.ui_manager.change_onclick_methods(funcs)

    def start_game(self):
        self.ui_manager.mainloop()

    def restart_game(self):
        self.board: list[list[str]] = [["", "", ""] for _ in range(3)]
        self.ui_manager.restart_game()

    def get_board_indexes(self) -> list[tuple]:
        """
        Gets all The indexes of The Board and returns them as a list
        Like: [(0, 0), (0, 1), (0, 2)...etc]
        """
        coords = []

        for ind, board_row in enumerate(self.board):
            for i in range(len(board_row)):
                coords.append((ind, i))

        return coords

    def did_game_end(self) -> dict[str, bool | str]:
        def list_is_valid(check_in: list | tuple):
            """
            :param check_in: The list to check items in
            :returns: True if there's no "" in list, and it's length is 1 else False
            """
            if "" not in check_in and len(set(check_in)) == 1:
                # Sets cannot store duplicate elements
                return True

            return False

        # --------------
        game_over = False
        winner, winner_symbol = None, None

        # Example List: [
        #   [1, 2, 3],
        #   [4, 5, 6],
        #   [7, 8, 9],
        # ]

        # according to example list above
        # pairs of diagonal_row_1 will be (1, 5, 9)
        diagonal_row_1 = [self.board[i][i] for i in range(3)]

        # Pairs of diagonal_row will be (3, 5, 7)
        diagonal_row_2 = [self.board[0][2], self.board[1][1], self.board[2][0]]

        if list_is_valid(diagonal_row_1):
            game_over = True
            winner_symbol = diagonal_row_1[0]

        if list_is_valid(diagonal_row_2):
            game_over = True
            winner_symbol = diagonal_row_2[0]

        # Checking downwards
        # pairs according to above example list will be (1, 4, 7), (2, 5, 8), (3, 6, 9)
        for row in zip(*self.board):
            if list_is_valid(row):
                game_over = True
                winner_symbol = row[0]

        for board_row in self.board:
            # Checking Each row from left to right
            # pairs according to example_list: (1, 2, 3), (4, 5, 6), (7, 8, 9)
            if list_is_valid(board_row):
                game_over = True
                winner_symbol = board_row[0]

        if game_over:
            if winner_symbol == self.players[1]["symbol"]:
                winner = self.players[1]
            else:
                winner = self.players[2]

        else:
            winner = None

            # Checks if all the board is filled, But no one wins
            if not any("" in row for row in self.board):
                game_over = True
                winner = "draw"

        return {"is_game_over": game_over, "winner": winner}


if __name__ == "__main__":
    TicTacToe().start_game()
