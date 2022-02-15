import turtle
from random import randint
import time



class DrawingTurtle(turtle.Turtle):
    def __init__(self):
        super().__init__(visible=False)
        self.speed(7)
        self.width(10)
        self.penup()
        self.drawing = False

    def reset_pos(self):
        self.penup()
        self.home()

    def draw_circle(self, coordinates: tuple[int | float, int | float]):
        self.goto(coordinates)
        self.forward(30)
        self.setheading(-270)
        self.pendown()
        self.circle(radius=40)

        self.reset_pos()

    def draw_cross(self, coordinates: tuple[int | float, int | float]):
        self.goto(coordinates)

        self.setheading(90 * 0.5)
        self.back(60)
        self.pendown()
        self.forward(120)

        self.penup()
        self.back(60)

        self.setheading(270 * 0.5)
        self.back(60)
        self.pendown()
        self.forward(120)

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

        if not functions_list:
            functions_list = [None for _ in range(len(self.turtles))]

        print(self.turtles)
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

    def mainloop(self):
        self.screen.mainloop()


class TicTacToe:

    def __init__(self):
        self.ui_manager = UiManager()
        self.ui_manager.setup_ui()

        # Setting Up key binds
        self.generate_onclick_functions(True)

        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
        ]

        self.players = {
            1: {"name": "Player 1", "symbol": "O"},
            2: {"name": "Player 2", "symbol": "X"}
        }

        # Randomly gives someone a turn
        self.prvs_player = randint(1, 2)

    def make_move(self, turtle_to_move_towards: turtle.Turtle, ind_to_make_move_at: tuple):

        if self.prvs_player == 2:
            current_player = self.players[1]
        else:
            current_player = self.players[2]

        coords_to_move_to = (turtle_to_move_towards.xcor(), turtle_to_move_towards.ycor())

        # Removes all The bindings so, User cannot click until shape is drawn
        # self.generate_onclick_functions(False)

        # {"is_game_over": game_over, "winner": winner}

        # Adds the player_symbol to the board
        self.board[ind_to_make_move_at[0]][ind_to_make_move_at[1]] = current_player["symbol"]

        if current_player["symbol"] == "O":
            self.ui_manager.drawing_turtle.draw_circle(coords_to_move_to)
            # changes the previous player
            self.prvs_player = 1

        else:
            self.ui_manager.drawing_turtle.draw_cross(coords_to_move_to)
            self.prvs_player = 2

        if self.did_game_end()["is_game_over"]:
            print("Game Ended")
            print(f"{self.players[self.prvs_player]['name']} Wins!")

        print(self.board)
        # Rebinds everything
        # self.generate_onclick_functions(True)


    def generate_onclick_functions(self, generate: bool):
        board_indexes = self.get_board_indexes()
        print(board_indexes)

        if not generate:
            funcs = None

        # change_onClick_methods
        else:
            # passes the turtles objects to make move_function so make_move can get then x and y cords

            x1 = lambda *_: self.make_move(self.ui_manager.turtles[0], board_indexes[0])  # board_indexes[0])
            x2 = lambda *_: self.make_move(self.ui_manager.turtles[1], board_indexes[1])  # board_indexes[1])
            x3 = lambda *_: self.make_move(self.ui_manager.turtles[2], board_indexes[2])  # board_indexes[2])
            x4 = lambda *_: self.make_move(self.ui_manager.turtles[3], board_indexes[3])  # board_indexes[3])
            x5 = lambda *_: self.make_move(self.ui_manager.turtles[4], board_indexes[4])  # board_indexes[4])
            x6 = lambda *_: self.make_move(self.ui_manager.turtles[5], board_indexes[5])  # board_indexes[5])
            x7 = lambda *_: self.make_move(self.ui_manager.turtles[6], board_indexes[6])  # board_indexes[6])
            x8 = lambda *_: self.make_move(self.ui_manager.turtles[7], board_indexes[7])  # board_indexes[7])
            x9 = lambda *_: self.make_move(self.ui_manager.turtles[8], board_indexes[8])  # board_indexes[8])

            funcs = [x1, x2, x3, x4, x5, x6, x7, x8, x9]

            # sleeps because Turtle draws in a Thread
            # time.sleep(1)

        # applies the new Functions
        self.ui_manager.change_onclick_methods(funcs)

    def x(self):
        self.x()


    @staticmethod
    def get_board_indexes() -> list:
        """
        Gets all The indexes of The Board and returns them as a list
        Like: [(0, 0), (0, 1), (0, 2)...etc]
        """

        coords = []
        cordx, cordy = (0, 0)

        # These lines in the if-statements are for all indexes in The board list
        for ind in range(9):
            if ind > 0:
                cordy += 1

                if ind % 3 == 0:
                    cordy = 0
                    cordx += 1

            coord = (cordx, cordy)
            coords.append(coord)

        return coords

    def did_game_end(self) -> dict[str, bool]:

        def are_values_clear(items: list | tuple, check_in=None) -> bool:
            """ 
            items: checks if all of them are same
            
            check_in:  If check in is none Checks in the item list
            Should be a List, It basically Goes in the list and checks if "" in the list
            If it does returns False, else Return True
            """

            li_to_checkin = check_in

            if not check_in:
                li_to_checkin = items

            if "" in li_to_checkin:
                return False

            """
            converts the list items to set(a set cannot have duplicate values)
            and returns if the len of the set is == 1 or not
            """
            return len(set(items)) == 1

        game_over = False

        # winner symbol will be The symbol that will be added if game is won
        winner_symbol = ""

        for board_row_ind, board_row in enumerate(self.board):
            # Loops Through The nested lists inside board, and their indexes

            if game_over:
                break

            # passes the board_row to the are_values_same lambda function above

            if are_values_clear(board_row):
                game_over = True
                winner_symbol = board_row[0]

            # If board_row_ind != 0 or game_over is True then we break
            if board_row_ind and game_over:
                game_over = True
                break

            for row_ind, item in enumerate(board_row):
                # temporary variables
                ri = row_ind
                bri = board_row_ind

                # Basically Goes Down The List, Gets Their items and Check if they are same
                x = [self.board[bri][ri], self.board[bri + 1][ri], self.board[bri + 2][ri]]

                print(x)

                if are_values_clear(
                    # below line basically does this board[bri][ri] == board[bri + 1][ri] == board[bri + 2][ri]
                    x,
                    check_in=board_row
                ):
                    winner_symbol = self.board[bri][ri]
                    game_over = True

                """ 
                if row_ind is 0, Checks Diagonally on The Right
                if it's 2 checks diagonally on the left 
                """
                if row_ind != 1:
                    ri_index: int = 1

                    if row_ind == 2:
                        ri_index = -1

                    i = (
                        self.board[bri][ri],
                        self.board[bri + 1][ri + 1 * ri_index],
                        # bri = nested_list: 1, 1
                        self.board[bri + 2][ri + 2 * ri_index],
                    )

                    if are_values_clear(i):
                        winner_symbol = i[0]
                        game_over = True
                        break

        if game_over:
            if winner_symbol == self.players[1]["symbols"]:
                winner = self.players[1]
            else:
                winner = self.players[2]

        else:
            winner = None

        return {"is_game_over": game_over, "winner": winner}


x = TicTacToe()
x.ui_manager.mainloop()
# print(x.get_board_indexes())

# x.setup_ui()
# x.mainloop()

quit()
#
# print('\n')
#
# board = [
#     ["", "", ""],
#     ["", "", ""],
#     ["", "", ""],
# ]
#
#
# def did_game_end() -> bool:
#     game_over = False
#
#     # winner symbol will be The symbol that will be checked if game is won
#     winner_symbol = ""
#
#     for board_row_ind, board_row in enumerate(board):
#         # Loops Through The nested lists inside board, and their indexes
#
#         if game_over:
#             # print('\nGame Over!')
#             break
#
#         if "" not in board_row and board_row[0] == board_row[1] == board_row[2]:
#             game_over = True
#             winner_symbol = board_row[0]
#
#         # If board_row_ind == 0 and game_over is False then we loop
#         if not board_row_ind and game_over is False:
#
#             for row_ind, item in enumerate(board_row):
#                 # Basically Goes Down The List, Gets Their items and Check if they are same
#                 if "" not in board_row and board[board_row_ind][row_ind] == board[board_row_ind + 1][row_ind] == \
#                         board[board_row_ind + 2][row_ind]:
#                     winner_symbol = board[board_row_ind][row_ind]
#                     game_over = True
#
#                 # temporary variables
#                 ri = row_ind
#                 bri = board_row_ind
#
#                 """
#                 if row_ind is 0, Checks Diagonally on The Right
#                 if it's 2 checks diagonally on the left
#                 """
#                 match row_ind:
#                     case 0:
#                         i = (
#                             board[bri][ri],
#                             board[bri + 1][ri + 1],
#                             # bri = nested_list: 1, 1
#                             board[bri + 2][ri + 2],
#                         )
#
#                     case 2:
#                         i = (
#                             board[bri][ri],
#                             board[bri + 1][ri - 1],
#                             board[bri + 2][ri - 2],
#                         )
#
#                 # print(f'\nELEMENTS:{bri}, {ri}')
#
#                 if "" not in i and i[0] == i[1] == i[2]:
#                     winner_symbol = i[0]
#                     game_over = True
#                     break
#
#     if game_over:
#         if winner_symbol == p1_symbol:
#             winner = "Player 1"
#         else:
#             winner = "Player 2"
#
#     else:
#         winner = None
#
#     return {"is_game_over": game_over, "winner": winner}
#
#
#
# print_board = lambda: [print(row) for row in board]
# format_choice = lambda item_to_format: [int(item) - 1 for item in item_to_format.split(',')]
#
# print("Welcome To Tic-Tac-Toe, Input data like this Eg: 1, 2")
# p1_symbol = "O"
# p2_symbol = "X"
#
# while True:
#     print_board()
#
#     if did_game_end()["is_game_over"]:
#         print_board()
#         break
#
#     p1_choice = format_choice(input("P1: "))
#
#     if did_game_end()["is_game_over"]:
#         print_board()
#         break
#
#     p2_choice = format_choice(input("P2: "))
#
#     board[p1_choice[0]][p1_choice[1]] = p1_symbol
#     board[p2_choice[0]][p2_choice[1]] = p2_symbol
#
#     print(p1_choice)
#     print(p2_choice)
