from tkinter import *   ## notice lowercase 't' in tkinter here
from colour import Color
from PIL import Image, ImageTk
import tuner
import dialog
import math
import threading
import needle

class App:
    __tuner = None
    __master = None
    __accuracy = None

    __text_info = None
    __info_content = None

    __canvas = None

    __needle = None
    __colors = []

    errorper = 0.0
    error = 0.0
    pitch = 0.0
    note = ""
    octave = 0

    photo = None

    listen_t = None
    running = True

    __height = None
    __width = None

    def __init__(self, width, height, A4 = 440, tolerance = 0.1, accuracy = 5):
        self.__tuner = tuner.Tuner(A4, tolerance, accuracy)
        self.__master = Tk()

        screen_w = self.__master.winfo_screenwidth()
        screen_h = self.__master.winfo_screenheight()

        self.__width  = width
        self.__height = height

        pos = "{}x{}".format(int(screen_w/2-self.__width/2),
                              int(screen_h/2-self.__height/2))

        self.__master.title("Chromatic tuner")

        self.__master.geometry(pos)
        self.__master.resizable(False, False)
        self.__accuracy = accuracy

        self.__info_content = StringVar()
        self.__text_info = Label(self.__master, textvariable=self.__info_content)

        self.__canvas = Canvas(self.__master, width=self.__width, height=self.__height)

        image = Image.open("../assets/gears.png")
        image = image.resize((35, 35), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)

        self.button = Button(self.__master, command=self.settings)
        self.button.config(image=self.image)
        self.button.grid(row=0,column=0, sticky=W)

        self.__c_freq = StringVar()
        self.updateCfreq()
        
        Label(self.__master, 
              textvariable=self.__c_freq,
              font="Helvetica 16 bold"
              ).grid(row=0, column=0)

        self.__canvas.grid(row=1,column=0)
        self.__text_info.grid(row=2,column=0)

        self.__needle = needle.Needle(self.__master, self.__canvas, width, height)
        self.drawBar()
        self.listen_t = threading.Thread(target=self.read,args=())
        self.listen_t.start()

    def updateCfreq(self):
        self.__c_freq.set("A4 = {} Hz".format(self.__tuner.getA4()))
    
    def settings(self):
        w = dialog.Settings(self.__master)
        self.__tuner.setA4(w.result)
        self.updateCfreq()

    def read(self):
        while self.running:
            self.errorper, self.error, self.pitch, self.note, self.octave = self.__tuner.getData() 

    def update(self):
        if self.__needle.inTransit():
            self.__needle.move()
        else:
            errorper = self.errorper
            error=self.error
            pitch= self.pitch
            note = self.note 
            octave = self.octave

            if pitch != 0:
                self.updateInfo(pitch, note, octave)
                self.updateNeedle(errorper, error)

        self.__master.after(1, self.update)
    
    def updateInfo(self, pitch, note, octave):
        self.__info_content.set("Pitch: {:.2f} Hz Note: {}{}".format(pitch, note, octave))

    def updateNeedle(self, errorper, error):
        colorIndex = int(10*errorper)
        newX = 0

        if error > 0:
            newX = int(self.__width/2 + (3.0*self.__width/8)*errorper)
            colorIndex += 9
        else:
            newX = int(self.__width/2 - (3.0*self.__width/8)*errorper)
            colorIndex = 9 - colorIndex

        self.__needle.update(newX, colorIndex)

    def run(self):
        self.__master.after(1, self.update)
        self.__master.mainloop()
        self.running = False

    def drawBar(self):
        self.__canvas.create_line(1.0/8 * self.__width, self.__height/2,
                                  7.0/8 * self.__width, self.__height/2,
                                  width = 2.0)
        self.__canvas.create_line(self.__width/2, self.__height/2,
                                  self.__width/2, self.__height/2 - 20,
                                  fill="black",
                                  width=2.0)

app = App(width=500, height=281)
app.run()
