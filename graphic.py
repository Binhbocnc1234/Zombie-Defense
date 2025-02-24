
import math,os,motion
import time_control as time
import pygame 

pygame.init()
pygame.display.init()
#Color
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
blue=(0,0,255)
green=(0,255,0)
YELLOW=(255,255,0)
aqua=(0, 154, 224)
gray=(133, 130, 123)
gray_white=(200,200,200)
purple=(116, 0, 173)

default_font="sans"
def font(size=30,name=default_font) -> pygame.font.SysFont:
    return pygame.font.SysFont(name,size)

#Handle Surface
bar_transparentcy=255
def image(*img):
    if len(img)>=2:
        return pygame.image.load(os.path.join(*img[:-1],img[-1]+".png")).convert_alpha()
    else:
        return pygame.image.load(img).convert_alpha()
def clear(sur):
    sur.fill((0,0,0,0))
def scale(img,size,type="size"):
    if type=="size":
        return pygame.transform.scale(img,size)
    elif type=="percent":
        wid,hei=round(img.get_width()*size),round(img.get_height()*size)
        return pygame.transform.scale(img,(wid,hei))
def mask(sur):
    return pygame.mask.from_surface(sur)
def surface(wid,len):
    '''Create transparent pygame.Surface'''
    surface=pygame.Surface((wid,len)).convert_alpha()
    surface.fill((0,0,0,0))
    return surface

#Screen effects
def fadeout(sur: pygame.Surface,alpha=255,time_delay=10,color=BLACK):
    alpha_sur=surface(*sur.get_size())
    alpha_sur.fill(color+(1,))
    for value in range(1,alpha+1):
        sur.blit(alpha_sur,(0,0))
        pygame.display.flip()
        pygame.time.delay(time_delay)
def setup_Display(size: tuple,caption: str=None,icon: pygame.Surface=None,flags=None):
    global Display,screen,sub_screen,RECT
    Display=pygame.display.set_mode(size)
    RECT=Display.get_rect()
    if caption:
        pygame.display.set_caption(caption)
    if icon:
        pygame.display.set_icon(icon)
    screen=surface(*size)
    sub_screen=surface(*size)
setup_Display((1000,600),"Zombie Defense")

class Closescreen:
    def __init__(self,delay=10,delay_when_open=800):
        self.delay=delay
        self.delay_when_open=delay_when_open
        self.initial_velocity=18
        self.vec=motion.Vector(j=self.initial_velocity,x=RECT.w,y=0,acceleration=(0,(-self.initial_velocity**2)/RECT.h))
        self.sur=pygame.Surface((RECT.w,RECT.h))
    def close(self,sur=sub_screen):
        self.reset()
        while True:
            pygame.event.pump()
            if round(self.vec.j)==0:
                pygame.time.delay(self.delay_when_open)
                return False
            self.draw(sur)
    def open(self,sur=sub_screen):
        if self.vec.y>0:
            self.draw(sur)
        else:
            self.reset()
    def draw(self,sur=sub_screen):
        self.vec.move()
        sur.fill((0,0,0,0))
        sur.blit(self.sur,(0,0),(0,0,*self.vec.get_point()))
        sur.blit(self.sur,(0,RECT.h-self.vec.y))
        Display.blit(sur,(0,0))
        pygame.display.flip()
        pygame.time.delay(self.delay)
    def reset(self):
        self.vec.j=self.initial_velocity
        self.vec.y=0

class Rotate:
    def __init__(self, img: pygame.Surface , center: tuple, angle_per_frame: float=0):
        self.img=img
        self.center=center
        self.rect=self.img.get_rect(center=center)
        self.angle=0
        self.angle_per_frame=angle_per_frame
    def draw(self, sur=screen):
        '''Rotate img clockwise and draw it on screen'''
        self.angle+=self.angle_per_frame
        rotated_img=pygame.transform.rotate(self.img,-self.angle)
        sur.blit(rotated_img,self.img.get_rect(center=self.center))

default_font="sans"
class Font:
    lst=[]
    def __init__(self,size=30,name=default_font,color=YELLOW):
        self.font=pygame.font.SysFont(name,size)
        self.color=color
        self.size=size
    def render(self, text: str):
        return self.font.render(text, True, self.color).convert_alpha()
class Spritesheet:
    """
    Allow you to use image that contains multiple images, animations
    Some attributes:
        sheet: the whole image
        img_lst: a list contains small scaled images
    """
    lst=[]
    def __init__(self,sheet,x=0,y=0,rol=3,col=1,delay=0.3,remove=True,ratio=1):
        self.sheet=sheet
        self.row,self.col=rol,col
        self.wid,self.len=self.get_width(),self.get_height()
        self.time=time.Time(delay)
        self.index=0
        self.remove=remove
        #Small image stat    
        self.img_num=self.row*self.col      
        self.img_rect=pygame.Rect(x,y,self.wid//self.row,self.len//self.col)
        self.ratio=ratio
        if self.ratio!=1:
            self.img_lst=[scale(self.get_img(index),self.ratio,"percent") for index in range(0,self.img_num)]
            self.img_rect.size=self.img_rect.w*self.ratio,self.img_rect.h*self.ratio
        else:
            self.img_lst=[self.get_img(index) for index in range(0,self.img_num)]
        self.mask=mask(self.img_lst[0])
    def get_img(self,index):
        img_x=((index)%self.row)*self.img_rect.w
        img_y=((index)//self.row)*self.img_rect.h
        self.sur=surface(self.img_rect.w,self.img_rect.h)
        self.sur.blit(self.sheet,(-1,0),(img_x,img_y, self.img_rect.w,self.img_rect.h))
        return self.sur
    def animation(self,sur=screen):
        sur.blit(self.img_lst[self.index],(self.img_rect.x,self.img_rect.y))
        if self.time.count():
            self.index+=1
            if not self.index<self.img_num:
                if self.remove:
                    if self in Spritesheet.lst:
                        Spritesheet.lst.remove(self)
                else:
                    self.index=0
                return False
    def draw(self,sur=screen):
        sur.blit(self.img_lst[0],(self.img_rect.x,self.img_rect.y))
    def set_pos(self,x,y):
        '''Set position for animating'''
        self.img_rect.x,self.img_rect.y=x,y
    def scale(self):
        pass
    def get_width(self):
        return self.sheet.get_width()
    def get_height(self):
        return self.sheet.get_height()
class Scrolbagr:

    def __init__(self,*filename,speed=0.5):
        self.img=image(*filename)
        self.speed=speed
        self.img_coor_y=[self.get_height()*i for i in range(0,math.ceil(RECT.h/self.get_height())+1)] 
        self.img_coor_x=[self.get_width()*i for i in range(0,math.ceil(RECT.w/self.get_width())+1)]  
        self.x_const=0
        self.y_const=0
    def scrolling(self,sur,mode="y"):
        if mode=="y":
            for i in range(0,len(self.img_coor_y)):
                sur.blit(self.img,(self.x_const,self.img_coor_y[i]))
                self.img_coor_y[i]+=self.speed
                if self.img_coor_y[i]>RECT.h:
                    self.img_coor_y[i]=min(self.img_coor_y)-self.get_height()
        elif mode=="x":
            for i in range(0,len(self.img_coor_x)):

                sur.blit(self.img,(self.img_coor_x[i],self.y_const))
                self.img_coor_x[i]+=self.speed
                if self.img_coor_x[i]>RECT.w:
                    self.img_coor_x[i]=min(self.img_coor_x)-self.get_width()
    def get_height(self):
        return self.img.get_height()
    def get_width(self):
        return self.img.get_width()

class Button:
    '''
    Class represents the button for the player to interact with.
    Some attributes:
        img: a tuple with the first element being the image when the mouse pointer is not in the button and the other being the image when it is pressed
        pos: a tuple represents cursor' position
        other_img: structure [(Surface, offset),(Surface, offset),...], where offset is position relative to Button
    '''
    def __init__(self,img: tuple, pos: tuple, other_img=[]):
        self.img=img
        self.is_pressed=0
        if type(img) in (tuple,list):
            self.rect=self.img[0].get_rect(x=pos[0],y=pos[1])
        else:
            self.rect=self.img.get_rect(x=pos[0],y=pos[1])
        self.other_img=other_img
        
    def draw(self,sur=screen) -> bool:
        '''Draw img and other_img on Surface'''
        if type(self.img) in (tuple,list):
            img=self.img[self.is_pressed]
            
        else:
            img=self.img
        sur.blit(img,self.rect)
        for img, pos in self.other_img:
            sur.blit(img, (self.rect.x + pos[0], self.rect.y+pos[1]))
    def collide(self,pl_pos):
        '''return True if the cursor's position is in Button'''
        if self.rect.collidepoint(pl_pos):
            self.is_pressed=1
        else:
            self.is_pressed=0
        return self.is_pressed==1

class ButtonLst:
    '''
    Class contains list of Button object
    Some attributes:
        button_rect: contains width, height of a button
        sur: Surface to draw 
        resolution: size of self.sur
        other_img: structure: [((Surface, offset),(Surface, offset)),((Surface, offset),...),...]
    '''
    scroll_button=Spritesheet(image("Other","scroll button"),rol=2)
    def __init__(self,choose_lst,button,pos,offset,other_img=[],resolution=None):
        if type(button)==tuple:
            self.button_rect=pygame.Rect(0,0,*button)
        else:
            self.button_rect=button[0].get_rect()
        self.resolution=resolution
        if resolution:
            self.main_sur=surface(*resolution)
            self.sur=surface(resolution[0],2000)
        else:
            self.main_sur=surface(RECT.w,RECT.h)
            self.sur=surface(RECT.w,2000)
        self.Offset=[0,0]
        self.Offset_limit=[-150,30]
        self.rect=self.main_sur.get_rect(x=pos[0],y=pos[1])
        if resolution:
            self.scroll_img=surface(self.rect.w,20)
            self.scroll_img.fill((0,0,0,50))
            self.flip_scroll_img=self.scroll_img.copy()
            self.scroll_img.blit(ButtonLst.scroll_button.img_lst[0],(self.scroll_img.get_width()/2-10,0))
            self.flip_scroll_img.blit(ButtonLst.scroll_button.img_lst[1],(self.scroll_img.get_width()/2-10,0))
        self.dict={}
        for i in range(0,len(choose_lst)):
            if i > len(other_img)-1:
                button_other_img=[]
            else:
                button_other_img=other_img[i]
            self.dict[choose_lst[i]]=Button(button,(0,(self.button_rect.h+offset)*i),button_other_img)
    def draw(self,pos,sur=screen,clear=True):
        '''
        Draw buttons and other imgs on self.sur. Return the name of button pressed, if no button is pressed, return None
        '''
        choice=None
        x= pos[0]-self.rect.x-self.Offset[0]
        y= pos[1]-self.rect.y-self.Offset[1]
        if clear:
            self.clear()
        for key, button in self.dict.items():
            if button.collide((x,y)):
                choice=key
            button.draw(self.sur)
        self.main_sur.blit(self.sur,self.Offset)
        if self.resolution:
            self.main_sur.blits(((self.scroll_img,(0,0)), (self.flip_scroll_img,(0,self.rect.h-self.scroll_img.get_height()))))
        if sur:
            sur.blit(self.main_sur,self.rect)
        return choice
    def scroll(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            self.mouse_scroll=True
        elif event.type==pygame.MOUSEBUTTONUP:
            self.mouse_scroll=False
        elif event.type==pygame.MOUSEWHEEL:
            self.Offset[1]+=event.y*10
            self.Offset[1]=motion.limit(self.Offset[1],*self.Offset_limit)
    def clear(self):
        clear(self.sur)
        clear(self.main_sur)

# def fill_background():
#     gp.screen.fill()
if __name__=="__main__":
    pass
