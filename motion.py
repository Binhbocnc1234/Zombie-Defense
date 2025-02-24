import math
import random
import copy
import typing
from time_control import *


class Vector:
    '''Class represents Vector 2D in mathematics
    Some attributes:
        i,j : representing velocity
        x,y : position
        length,
        angle (angle to Oy axis. The magnitude of angle increases clockwise),
        gravity: float
        acceleration: Vector
    '''
    __hash__ = object.__hash__
    def __init__(self, i: float=0, j: float=0, x=None, y=None,**other_stat):
        self.i,self.j,self.x,self.y = i,j,x,y
        self.length=math.sqrt(self.i ** 2 + self.j ** 2)
        self.angle=0
        self.gravity=0
        self.ground=None
        self.is_ground=False
        self.acceleration=(0,0)
        for name,val in other_stat.items():
            exec("self.{}={}".format(name,val))
    def __repr__(self):
        return "Vector({},{},{},{})".format(self.i,self.j,self.x,self.y)
    def __add__(self, other):
        if isinstance(other, self.__class__):
            self.set((self.i+other.i,self.j+other.j))
            return self
        self.set((self.i+other[0],self.j+other[1]))
        return self
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            self.set((self.i-other.i,self.j-other.j))
            return self
        self.set((self.i-other[0],self.j-other[1]))
        return self
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return self.i * other.i + self.j * other.j
        return self.i*other, self.j*other
    def __rmul__(self, other):
        return self.__mul__(other)
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.i / other.i, self.j / other.j, self.x, self.y)
        return Vector(self.i / other, self.j / other, self.x, self.y)
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.i == other.i and self.j == other.j
        elif other==None:
            return False
        return self.i == other[0] and self.j == other[1]
    def __neg__(self):
        return Vector(-self.i, -self.j)
    def round(self,decimal: int=0):
        self.i,self.j=round(self.i,decimal),round(self.j,decimal)
        self.x,self.y=int(self.x),int(self.y)
    @typing.overload
    def set(self, velocity):
        ...
    @typing.overload
    def set(self, vector):
        ... 
    def set(self, vec):
        if type(vec) == tuple:
            self.i, self.j = vec
        else:
            self.i, self.j = vec.i, vec.j
    def get(self) -> tuple[float,float]:
        return (self.i,self.j)
    def set_point(self,x,y):
        self.x, self.y= x, y
    def get_point(self) -> tuple[float,float]:
        return (self.x,self.y)
    def get_length(self):
        return math.sqrt(self.i ** 2 + self.j ** 2)
    def get_angle(self):
        return math.degrees(math.acos(-self.j/self.length))
    def angle_between(vec1, vec2=None):
        if None==vec2:
            vec2=Vector(0,1)
        return math.degrees(math.acos(
            (vec1*vec2)/(vec1.length*vec2.length)
        ))
    def get_from_length(self):
        '''Get i, j from vector.length, angle'''
        if self.length==0:
            raise Exception("Object.length must be greater than 0")
        self.i=self.length*math.sin(math.radians(self.angle))
        self.j=-self.length*math.cos(math.radians(self.angle))
        return self.get()
    def get_from_point(self, x,y):
        self.i,self.j=x-self.x, y-self.y
        return self.get()
    def copy(self):
        return copy.deepcopy(self)
    def negate(self):
        '''Make vector opposite in place'''
        self.j*=-1
        self.i*=-1
        self.acceleration=tuple((-i for i in self.acceleration))
    def move(self,type="xy"):
        '''Change the coordinate of vector, the travel distance depends on self.j,self.i and FRAMERATE.
        Frame rate is inversely proportional to the distance traveled'''
        num=get_fps_rate()
        if "x" in type:
            self.x+=self.i*num
        if "y" in type:
            if not self.is_ground:
                self.j+=self.gravity
            self.y+=self.j*num
        if self.ground != None:
            if self.y> self.ground:
                self.y=self.ground
                self.j=0
                self.is_ground=True
            elif self.y < self.ground:
                self.is_ground=False
        self+=self.acceleration
        return (self.x,self.y)
    def raw_move(self,type="xy"):
        '''Change the coordinate of vector, the travel distance depends on self.j,self.i'''
        if "x" in type:
            self.x+=self.i
        if "y" in type:
            if not self.is_ground:
                self.j-=self.gravity
            self.y+=self.j
        if self.j> self.ground:
            self.j=self.ground
            self.is_ground=True
        elif self.i < self.ground:
            self.is_ground=False
        self+=self.acceleration
        return (self.x,self.y)
    def reflect(self,axis="x"):   #refract: khúc xạ
        '''Used to make object bounce when it collides with wall'''
        if axis=="x":
            self.i*=-1
        elif axis=="y":
            self.j*=-1
    def circular_motion(self,angle_per_frame: float=1) -> tuple:
        '''Return position representing '''
        self.angle+=angle_per_frame
        self.get_from_length()
        self.round(2)
        return (self.x+self.i,self.j)
    @staticmethod
    def from_length(length,angle,gravity=0):
        '''Get Vector from length, angle'''
        vec=Vector(length=length,angle=angle,gravity=gravity)
        vec.get_from_length()
        return vec
    @staticmethod
    def from_two_point(point1,point2):
        return Vector(point2[0]-point1[0],point2[1]-point1[1],*point1)
class BezierCurve:
    def __init__(self,point1,point2):
        self.point1=point1
        self.point2=point2
    def get_point(self,t):
        return ((1-t)*self.point1[0]+t*self.point2[0], (1-t)*self.point1[1]+t*self.point2[1])
    def draw_graph(self,sur):
        pass



def rect(point1: tuple, point2: tuple):
    '''Get pygame.Rect object from 2 points opposite each other'''
    return pygame.Rect(point1,(point2[0]-point1[0],point2[1]-point1[1]))

def limit(pos: float, left: float, right: float):
    if pos < left:
        pos=left
    elif pos > right:
        pos=right
    return pos

def collidelist(lst: typing.Union[list,dict],pos):
    choice=None
    if type(lst)==dict:
        for key,val in lst.items():
            if val.collidepoint(pos):
                choice=key
                break
    elif type(lst)==list:
        for i in range(0,len(lst)):
            if lst[i].collidepoint(pos):
                choice=i
                break
    return choice

if __name__=="__main__":
    pass
