from random import randint
from tkinter import messagebox
from ui import UiManager


class TicTacToe:

    def __init__(self):
        self.ui_manager = UiManager()
        self.ui_manager.setup_ui()

        self.board = [[""] * 3] * 3

        self.players = {
            1: {"name": "Player 1", "symbol": "O"},
            2: {"name": "Player 2", "symbol": "X"},
        }
        
        # Randomly gives someone a turn
        self.prvs_player = randint(1, 2)
          
        # Setting Up key binds
        self.generate_onclick_functions()

    
    def make_move(self, turtle_to_move_towards, ind_to_make_move_at: tuple):
        
        if self.prvs_player == 2:
            current_player = self.players[1]
        else:
            current_player = self.players[2]

        # coords_to_move_to = (turtle_to_move_towards.xcor(), turtle_to_move_towards.ycor())
        coords_to_move_to = self.ui_manager.get_turtle_coords(turtle_to_move_towards)

        # Adds the player_symbol to the board list
        self.board[ind_to_make_move_at[0]][ind_to_make_move_at[1]] = current_player["symbol"]

        if current_player["symbol"] == "O":
            self.ui_manager.drawing_turtle.draw_circle(coords_to_move_to)
            # changes the previous player
            self.prvs_player = 1

        else:
            self.ui_manager.drawing_turtle.draw_cross(coords_to_move_to)
            self.prvs_player = 2

        did_game_end = self.did_game_end()
        
        if did_game_end["is_game_over"]:
            
            winner_name = self.players[self.prvs_player]['name']
            self.ui_manager.drawing_turtle.game_over = True
            str_to_ask = f"{winner_name} Wins!\nWould You Like To Play Again?"
            
            if did_game_end["winner"] == "draw":
                str_to_ask = "Draw!\nWould You Like To Play Again?"
            
            
            if not messagebox.askyesno(title="Tic Tac Toe", message=str_to_ask):
                # if user says no we just exit the game
                quit()

            # else
            self.restart_game()
    
    def generate_onclick_functions(self):
        board_indexes = self.get_board_indexes()

        # change_onClick_methods
        # passes the turtles objects to make move_function so make_move can get then x and y cords

        funcs = [lambda *_, i=i: self.make_move(self.ui_manager.turtles[i], board_indexes[i]) for i in range(9)]

        # applies the new Functions
        self.ui_manager.change_onclick_methods(funcs)


    def start_game(self):
        self.ui_manager.mainloop()

    def restart_game(self):
        self.board = [[""] * 3] * 3

        # calling The ui Manager's Restart game method
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

    def did_game_end(self) -> dict[str, bool]:

        def are_values_clear(items: list | tuple) -> bool:
            """
            items: checks if all of them are same
            Should be a List, It basically Goes in the list and checks if "" in the list
            If it does returns False, else Return True (if all values are equal)
            """

            if "" in items:
                return False

            """
            converts the list items to set(a set cannot have duplicate values)
            and returns if the len of the set is == 1 or not
            """
            return len(set(items)) == 1

        winner_symbol = None
        game_over = False


        for board_row_ind, board_row in enumerate(self.board):
            if game_over:
                break

            # passes all full board row like this ["", "", ""] and checks if they are same
            if are_values_clear(board_row):
                """
                This checks all the nested rows inside the board list
                These ones : [ 
                    ["0", "X", ""], Checks from left to right
                    ["X", "X", ""], on all these nested rows
                    ["0", "X", ""]
                ]
                and goes from left to right and checks if they are same, If they are then game is over
                """
                game_over = True
                winner_symbol = board_row[0]


            if board_row_ind == 0 and game_over is False:

                for row_col_ind in range(len(board_row)):
                    # row_col ind is the indexes of the nested row(inside the board), That we get from above loop

                    # This Line Goes down the Nested Lists, and checks it with the current row_col_ind

                    if are_values_clear([
                        self.board[i][row_col_ind] for i in range(3)
                    ]):
                        winner_symbol = self.board[board_row_ind][0]
                        game_over = True
                        break

                    # --------------- Diagonal Checking  ---------------------------- #
                    """
                    if row_ind is 0, Checks Diagonally on The Right
                    if it's 2 checks diagonally on the left
                    """

                    if row_col_ind != 1:
                        multiply_by = 1

                        if row_col_ind == 2:
                            multiply_by = -1

                        if are_values_clear(
                                [self.board[i][row_col_ind + (i * multiply_by)] for i in range(3)]
                        ):
                            winner_symbol = self.board[board_row_ind][row_col_ind]
                            game_over = True
                            break


        if game_over:
            if winner_symbol == self.players[1]["symbol"]:
                winner = self.players[1]
            else:
                winner = self.players[2]

        else:
            winner = None
            # Checks if all of the board is filled, But no one wins
            li = []

            for row in self.board:
                for item in row:
                    li.append(item)
            
            if "" not in li:
                game_over = True
                winner = "draw"


        return {"is_game_over": game_over, "winner": winner}



game = TicTacToe()
game.start_game()
