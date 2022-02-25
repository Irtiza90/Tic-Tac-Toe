from turtle import Turtle, Screen


class DrawingTurtle(Turtle):
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
        self.screen = Screen()
        self.screen.setup(width=652, height=645)
        self.screen.title("Tic Tac Toe")

        self.drawing_turtle = DrawingTurtle()

        self.all_coordinates = []
        self.turtles = []

    @staticmethod
    def create_turtles(
            turtle_to_clone: Turtle,
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
        grid_t = Turtle(shape="square")
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
        line1 = Turtle(shape="square", visible=False)
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

    
    def get_turtle_coords(self, turtle_obj: Turtle) -> tuple[float, float]:
        "Returns the x and y coordinates of a Turtle object, as a tuple (x, y)"
        return (turtle_obj.xcor(), turtle_obj.ycor())
    
    
    def restart_game(self):
        self.drawing_turtle.game_over = False
        self.drawing_turtle.clear()

    def mainloop(self):
        try:
            self.screen.mainloop()
        except KeyboardInterrupt: 
            pass
