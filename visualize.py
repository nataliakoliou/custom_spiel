import tkinter as tk

class Visualizer:
    def __init__(self, grid, title=None, size=80):
        self.grid = grid
        self.title = title
        self.size = size
        self.root = tk.Tk()
        self.config()
        self.draw()
        self.root.mainloop()

    def config(self):
        self.root.title(self.title)
        self.canvas = tk.Canvas(self.root, width=self.grid.columns * self.size, height=self.grid.rows * self.size)
        self.canvas.pack()

    def draw(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.columns):
                cell = self.grid.grid[i][j]
                x0, y0 = j * self.size, i * self.size
                x1, y1 = x0 + self.size, y0 + self.size
                color = "white" if not cell.hidden else "grey"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")