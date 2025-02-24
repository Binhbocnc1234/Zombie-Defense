import pygame, motion, music
import graphic as gp
import game_engine as ge
import entities as en
from other import *

game_background=[gp.image("Background","background"),gp.image("Background","house")]
button_img=[gp.image("Other","button"),gp.image("Other","light button"),gp.image("Other","return button"),gp.scale(gp.image("Other","pause button"),2,"percent")]
return_rect=button_img[2].get_rect(x=950,y=0)
pause_rect=button_img[3].get_rect(x=930,y=10)
click_sound=music.load_sound("Other","click sound.mp3",volume=0.7)

player=en.Player()
close_screen=gp.Closescreen()
health_font=gp.Font(40)

def game():

    ge.reset()
    close_screen.close()
    while True:
        x,y=ge.loop(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ge.save_exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    if not ge.pause1():
                        return False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if pause_rect.collidepoint(x,y):
                        if not ge.pause1():
                            return False
                    player.is_charge=True

            elif event.type==pygame.MOUSEBUTTONUP:
                player.release=True

        gp.screen.blits(((game_background[0],(0,0)),(button_img[3],pause_rect)))
        player.draw()
        player.shot(x,y)
        gp.screen.blit(game_background[1],(-20,40))
        #Font
        gp.screen.blit(health_font.render("Health"+str(en.Player.health)),(20,200))
        ge.Level.current_level().spawn()
        for arrow in en.Bullet.lst:
            arrow.draw()
            arrow.off_screen()
            for enemy in en.Enemy.lst:
                if arrow in en.Bullet.lst:
                    if arrow.hit(enemy):
                        break
        for enemy in en.Enemy.lst:
            if not enemy.is_hold:
                enemy.move()
                enemy.draw()
            if enemy.flame:
                enemy.flaming()
        en.Enemy.exploding()
        for ani in gp.Spritesheet.lst:
            ani.animation()
        for obj in en.Damage.lst:
            obj.draw()
        close_screen.open()
        #End
        if not ge.Level.current_level().end():
            return False
        
level_font=gp.Font(40)
mode_text=[(gp.Font(60).render("Campain"),(160,130)),(gp.Font(60).render("Challenges"),(500,130))]
lock=gp.scale(gp.image("Other","lock"),0.5,"percent")
star_img=gp.scale(ge.star_img,0.13,"percent")
level_render=[[[level_font.render("-Level{}-".format(i)),(15,10)]] for i in range(1,len(ge.Level.lst["Campain"])+1)]
level_button = [gp.scale(img,(200,60)) for img in button_img[:2]]

level_button={
    "Challenges":gp.ButtonLst([i for i in range(1,len(ge.Level.lst["Challenges"])+1)],level_button,(500,228),5,
level_render,(200,360)),
    "Campain":gp.ButtonLst([i for i in range(1,len(ge.Level.lst["Campain"])+1)],level_button,(160,228),5,
level_render,(240,360))
}


def level():
    '''Function helps Player choose level'''
    while True:
        pos=ge.loop()
        gp.screen.blit(menu_background,(0,0))
        gp.screen.blits(mode_text)
        choice=None
        for type, button_lst in level_button.items():
            tem_choice=button_lst.draw(pos,sur=None)
            if tem_choice:
                choice=(tem_choice,type)
            for key, button in button_lst.dict.items():
                level=ge.Level.lst[type][key-1]
                if level.unlock=="lock":
                    button_lst.main_sur.blit(lock,lock.get_rect(center=add_tuple(button.rect.center,button_lst.Offset)))
                else:
                    for i in range(1,level.star+1):
                        button_lst.main_sur.blit(star_img, star_img.get_rect(
                        center=add_tuple((button.rect.centerx+i*star_img.get_width()+20,button.rect.centery),button_lst.Offset)))
            gp.screen.blit(button_lst.main_sur,button_lst.rect)
        gp.screen.blit(button_img[2],return_rect)
        gp.screen.blit(gp.Font(20,color=gp.WHITE).render("*Note: You won't earn star in Challenges mode"),(500,100))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                ge.save_exit()
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                click_sound.play()
                if choice != None and ge.Level.lst[choice[1]][choice[0]-1].unlock=="unlock":
                    ge.Level.level,ge.Level.type=choice
                    if choice[1]=="Campain":
                        en.Player.upgrade=en.Player.upgrade_lst[0]
                        game()
                        return False
                    elif choice[1]=="Challenges":
                        en.Player.upgrade=en.Player.upgrade_lst[1]
                        if upgrade(ge.Level.current_level().max_upgrade):
                            game()
                        return False
                elif return_rect.collidepoint(pos):
                    return False
            for i in level_button.values():
                i.scroll(event)
up_font={"big":gp.Font(40),"small":gp.Font(20)}
long_button=[gp.scale(img,(150,50)) for img in button_img[:2]]
keys=tuple(en.Player.upgrade.keys())

up_button=gp.ButtonLst(keys,button_img[:2],(292,213),0,
[[(gp.image("Other",key),(0,0)),(up_font["big"].render(key),(button_img[0].get_width()+5,0))] for key in keys],
resolution=(500,360))
reset_button=gp.Button(long_button,(800,100),[(up_font["big"].render("Reset"),(20,5))])
continue_button=gp.Button(long_button,(800,450),[(up_font["big"].render("Continue"),(5,10)),(gp.image("Other","ready"),(-35,0))])

#detail for upgrades
detail_text={
    "Shadow arrow": [up_font["small"].render(text) for text in ["Create an additional arrows when shooting","One shadow arrow per shot. Damage: 21%",
"Damage: 42%","Two shadow arrow per shot. Damage: 42 -> 32%","Damage: 42%","Damage: 53%","Damage: 63%","Damage: 74%","Damage: 84%"]],
    "Flame arrow": [up_font["small"].render(text) for text in ["Arrow deals fire damage over time"]+
["Damage: {}%".format(i*en.Player.upgrade["Flame arrow"][1]) for i in range(1,5)]],
    "Damage up": [up_font["small"].render("Damage: {}%".format(round(100*(1+i*en.Player.upgrade["Damage up"][1])))) for i in range(0,9)],
    "Fire rate up": [up_font["small"].render("Fire rate: {}%. Arrow's speed: +{}".format(round((1+i*en.Player.upgrade["Fire rate up"][1])*100),round(i*0.8,1))) for i in range(0,6)]
}

def upgrade(max_upgrade=None):
    close_screen.close()
    if max_upgrade:
        main_upgrade=max_upgrade
        for i in en.Player.upgrade.values():
            i[0]=0
    else:
        en.Player.upgrade=en.Player.upgrade_lst[0]
    while True:
        x,y=ge.loop(True)
        gp.screen.blit(menu_background,(0,0))
        up_button.clear()
        for key, button in up_button.dict.items():
            up_level=en.Player.upgrade[key][0]
            pos=button.rect.midright
            up_button.sur.blit(detail_text[key][up_level],pos)
            up_button.sur.blit(up_font["small"].render("Level {}/{}".format(up_level,len(detail_text[key])-1)),(pos[0],pos[1]+30))
        choice=up_button.draw((x,y),clear=False)
        if max_upgrade == None:
            num=ge.star_left
        else:
            num=max_upgrade
            continue_button.draw()
            continue_button.collide((x,y))
        gp.screen.blit(up_font["big"].render("You have {} star left".format(num)),(292,160))        
        gp.screen.blit(button_img[2],return_rect)
        
        reset_button.draw()
        reset_button.collide((x,y))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                ge.save_exit()
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                click_sound.play()
                if choice in keys:
                    if max_upgrade == None:
                        if en.Player.upgrade[choice][0] < len(detail_text[choice])-1 and ge.star_left>0:
                            en.Player.upgrade[choice][0] +=1
                            ge.star_left-=1
                    else:
                        if en.Player.upgrade[choice][0] < len(detail_text[choice])-1 and max_upgrade > 0:
                            en.Player.upgrade[choice][0] +=1
                            max_upgrade-=1
                elif return_rect.collidepoint(x,y):
                    return False
                elif reset_button.is_pressed:
                    if max_upgrade != None:
                        max_upgrade=main_upgrade
                        for i in en.Player.upgrade.values():
                            i[0]=0
                    else:
                        for i in en.Player.upgrade.values():
                            ge.star_left += i[0]
                            i[0]=0
                elif continue_button.is_pressed:
                    return True
            up_button.scroll(event)
        close_screen.open()      

menu_background=gp.image("Background","menu background")
title=gp.image("Background","title")
bar=[gp.scale(img,(290,100)) for img in button_img[:2]]
menu_option=("Play","Upgrade","Credit")
credit_text=gp.image('Other',"Credit")
menu_button=gp.ButtonLst(menu_option,bar,(701,240),20,[[[gp.Font(60).render(i),(40,25)]] for i in menu_option])
def menu():
    music.load_music("Background","music.mp3")
    def credit():
        while True:
            gp.screen.blit(menu_background,(0,0))
            gp.screen.blit(credit_text,(300,0))
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                    return False
                elif event.type==pygame.QUIT:
                    ge.save_exit()
            ge.loop()
    while True:
        x,y=ge.loop()
        gp.screen.blits(((menu_background,(0,0)),(title,(0,0))))
        choice=menu_button.draw((x,y))
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                click_sound.play()
                if choice=="Play":
                    level()
                elif choice=="Upgrade":
                    upgrade()
                elif choice=="Credit":
                    credit()
            elif event.type==pygame.QUIT:
                ge.save_exit()

try:
    ge.get_history()
    menu()
except:
    ge.save_exit()


