import entities as en
import time_control as time
import graphic as gp
import game_engine as ge
import pygame,random,music,math,json

vic=gp.Font(80).render("VICTORY!")
loss=gp.Font(80).render("LOSS!")
player_died=gp.scale(gp.image("Player","died"),2,"percent")
level_clear=gp.Font(80).render("Level Clear")
click_screen= gp.Font(30).render("Click to countinue")
star_img=gp.image("Other","star")
star_left=0

class Wave:   
    def __init__(self, *enemy_lst, delay=0, shuffle=True): 
        self.enemy_lst=[]
        enemy_lst=[list(i) for i in enemy_lst]
        for enemy in enemy_lst:
            n=enemy.copy()
            for i in range(n[1]):                  
                self.enemy_lst.append([n[0]]+n[2:])
        self.shuffle=shuffle
        self.time=time.Time(delay)
        self.num=0
        self.total_num=len(self.enemy_lst)
        self.last_en_spawn=pygame.time.get_ticks()
    def shuffled(self):
        if self.shuffle==True:
            random.shuffle(self.enemy_lst)
    def spawn(self):              
        if self.time.count() and self.num<len(self.enemy_lst):
            self.num+=1   
            cur_en=self.enemy_lst[self.num-1]  
            if len(cur_en) == 2:         
                en.Enemy(cur_en[0],**cur_en[1])
            else:
                en.Enemy(*cur_en)
            self.last_en_spawn=0
    def enemy_clear(self):
        return self.num==self.total_num and len(en.Enemy.lst)==0 and len(en.Enemy.explode_lst)==0

class Level:
    level=1
    type=None
    star=gp.scale(star_img,0.3,"percent")
    clock={"level_clear":time.Time(3.5),"wave_clear":time.Time(2),"level_start":time.Time(2),"end":time.Time(1.5)}
    lst={"Campain":[],"Challenge":[]}
    def __init__(self, *wave_lst, max_upgrade=None, health=15, name=None):
        for key,val in Level.lst.items():
            if self in val:
                self.type=key
        self.wave_lst=wave_lst
        self.unlock="lock"
        self.star=0
        self.max_upgrade=max_upgrade
        self.name=name
        self.health=health
        self.wave=1
    def spawn(self):
        if not Level.clock["level_start"].count(reset=False):
            wave1=gp.Font(80).render("Wave 1")
            gp.screen.blit(wave1,wave1.get_rect(center=gp.RECT.center))
            self.curren_wave().spawn()
            return True
        else:
            self.curren_wave().spawn()
    def curren_wave(self) -> Wave:
        return self.wave_lst[self.wave-1]
    @staticmethod
    def current_level():
        return Level.lst[Level.type][Level.level-1]
    def end(self):
        if self.curren_wave().enemy_clear():
            if self.wave < len(self.wave_lst):
                self.wave_clear()
            elif self.wave == len(self.wave_lst):
                if Level.level==len(Level.lst[self.type]):
                    Level.victory()
                    return False
                else:     
                    return self.level_clear()
        #Loss
        if en.Player.health <=0:
            Level.loss()
            return False
        return True
    @staticmethod
    def victory():
        Level.current_level().star=1
        music.load_music("Background","Laudaitinhai.mp3")
        while True:
            x,y=loop()
            timer=timer_end()
            gp.screen.blit(vic,(gp.RECT.w/2-vic.get_width()/2,gp.RECT.h/2-vic.get_height()/2))
            gp.screen.blit(click_screen,(gp.RECT.w/2-click_screen.get_width()/2,gp.RECT.h/2-click_screen.get_height()/2+150))
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    ge.save_exit()
                if timer and event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                    music.load_music("Background","music.mp3")
                    return False
            
    @staticmethod
    def loss():
        
        while True:
            loop(True)
            timer=timer_end()
            gp.clear(gp.sub_screen)
            gp.sub_screen.blit(loss,loss.get_rect(center=(gp.RECT.centerx,gp.RECT.centery-50)))
            gp.sub_screen.blit(click_screen,click_screen.get_rect(center=(gp.RECT.centerx,gp.RECT.centery+70)))
            gp.sub_screen.blit(player_died,(gp.RECT.centerx-player_died.get_width()/2,360))
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    ge.save_exit()
                if timer and  event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                    Level.clock["end"].time=0
                    return False 
        
    def level_clear(self):
        global star_left
        if self.type=="Campain":
            if en.Player.health == 15:
                cur_star=3
            elif en.Player.health > 8:
                cur_star=2
            else:
                cur_star=1
        elif self.type=="Challenges" and en.Player.health>0:
            self.star=1
        if not Level.clock["level_clear"].count():
            gp.screen.blit(level_clear,(gp.RECT.w/2-level_clear.get_width()/2,gp.RECT.h/2-level_clear.get_height()/2))
            if self.type=="Campain":
                for i in range(0,cur_star):
                    gp.screen.blit(Level.star,(390+Level.star.get_width()*i,330))
            return True
        else:
            if Level.level < len(Level.lst["Campain"]):
                Level.lst["Campain"][Level.level].unlock="unlock"
            if Level.level < len(Level.lst["Challenges"]):
                Level.lst["Challenges"][Level.level-1].unlock="unlock"
            if self.type=="Campain":
                if cur_star > self.star:
                    star_left += (cur_star-self.star)
                    self.star=cur_star
            return False
    def wave_clear(self):
        if not Level.clock["wave_clear"].count():
            next_wave=gp.Font(80).render("Wave {}".format(self.wave+1))
            gp.screen.blit(next_wave,(gp.RECT.centerx-next_wave.get_width()/2,gp.RECT.centery-next_wave.get_height()/2))
        else:
            self.wave+=1
            
def timer_end():
    timer=Level.clock["end"].count(reset=False)
    if timer:
        click_screen.set_alpha(255)
    else:
        click_screen.set_alpha(180)
    return timer
def unlock_lv(lv,mode):
    Level.lst[mode][lv-1].unlock="unlock"

Level.lst={
"Campain":[
Level(Wave(("Zombie", 9),delay=2.7),Wave(("Zombie",5),("Bucket Zombie",2),delay=2.9)),
Level(Wave(("Zombie",10),("Werewolf",3),delay=1), Wave(("Zombie",10),("Werewolf",6),("Bucket Zombie",4),delay=3.5)),
Level(Wave(("Bucket Zombie",3),("Bat",2),delay=1.4), Wave(("Zombie",12),("Werewolf",4),("Bat",7),delay=3.1),
    Wave(("Bucket Zombie",5),("Werewolf",4),("Bat",4),("Bat",3,{"hold":"Bucket Zombie"}),delay=5)),
Level(Wave(("Zombie", 9),("Bucket Zombie",4),("Bat",2),delay=1.5),
      Wave(("Zombie",10),("Werewolf",8),("Bucket Zombie",3),("Bat",3),delay=1.6),
    Wave(("Zombie",15),("Werewolf",8),("Bucket Zombie",10),("Bat",10),delay=2)),
Level(Wave(("Zombie",20),("Destroyer",1),delay=1),Wave(("Zombie",10),("Bucket Zombie",5),("Destroyer",3),delay=2),
    Wave(("Werewolf",4),("Bucket Zombie",6),("Destroyer",4),delay=3.5)),
Level(Wave(("Zombie",7,{"is_giant":True}),("Bucket Zombie",7),("Destroyer",3),delay=1.7),
    Wave(("Bucket Zombie",10),("Destroyer",3),("Destroyer",1,{"is_giant":True}),delay=2),
    Wave(("Werewolf",14),("Werewolf",5,{"is_giant":True}),("Bat",10),delay=1.5),
    Wave(("Zombie",10,{"is_giant":True}),("Bucket Zombie",2,{"is_giant":True}),("Bat",6),("Bat",3,{"hold":"Bucket Zombie"}),("Destroyer",2),delay=0.7),health=5)
],
"Challenges":[
Level(Wave(("Zombie",70),("Bucket Zombie",8),delay=1.4),max_upgrade=4,health=12),
Level(Wave(("Werewolf",10),("Zombie",10),delay=1),Wave(("Werewolf",10),("Bucket Zombie",3),delay=1.5),max_upgrade=6,health=5),
Level(Wave(("Bat",16,{"hold":"Zombie"}),("Bat",10),delay=2),
    Wave(("Bat",9,{"hold":"Bucket Zombie"}),("Bat",8),delay=3),
    Wave(("Bat",10,{"hold":"Werewolf"}),("Bat",8),delay=2.5),max_upgrade=9,health=4),
Level(Wave(("Zombie",40),("Bucket Zombie",15),delay=0.6),Wave(("Zombie",10),("Werewolf",20),("Bucket Zombie",5),("Bat",5,{"hold":"Werewolf"}),delay=1.2),
    Wave(("Zombie",15),("Bucket Zombie",10),("Bat",20),("Bat",9,{"hold":"Bucket Zombie"}),delay=1.7),
    Wave(("Zombie",25),("Werewolf",15),("Bucket Zombie",17),("Bat",10),("Bat",5,{"hold":"Bucket Zombie"}),delay=1.5),max_upgrade=14,health=1),
Level(Wave(("Destroyer",6),("Destroyer",2,{"is_giant":True}),delay=9),max_upgrade=12,health=8,name="Lucky box"),
Level(Wave(("Zombie",25,{"is_giant":True}),("Bucket Zombie",12,{"is_giant":True}),delay=1),
    Wave(("Bucket Zombie",6,{"is_giant":True}),("Bat",20,{"is_giant":True}),("Bat",10,{"is_giant":True,"hold":"Zombie"}),delay=1.5),
    Wave(("Werewolf",18,{"is_giant":True}),("Bat",8,{"is_giant":True,"hold":"Werewolf"}),delay=1.7),
    Wave(("Bucket Zombie",10,{"is_giant":True}),("Destroyer",5,{"is_giant":True}),("Bat",1,{"is_giant":True,"hold":"Destroyer"}),delay=3.5),max_upgrade=20, health=12)
]
}

unlock_lv(1,"Campain")

def reset():
    en.Player.health=Level.current_level().health
    en.Enemy.lst.clear()
    en.Bullet.lst.clear()
    Level.clock["level_start"].time=0
    for type in Level.lst.values():
        for level in type:
            level.wave=1
            for wave in level.wave_lst:
                wave.shuffled()
                wave.num=0
                wave.time.time=wave.time.total_time

pause1_text=gp.font(80).render("Pause",True,gp.WHITE)
pause_button={"Surrender":gp.Button(gp.Font(40).render("Surrender"),(250,400)),"Resume":gp.Button(gp.Font(40).render("Resume"),(600,400))}
def pause1():
    while True:
        x,y=loop(True)
        gp.sub_screen.blit(pause1_text,pause1_text.get_rect(center=gp.RECT.center))
        for button in pause_button.values():
            button.collide((x,y))
            button.draw(gp.sub_screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                for name,button in pause_button.items():
                    if button.is_pressed:
                        gp.clear(gp.sub_screen)
                        if name=="Surrender":
                            Level.loss()
                            return False
                        elif name=="Resume":
                            return True
            elif event.type== pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    return True
            elif event.type == pygame.QUIT:
                save_exit()
            
def loop(sub_screen=False):
    time.control_fps()
    gp.Display.blit(gp.screen,(0,0))
    if sub_screen:
        gp.Display.blit(gp.sub_screen,(0,0))
    pygame.display.flip()
    return pygame.mouse.get_pos()


def save_exit():
    info = ["en.Player.upgrade_lst[0]","ge.star_left"]
    info.append({"ge.Level.lst['{}'][{}]".format(type,i) : ["unlock","star"] for type in ("Challenges","Campain") for i in range(0,len(Level.lst[type]))} )
    with open("history.py","w+") as file:
        save_dict={}
        for var in info:
            if type(var)==tuple:
                save_dict[var[0]]=var[1]
            elif type(var)==dict:
                for key, val in var.items():
                    save_dict["Obj att "+key]= {i: eval(key+"."+i) for i in val}
            else:
                save_dict[var]=eval(var)
        json.dump(save_dict,file,indent=4)
    quit()

def get_history():
    with open("history.py","a+") as file:
        file.seek(0)
        if file.read():
            file.seek(0)
            for key, val in json.load(file).items():
                if "Obj att " in key:
                    for name, att in val.items():
                        if type(att)==str:
                            att="'"+att+"'"
                        exec("{}={}".format(key[8:]+"."+name,att))
                else:
                    exec("{}={}".format(key,val))

if __name__ == "__main__":
    print(Level.lst["Campain"][0].unlock)