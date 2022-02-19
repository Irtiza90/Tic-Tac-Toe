import turtle
from random import randint
from time import sleep
from tkinter import messagebox


class DrawingTurtle(turtle.Turtle):
    def __init__(self):
        super().__init__(visible=False)
        self.speed(10)
        self.width(10)
        self.penup()

        self.game_over = False

    def reset_pos(self):
        self.penup()
        self.home()

    def draw_circle(self, coordinates: tuple[int | float, int | float]):
        if self.game_over:
            return

        self.goto(coordinates)
        self.forward(30)
        self.setheading(-270)
        self.pendown()
        self.circle(radius=40)

        self.reset_pos()

    def draw_cross(self, coordinates: tuple[int | float, int | float]):
        if self.game_over:
            return

        self.goto(coordinates)
        pos = 90

        for i in range(2):
            self.setheading(pos * 0.5)
            self.back(60)
            self.pendown()
            self.forward(120)

            if not i:  # if i = 0
                self.penup()
                self.back(60)
                pos *= 3  # 90 * 3 = 270

        self.reset_pos()


class UiManager:
    def __init__(self):

        # Setting Up the Screen
        self.screen = turtle.Screen()
        self.screen.setup(width=652, height=645)
        self.screen.title("Tic Tac Toe")

        self.drawing_turtle = DrawingTurtle()

        self.all_coordinates = []
        self.turtles = []

    @staticmethod
    def create_turtles(
            turtle_to_clone: turtle.Turtle,
            amount_of_copies: int,
            del_original=False
    ):
        """
        Clones given Turtle in the range of amount of copies required
        coordinates are a tuple that should be given to func
        Coords are for Turtles positions in which they will move llater on
        del_original Basically deletes Drawings of The original Turtle given
        """
        turtles = []

        for _ in range(amount_of_copies):
            cloned_t = turtle_to_clone.clone()
            turtles.append(cloned_t)

        if del_original:
            turtle_to_clone.clear()
            turtle_to_clone.hideturtle()

        return turtles

    def setup_ui(self):
        # Making The Grid Turtle, That will be cloned
        grid_t = turtle.Turtle(shape="square")
        grid_t.speed("fastest")
        grid_t.color("white")
        grid_t.penup()
        grid_t.shapesize(stretch_wid=10, outline=0)

        # Creates all the positions for Grids

        for i in range(-1, 2):
            for j in range(-1, 2):
                index = (j * 220, i * 220 * -1)
                self.all_coordinates.append(index)

        # cordx, cordy = (0, 0)

        # creates Turtles
        self.turtles = self.create_turtles(grid_t, 9, del_original=True)

        for ind, turtle_ in enumerate(self.turtles):
            # Getting the Turtles to their positions
            turtle_goto_pos = self.all_coordinates[ind]

            turtle_.goto(turtle_goto_pos)
            # turtle_.onclick(functions[ind])

        # calls the draw_lines function
        self.draw_lines()

    def change_onclick_methods(self, functions_list: list | None):
        """
        takes one argument "functions_list"
        if it is None Removes all The Click Bindings Otherwise
        Adds Click Binds to the Button
        """

        for ind, turtle_ in enumerate(self.turtles):
            turtle_.onclick(functions_list[ind])

    def draw_lines(self):
        """
        This function will Only be used by the setup_ui function
        """
        line1 = turtle.Turtle(shape="square", visible=False)
        line1.penup()
        line1.speed(8)

        # Creating The Turtles, that will drawy lines
        line_turtles = self.create_turtles(line1, 4, del_original=True)

        heading = -90

        coordinates = [
            (-320, -110),
            (-110, -320),
            (320, 110),
            (110, 320),
        ]

        # loops Through the Line turtles Created above, moves them and draws 4 lines
        for ind, turtle_ in enumerate(line_turtles):
            coordinate_to_goto = coordinates[ind]
            heading += 90

            turtle_.goto(coordinate_to_goto)
            turtle_.setheading(heading)

            turtle_.pendown()
            turtle_.width(20)

            turtle_.forward(650)

    def restart_game(self):
        self.drawing_turtle.game_over = False
        self.drawing_turtle.clear()

    def mainloop(self):
        try:
            self.screen.mainloop()
        except KeyboardInterrupt: 
            pass


class TicTacToe:

    def __init__(self):
        self.ui_manager = UiManager()
        self.ui_manager.setup_ui()

        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
        ]

        self.players = {
            1: {"name": "Player 1", "symbol": "O"},
            2: {"name": "Player 2", "symbol": "X"},
        }
        
        # Randomly gives someone a turn
        self.prvs_player = randint(1, 2)
          
        # Setting Up key binds
        self.generate_onclick_functions()

    
    def make_move(self, turtle_to_move_towards: turtle.Turtle, ind_to_make_move_at: tuple):
        
        if self.prvs_player == 2:
            current_player = self.players[1]
        else:
            current_player = self.players[2]

        coords_to_move_to = (turtle_to_move_towards.xcor(), turtle_to_move_towards.ycor())


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
        
        # These Methods Don't work        
        # funcs = []
        # for i in range(9):
        #     funcs.append(lambda *_: self.make_move(self.ui_manager.turtles[i], board_indexes[i]))
        
        # funcs = [
        #     lambda *_: self.make_move(self.ui_manager.turtles[i], board_indexes[i]) 
        #     for i in range(9)
        # ]
        
        x1 = lambda *_: self.make_move(self.ui_manager.turtles[0], board_indexes[0])
        x2 = lambda *_: self.make_move(self.ui_manager.turtles[1], board_indexes[1])
        x3 = lambda *_: self.make_move(self.ui_manager.turtles[2], board_indexes[2])
        x4 = lambda *_: self.make_move(self.ui_manager.turtles[3], board_indexes[3])
        x5 = lambda *_: self.make_move(self.ui_manager.turtles[4], board_indexes[4])
        x6 = lambda *_: self.make_move(self.ui_manager.turtles[5], board_indexes[5])
        x7 = lambda *_: self.make_move(self.ui_manager.turtles[6], board_indexes[6])
        x8 = lambda *_: self.make_move(self.ui_manager.turtles[7], board_indexes[7])
        x9 = lambda *_: self.make_move(self.ui_manager.turtles[8], board_indexes[8])

        funcs = [x1, x2, x3, x4, x5, x6, x7, x8, x9]

        # applies the new Functions
        self.ui_manager.change_onclick_methods(funcs)


    def start_game(self):
        self.ui_manager.mainloop()

    def restart_game(self):
        self.board = [
            ["" for _ in range(3)]
            for _ in range(3)
        ]

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

        return {"is_game_over": game_over, "winner": winner}



game = TicTacToe()
game.start_game()
