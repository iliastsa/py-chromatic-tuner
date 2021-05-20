from tkinter import *   ## notice lowercase 't' in tkinter here
from colour import Color
import math

class Needle:
    __colors = []
    __master = None
    __canvas = None
    __needle = None

    __in_transition = False

    __trans_rate = 0
    __color_rate = 0.0

    __curColorIndex = 0.0
    __newColorIndex = 0

    __width  = 0
    __height = 0
    
    __curPos = {}
    __newPos = {}

    __length = 15

    def __init__(self, container, canvas, width, height):
        self.__master = container
        self.__canvas = canvas
        self.__width = width
        self.__height = height
        self.initColors()
        self.initNeedle()

    def initColors(self):
        green = Color("green")
        red = Color("red")

        right = list(green.range_to(red, 10))
        left = list(red.range_to(green, 10))


        self.__colors = left[:9] + right

    def initNeedle(self):
        width  = self.__width
        height = self.__height

        self.__curPos["x"] = width/2
        self.__curPos["y"] = height/2
        
        x = width/2
        y = self.__curPos["y"]
        self.__needle = self.__canvas.create_line(x, y,
                                                  x, y - self.__length,
                                                  fill="green",
                                                  width=2.0)

    def draw(self, x, color):
        y = self.__curPos["y"]
        self.__canvas.coords(self.__needle, x, y,
                                            x, y - self.__length)
        self.__canvas.itemconfig(self.__needle, fill=color)

    def update(self, x, final_color):
        self.__in_transition = True
        self.__newPos["x"] = x
        self.__newColorIndex = final_color
        
        no_steps = 100

        self.__trans_rate = float(x - self.__curPos["x"])/no_steps
        self.__color_rate = float(final_color - self.__curColorIndex)/no_steps
        
        self.move()

    def move(self):
        if self.__curPos["x"] == self.__newPos["x"]:
            self.__in_transition = False
            return
        
        diff = self.__newPos["x"] - self.__curPos["x"]

        rate = self.__trans_rate

        if math.fabs(diff) > math.fabs(rate) and rate != 0:
            self.__curPos["x"] = self.__curPos["x"]     + rate
            self.__curColorIndex = self.__curColorIndex + self.__color_rate

            x = self.__curPos["x"]
            colorIndex = self.__curColorIndex

            self.draw(x, self.__colors[int(colorIndex)]) 
        else:
            self.draw(self.__newPos["x"], self.__colors[int(self.__newColorIndex)])
            self.__curColorIndex = self.__newColorIndex
            self.__curPos["x"] = self.__newPos["x"]

    def getX(self):
        return self.__curPos["x"]

    def inTransit(self):
        return self.__in_transition


