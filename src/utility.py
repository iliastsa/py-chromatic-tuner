import aubio
import numpy as num
import pyaudio
import math
import wave
import time
import sys

name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def findnote(freq, C0):
    h = round(12*math.log(freq/C0,2))
    octave = int(h // 12)
    n =int(h % 12)
    return (name[n], octave)

def colorize(string, errorper, tolerance):
    if errorper <= tolerance:
	    return '\033[32m' + string + '\033[0m'
    elif errorper < 0.33:
	    return '\033[93m' + string + '\033[0m'
    elif errorper < 0.66:
        return '\033[33m' + string + '\033[0m'
    else:
        return '\033[91m' + string + '\033[0m'

def initStream():
    #PyAudio stream object.
    p = pyaudio.PyAudio()
    
    #Open the stream.
    stream = p.open(format=pyaudio.paFloat32,
     		    channels=1,rate=44100,input=True,
                    frames_per_buffer=1024)
    
    return stream


def initDetector():
    # Aubio's pitch detection.
    pDetector = aubio.pitch("default", 2048,
        2048//2, 44100)
    # Set unit.
    pDetector.set_unit("Hz")
    pDetector.set_silence(-20)

    return pDetector
