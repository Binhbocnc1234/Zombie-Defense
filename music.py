import pygame
from pygame import mixer
import os

mixer.init()
Music_vol=0.7
music_vol=1
music_path=pygame.mixer.music
def load_music(*file,volume=music_vol):
    global music_vol
    music_vol=volume
    if len(file)>=2:
        music_path.load(os.path.join(*file))
    else:
        music_path.load(*file)
    music_path.set_volume(Music_vol*volume)
    music_path.play(-1)
def set_Music_vol(volume=None):
    global Music_vol
    if volume:
        Music_vol=volume
    music_path.set_volume(Music_vol*music_vol)
    return Music_vol
Sound_vol=0.7
sound_lst=[]
def load_sound(*file,volume=1):
    if len(file)>=2:
        sound= pygame.mixer.Sound(os.path.join(*file))
    else:
        sound= pygame.mixer.Sound(*file)
    sound.set_volume(Sound_vol*volume)
    sound_lst.append([sound,volume])
    return sound
def set_Sound_vol(volume=None):
    global Sound_vol
    if volume:
        Sound_vol=volume
    for i in sound_lst:
        i[0].set_volume(Sound_vol*(i[1]))
    return Sound_vol