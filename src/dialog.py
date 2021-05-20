from tkinter import *   ## notice lowercase 't' in tkinter here
#import tkSimpleDialog
import tkinter.simpledialog
import tuner

class Settings(tkinter.simpledialog.Dialog):
    def body(self, master):
        self.c_freq = StringVar()
        self.c_freq.set(str(440))
        self.freq_val = 440
        
        self.title("Settings")

        minus = Button(master, text="-", command=self.decrease).grid(row=0, column = 0)

        freq_label = Label(master, textvariable=self.c_freq).grid(row=0, column = 1)

        plus = Button(master, text="+", command=self.increase).grid(row=0, column=2)
        return None

    def apply(self):
        self.result = self.freq_val

    def increase(self):
        if self.freq_val < 450:
            self.freq_val += 1
            self.c_freq.set(str(self.freq_val))

    def decrease(self):
        if self.freq_val > 430:
            self.freq_val -= 1

            self.c_freq.set(str(self.freq_val))
