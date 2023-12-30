import tkinter as tk

class Visualizer:
    def __init__(self, grid, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.grid = grid
        self.cell_size = 80
        self.canvas = tk.Canvas(self.root, width=self.grid.columns * self.cell_size, height=self.grid.rows * self.cell_size)
        self.canvas.pack()
        self.draw()
        self.root.mainloop()

    def draw(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.columns):
                cell = self.grid.grid[i][j]
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                color = "white" if not cell.hidden else "grey"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

