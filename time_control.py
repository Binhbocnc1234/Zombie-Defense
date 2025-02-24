import pygame

sFPS=cur_fps=FPS=60  

Clock=pygame.time.Clock()
def control_fps():
    Clock.tick(FPS)
def get_fps_rate():
    if cur_fps < 1:
        return 0
    return round(sFPS/cur_fps,2)
class Time:
    '''A class helps to control time'''
    def __init__(self,total_time=0):
        self.time=0
        self.total_time=total_time
        self.times_passed=0
    def set_timer(self,total_time,reset=True):
        '''reset time=0 and set total_time in seconds. Method supports for count()'''
        if reset:
            self.time=0
        self.total_time=total_time
    def count(self,reset=True): 
        '''Should be placed in while loop to compute elapsed time
        return True if the elapsed time exceeds the total time and set self.time=0(if reset=True). Else: return False'''      
        if self.time>=self.total_time*cur_fps:
            if reset:
                self.time=0
                self.times_passed+=1
            else:
                self.times_passed+=1
            return True
        self.time+=1
        return False
