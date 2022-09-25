import json
import math
from re import L
from . import globals as gb
import numpy as np
import pygame
import pyaudio
from pydub import AudioSegment
from pydub.utils import make_chunks
import scipy.fftpack
import scipy.io.wavfile
import threading
import wave


def playSoundPos(pos: tuple[float, float] | list[float], pos_: tuple[float, float] | list[float], base: float, sound: pygame.mixer.Sound):
    dist = math.sqrt((pos[0] - pos_[0]) ** 2 + (pos[1] - pos_[1]) ** 2)
    
    vol = base * max(0, (250 - dist) / 250)
    if (vol > 0.05):
        sound.set_volume(vol)
        pygame.mixer.find_channel(True).play(sound)

class SongData:
    waveData: np.ndarray = None
    channels: int = None
    sampleWidth: int = None
    frameRate: int = None
    nFrames: int = None

def playMusic(src, vol):


    
    return
def update():
    ...