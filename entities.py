import pygame
import graphic as gp
import time_control as time
import motion,random,music,copy,math
def collide(obj1,obj2):
    '''Used for pixel perfect collisions'''
    offset_x = obj1.vector.x - obj2.vector.x
    offset_y = obj1.vector.y - obj2.vector.y
    return obj2.mask.overlap(obj1.mask, (int(offset_x), int(offset_y))) != None
def get_random(min,max):
    return random.uniform(min,max)
class Player:
    x=180
    y=250
    health=15
    sound=music.load_sound("Player","shot.mp3")
    def __init__(self):       
        self.form=0
        self.vector=motion.Vector(x=Player.rect.centerx,y=Player.rect.centery)
        self.is_charge=False
        self.release=False
        self.length=0
        self.min_length=7
        self.max_length=14
        self.health=15
    def draw(self,sur=gp.screen):
        sur.blit(Player.img[self.form],(Player.rect.x,Player.rect.y))
        sur.blit(Player.charge_bar["img"][1],Player.charge_bar["rect"])
        sur.blit(Player.charge_bar["img"][0],Player.charge_bar["rect"],
        (0,0,Player.charge_bar["rect"].w*(self.length/self.max_length),Player.charge_bar["rect"].h))
        sur.blit(Player.charge_bar["img"][2],Player.charge_bar["img"][2].get_rect(center=Player.charge_bar["rect"].center))
    def shot(self,x,y):
        if self.release:
            self.is_charge=self.release=False
            self.form=0
            if self.length>=self.min_length:
                dam=self.get_dam()
                self.length += Player.upgrade["Fire rate up"][0]*0.8
                Bullet(self.length,self.vector.angle,self.vector.get_point(),dam)
                up=Player.upgrade["Shadow arrow"]
                shadow_dam=dam*(up[0]*up[1])
                if up[0]==1 or up[0]==2:
                    Bullet(self.length,self.vector.angle-10,self.vector.get_point(),shadow_dam,shadow=True)
                elif up[0] >=3:
                    Bullet(self.length,self.vector.angle-10,self.vector.get_point(),shadow_dam/2,shadow=True)
                    Bullet(self.length,self.vector.angle+10,self.vector.get_point(),shadow_dam/2,shadow=True)
                Player.sound.play()
            self.length=0
        elif self.is_charge:
            if self.length<self.max_length:
                self.length+=Player.get_fire_rate()
            if x < self.rect.centerx+5:
                x=self.rect.centerx+5
            self.vector.get_from_point(x,y)
            self.vector.length=self.vector.get_length()
            pygame.draw.line(gp.screen,gp.YELLOW,self.vector.get_point(),(x,y))
            self.vector.angle=self.vector.get_angle()
            self.form=1
    @staticmethod
    def get_fire_rate():
        return 0.13*(1+math.prod(Player.upgrade["Fire rate up"]))         #Max : 55 frame
    def get_dam(self):
        return round((self.length*(100/23)+40)*(1+math.prod(Player.upgrade["Damage up"])))
Player.upgrade_lst=[{"Damage up":[0,0.18],"Fire rate up":[0,0.16],
                     "Shadow arrow":[0,0.21],"Flame arrow":[0,8]}]
Player.upgrade_lst.append(copy.deepcopy(Player.upgrade_lst[0]))
Player.upgrade=Player.upgrade_lst[0]
Player.img=[gp.image("Player","idle"),gp.image("Player","charge")]
Player.rect=Player.img[0].get_rect(x=180,y=250)
Player.charge_bar={"img":(gp.image("Other","charge bar"),gp.image("Other","charge frame"),gp.image("Other","limit"))}
Player.charge_bar["rect"]=Player.charge_bar["img"][0].get_rect(x=Player.rect.x+45,y=Player.rect.y-30)
class Enemy:
    lst=[]
    explode_lst=[]
    def __init__(self,type, is_giant=False, hold=None):
        Enemy.lst.append(self)
        self.type=type
        self.is_giant=is_giant
        self.flame, self.flame_dam= False, 0
        self.flame_time = time.Time(0.5)
        self.burn_times=0
        self.flame_img=gp.Spritesheet(gp.image("Player","fire animation"),delay=0.1,remove=False,ratio=0.5)
        self.img=Enemy.img[type]
        ratio=1
        self.live=1
        if hold:
            self.hold=Enemy(hold,is_giant)
        else:
            self.hold=None
        if self.hold:
            self.hold.is_hold=True
        self.is_hold=False
        if type=="Zombie":
            self.health=140
            ratio=0.5
            speed=0.4
            y=get_random(400,500)
        elif self.type=="Bucket Zombie":
            self.health=530
            speed=0.5
            ratio=0.33
            y=get_random(400,500)
        elif self.type=="Werewolf":
            self.health=400
            self.live=2
            speed=1
            ratio=0.7
            y=get_random(400,500)
        elif self.type=="Bat":
            self.health=400
            speed=0.7
            ratio=0.7
            y=get_random(20,300)
        elif self.type=="Destroyer":
            self.health=1100
            self.live=3
            self.explode_ani=gp.Spritesheet(gp.image("Enemy","explosion"),rol=10,delay=0.1,ratio=2)
            speed=0.4
            y=get_random(400,500)
        if is_giant:
            self.health*=2
            ratio*=1.5
            y-=40
            if type=="Destroyer":
                self.live=5
            else:
                self.live=2
        self.sheet=gp.Spritesheet(self.img,remove=False,ratio=ratio)
        self.mask=self.sheet.mask
        self.vector=motion.Vector(i=-speed,x=gp.RECT.w+10,y=y)
    def move(self):
        if self.vector.x<204:
            Enemy.lst.remove(self)
            if self.hold in Enemy.lst:
                Enemy.lst.remove(self.hold)
                Player.health-=self.hold.live
            Player.health-=self.live
        if self.hold:
            self.hold.vector.set_point(self.vector.x,self.vector.y+50)
        self.vector.move()

    def draw(self,sur=gp.screen):
        if self.hold in Enemy.lst:
            self.hold.sheet.set_pos(*self.hold.vector.get_point())
            self.hold.sheet.draw()
        self.sheet.set_pos(*self.vector.get_point())
        self.sheet.animation(sur)
    def get_health(self,ammount):
        self.health+=ammount
        if self.health<=0:         
            if self.type=="Destroyer":
                Enemy.explode_lst.append(self)
            if self.hold:
                self.hold.is_hold=False
                self.hold.vector.gravity=0.2
                self.hold.vector.ground=get_random(400,500)
            Enemy.lst.remove(self)
    def flaming(self):
        self.flame_img.img_rect.center=self.sheet.img_rect.center
        self.flame_img.animation()
        if self.flame_time.count():
            self.get_health(-self.flame_dam)
            Damage(self.flame_dam,*self.vector.get_point(),size=20)
            if self.flame_time.times_passed >= 3:
                self.flame=False
    @staticmethod
    def exploding():
        for self in Enemy.explode_lst:
            self.explode_ani.set_pos(*self.vector.get_point())
            if self.explode_ani.animation() == False:
                if random.randint(0,2)==0:
                    type_lst=Enemy.type_lst[:4]
                else:
                    type_lst=Enemy.type_lst
                lst=[Enemy(random.choice(type_lst),is_giant=self.is_giant) for i in range(0,random.randint(1,3))]
                for en in lst:
                    en.vector.set_point(get_random(self.vector.x-20, self.vector.x+20),get_random(self.vector.y-10,self.vector.y+10))
                Enemy.explode_lst.remove(self)


Enemy.type_lst=("Zombie","Bucket Zombie","Werewolf","Bat","Destroyer")
Enemy.img={type:gp.image("Enemy",type) for type in Enemy.type_lst}

class Bullet:
    hit_animmation=gp.image("Player","hit animation")
    img=gp.image("Player","arrow")
    lst=[]
    sound=music.load_sound("Player","hit.mp3",volume=0.7)
    def __init__(self,length,angle,pos,dam,shadow=False):
        Bullet.lst.append(self)
        self.length=length
        self.dam=round(dam)
        self.shadow=shadow
        self.vector=motion.Vector.from_length(self.length,angle,0.17)
        self.vector.set_point(*pos)
        self.sur=gp.Rotate(Bullet.img,self.vector.get_point())
    def draw(self):
        self.sur.center=self.vector.move()
        self.vector.length=self.vector.get_length()
        self.sur.angle=self.vector.get_angle()
        self.mask=gp.mask(self.sur.img)
        self.sur.draw()
    def hit(self,enemy: Enemy):
        if collide(self,enemy):
            enemy.get_health(-self.dam)
            gp.Spritesheet.lst.append(gp.Spritesheet(Bullet.hit_animmation,*self.vector.get_point(),rol=6,delay=0.1))
            Damage(self.dam,*self.vector.get_point())
            if Player.upgrade["Flame arrow"][0] > 0:
                enemy.flame, enemy.flame_dam = True, Player.upgrade["Flame arrow"][0]*Player.upgrade["Flame arrow"][1]
                enemy.flame_time.times_passed=0
            if not self.shadow:
                Bullet.sound.play()
            Bullet.lst.remove(self)
            return True
    def off_screen(self):
        if (not 0-self.sur.rect.w < self.vector.x < gp.RECT.w) and (not 0-self.sur.rect.h-gp.RECT.h < self.vector.y < gp.RECT.h):
            Bullet.lst.remove(self)
        

class Damage:
    '''A small class to display the damage caused by Bullet onto the screen'''
    lst=[]
    def __init__(self,dam,x,y,size=25):
        Damage.lst.append(self)
        self.font=gp.font(size).render(str(dam),True,gp.YELLOW)
        self.vector=motion.Vector(random.uniform(-1,1),random.uniform(-2,-1),x,y)
        self.vector.set_point(x,y)
        self.time=time.Time(0.3)
    def draw(self,sur=gp.screen):
        self.vector+=motion.Vector(0,0.25)
        self.vector.move()
        sur.blit(self.font,(self.vector.get_point()))
        if self.time.count():
            Damage.lst.remove(self)