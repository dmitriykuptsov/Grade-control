import tkinter as tk
from tkinter import Tk, Canvas, Frame, BOTH
import datetime
import sys
import os

class Canvas():
    def __init__(self, width, height, xmin, ymin, xmax, ymax, n, graphics):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.width = width
        self.height = height
        self.xscale = width / (xmax - xmin)
        self.yscale = height / (ymax - ymin)
        if (xmax - xmin) > (ymax - ymin):
            self.grid_size = (ymax - ymin) / n * self.yscale
        else:
            self.grid_size = (xmax - xmin) / n * self.xscale
        self.scale = self.xscale
        if self.yscale < self.xscale:
            self.scale = self.yscale
        self.n = n
        self.graphics = graphics

    def draw_grid(self):
        for i in range(0, self.n):
            self.graphics.draw_line(i*self.grid_size, 0, i*self.grid_size, self.height, width=1)
        
        for i in range(0, self.n):
            self.graphics.draw_line(0, i*self.grid_size, self.width, i*self.grid_size, width=1)
    
    def draw_line(self, p1, p2, width=5, color = "black"):
        self.graphics.draw_line(p1.x * self.scale, p1.y * self.scale, p2.x * self.scale, p2.y * self.scale, width, color)
    
    def draw_block(self, p1, p2, color):
        self.graphics.draw_square(p1.x * self.scale, p1.y * self.scale, p2.x * self.scale, p2.y * self.scale, color)

    def draw_text(self, p1, text, width=5, color="red"):
        self.graphics.draw_text(p1.x * self.scale, p1.y * self.scale, text=text, fill=color)

class Color():
    def __init__(self):
        pass

class Graphics():
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.objects = []


    def draw_line(self, x1, y1, x2, y2, width = 3, color = "black"):
        obj = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        self.objects.append(obj)

    def draw_square(self, x1, y1, x2, y2, color):
        obj = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        self.objects.append(obj)

    def draw_text(self, x, y, text, color):
        obj = self.canvas.create_text(x, y, text=text, fill=color, font=('Helvetica 15 bold'))
        self.objects.append(obj)

    def clear(self):
        for obj in self.objects:
            self.canvas.delete(obj)

    def refresh(self):
        pass
