from __future__ import print_function
import pyaudio, aubio, wave
import sys, time, getopt
import numpy as num
import math
import utility

class Tuner:
    __A4 = 440
    __C0 = 0
    __base_octave = {}
    __data_stream = None
    __pitch_detector = None
    __tolerance = 0
    __accuracy = 0

    def __init__(self, A4=440, tolerance = 0.1, accuracy = 5):
        self.__data_stream = utility.initStream()
        self.__pitch_detector = utility.initDetector()
        self.__A4 = A4
        self.__tolerance = tolerance
        self.__accuracy = accuracy
        self.calculateC0()
        self.initBaseOctave()

    def calculateC0(self):
        self.__C0 = self.__A4 * pow(2, -4.75)

    def initBaseOctave(self):
        temp = self.__C0
        for x in utility.name:
            self.__base_octave[x] = temp
            temp = temp * pow(2, 1.0/12) 

    def setA4(self, A4):
        self.__A4 = A4
        self.calculateC0()
        self.initBaseOctave()

    def getA4(self):
        return self.__A4

    def getData(self):
        data = self.__data_stream.read(1024)
        samples = num.fromstring(data, dtype=aubio.float_type)
        pitch = self.__pitch_detector(samples)[0]

        errorper = 0
        error= 0
        note = 0
        octave = 0
        
        if pitch != 0: 
            note,octave = utility.findnote(pitch, self.__C0)
            
            expected = self.__base_octave[note] * pow(2, octave)
            error = pitch - expected
            
            if error > 0:
                margin = expected * (pow(2,1.0/24) - 1)
            else:
                margin = expected * (1 - pow(2,-1.0/24))
            
            errorper = abs(error) / margin

        return errorper, error, pitch, note, octave


    def run(self):
        tolerance = self.__tolerance
        accuracy = self.__accuracy
        while True:
            errorper, error, pitch, note, octave = self.getData()
            
            if pitch!= 0: 
                output = "Pitch:" + str(pitch) + "Hz Note:" + note + str(octave) + "            "
                
                if  errorper > 1:
                    print("Error greater than 100% at pitch : " + pitch)
                    exit()
                if errorper <= tolerance:
                    print (accuracy * "  ." + utility.colorize("  ^  ", errorper, tolerance) + accuracy * ".  " + output + '\r',end = '')
                else:
                    if error > 0:
                        pre = accuracy * "  ." + "  "
                        pos = int(math.ceil(accuracy*errorper))
                        post = (pos - 1) * "  ." + utility.colorize("  <", errorper, tolerance) + (accuracy - pos) * "  ."
                    else:
                        post = accuracy * "  ."
                        pos = accuracy - int(math.ceil(accuracy*errorper)) + 1
                        pre = "  " + (pos - 1) * ".  " + utility.colorize(">  ", errorper, tolerance) + (accuracy - pos) * ".  "
                
                    print (pre + "|" + post + "  " + output + '\r', end = '')
            sys.stdout.flush()
