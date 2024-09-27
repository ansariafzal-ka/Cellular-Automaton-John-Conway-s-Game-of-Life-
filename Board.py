import tkinter as tk
import numpy as np
from Rules import get_next_state

class Board:
    def __init__(self, ROWS, COLS, CELL_SIZE, title="New Board"):
        self.array = np.zeros((ROWS, COLS))
        self.ROWS = ROWS
        self.COLS = COLS
        self.CELL_SIZE = CELL_SIZE

        self.WHITE_COLOR = "#fff"
        self.GRAY_COLOR = "#4a4949"
        self.BLACK_COLOR = "#000"

        self.WINDOW_WIDTH = self.COLS * self.CELL_SIZE
        self.WINDOW_HEIGHT = self.ROWS * self.CELL_SIZE

        self.mouse_x = 0
        self.mouse_y = 0

        self.grid_visible = False
        self.coordinates_visible = False
        self.game_running = False
        self.paused = False

        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.window.title(title)

        self.btn_frame = tk.Frame(self.window, width=self.WINDOW_WIDTH, height=50, bg=self.BLACK_COLOR, border=1)
        self.btn_frame.pack()

        self.btn_start_pause = tk.Button(self.btn_frame, text="Start", command=self.start_pause_game)
        self.btn_start_pause.grid(row=0, column=0)

        self.btn_grid = tk.Button(self.btn_frame, text="Toggle Grid", command=self.toggle_grid_lines)
        self.btn_grid.grid(row=0, column=1)

        self.btn_coordinates = tk.Button(self.btn_frame, text="Toggle Coordinates", command=self.toggle_mouse_coordinates)
        self.btn_coordinates.grid(row=0, column=2)

        self.btn_clear = tk.Button(self.btn_frame, text="Clear Canvas", command=self.clear_canvas)
        self.btn_clear.grid(row=0, column=3)

        self.btn_randomize = tk.Button(self.btn_frame, text="Randomize", command=self.randomize_board)
        self.btn_randomize.grid(row=0, column=4)

        self.canvas = tk.Canvas(self.window, width=self.WINDOW_WIDTH - 1, height=self.WINDOW_HEIGHT - 1, bg=self.BLACK_COLOR)
        self.canvas.pack()

        self.mouse_coordinates_label = tk.Label(self.canvas, text=f"x: {self.mouse_x}, y: {self.mouse_y}", foreground=self.WHITE_COLOR, background=self.BLACK_COLOR)
        self.mouse_coordinates_label.place(x=-50, y=-50)

        self.mouse_coordinates()

        self.canvas.bind("<Button-1>", self.fill_cell_on_click)
        self.canvas.bind("<Button-3>", self.remove_cell_on_click)

        self.update_interval = 10

    def start(self):
        self.window.mainloop()

    def clear_canvas(self):
        self.grid_visible = False
        self.array = np.zeros((self.ROWS, self.COLS))
        self.canvas.delete("all")

    def grid_lines(self):
        if self.grid_visible:
            for i in range(self.ROWS):
                line_id = self.canvas.create_line(0, self.CELL_SIZE * i, self.WINDOW_WIDTH, self.CELL_SIZE * i, fill=self.GRAY_COLOR, tags="grid_line")
            for j in range(self.COLS):
                line_id = self.canvas.create_line(self.CELL_SIZE * j, 0, self.CELL_SIZE * j, self.WINDOW_HEIGHT, fill=self.GRAY_COLOR, tags="grid_line")
        else:
            self.clear_grid_lines()

    def toggle_grid_lines(self):
        self.grid_visible = not self.grid_visible
        self.grid_lines()

    def clear_grid_lines(self):
        self.canvas.delete("grid_line")

    def fill_cell(self, row, col, color):
        self.canvas.create_rectangle(col * self.CELL_SIZE, row * self.CELL_SIZE, 
                                      (col * self.CELL_SIZE) + self.CELL_SIZE, 
                                      (row * self.CELL_SIZE) + self.CELL_SIZE, 
                                      fill=color)

    def fill_cell_on_click(self, event):
        row = event.y // self.CELL_SIZE
        col = event.x // self.CELL_SIZE
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            self.array[row][col] = 1
            self.fill_cell(row, col, self.WHITE_COLOR)

    def remove_cell_on_click(self, event):
        row = event.y // self.CELL_SIZE
        col = event.x // self.CELL_SIZE
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            self.array[row][col] = 0
            self.fill_cell(row, col, self.BLACK_COLOR)

    def clear_cell(self, row, col):
        self.fill_cell(row, col, self.BLACK_COLOR)

    def start_pause_game(self):
        if not self.game_running:
            self.game_running = True
            self.paused = False
            self.btn_start_pause.config(text="Pause")
            self.update_board()
        else:
            self.paused = not self.paused
            if self.paused:
                self.btn_start_pause.config(text="Start")
            else:
                self.btn_start_pause.config(text="Pause")
                self.update_board()

    def update_board(self):
        if self.game_running and not self.paused:
            self.array = get_next_state(self.array)
            self.redraw_board()
            self.window.after(self.update_interval, self.update_board)

    def redraw_board(self):
        self.canvas.delete("all")
        self.grid_lines()
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.array[row, col] == 1:
                    self.fill_cell(row, col, self.WHITE_COLOR)

    def randomize_board(self):
        self.array = np.random.choice([0, 1], size=(self.ROWS, self.COLS), p=[0.7, 0.3])
        self.redraw_board()

    def mouse_coordinates(self):
        self.canvas.bind("<Motion>", lambda event: self.update_mouse_coordinates(event))

    def show_mouse_coordinates(self):
        if self.coordinates_visible:
            self.mouse_coordinates_label.place(x=self.mouse_x, y=self.mouse_y - 30)
            self.mouse_coordinates_label.config(text=f"(row: {self.mouse_y // self.CELL_SIZE}, col: {self.mouse_x // self.CELL_SIZE})")
        else:
            self.mouse_coordinates_label.place(x=-50, y=-50)

    def toggle_mouse_coordinates(self):
        self.coordinates_visible = not self.coordinates_visible
        self.show_mouse_coordinates()

    def update_mouse_coordinates(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
        self.show_mouse_coordinates()
