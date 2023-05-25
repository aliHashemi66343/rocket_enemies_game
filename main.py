import random

import pygame
from pygame.locals import (

    K_UP,

    K_DOWN,

    K_LEFT,

    K_RIGHT,

    K_ESCAPE,

    KEYDOWN,

    K_SPACE,

    QUIT,

)

SCREEN_WIDTH = 800

SCREEN_HEIGHT = 600
pygame.init()

pygame.display.set_caption("tutorial game")
# icon = pygame.image.load('bear.png')
# pygame.display.set_icon(icon)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

rocketImg = pygame.image.load("rocket.png")
rocketX = 370
rocketY = 480

fireImg = pygame.image.load("fire.png")
fireX = 370
fireY = 480

enemy_img_paths=["ghost_1.png","ghost_2.png","ghost_3.png","ghost_4.png","ghost_5.png",]

def insert_text(text,font_size,color,x_y,font_name="freesansbold.ttf"):
    font = pygame.font.Font(font_name, font_size)
    text = font.render(text, True, color)
    X=x_y[0]
    Y=x_y[1]
    X-=text.get_width()/2
    Y-=text.get_height()/2

    screen.blit(text, (X,Y))
    # pygame.display.flip()

def modifies_for_two_enemies_dont_overlap(enem1,enem2):
    modifies=[]
    if enem2['x'] < enem1['x'] < enem1['x']+enem2['obj'].get_width():
        diff_value=abs(enem2['x']-(enem1['x']+enem1['obj'].get_width()))
        modifies.append( {"dir":"horiz",'value':diff_value})
    if enem2['y'] < enem1['y'] < enem1['y']+enem2['obj'].get_height():
        diff_value = abs(enem2['y'] - (enem1['y'] + enem1['obj'].get_height()))
        modifies.append({"dir": "vert", 'value': diff_value})
    return modifies
def enemies_overlap(enem1,enem2):
    modifies=[]
    if enem2['x'] < enem1['x'] < enem1['x']+enem2['obj'].get_width():
        return True
    else:
        return False
    #     modifies.append( {"dir":"horiz",'value':diff_value})
    # if enem2['y'] < enem1['y'] < enem1['y']+enem2['obj'].get_height():
    #     diff_value = abs(enem2['y'] - (enem1['y'] + enem1['obj'].get_height()))
    #     modifies.append({"dir": "vert", 'value': diff_value})
    # return modifies


def enemies_prepare_blit(enemy_number,enemy_img_paths):
    enemies=[]
    for i in range(0,enemy_number):
        enemies.append({"img":enemy_img_paths[random.randint(0,len(enemy_img_paths)-1)],"x":random.randint(int(SCREEN_WIDTH/3),int(SCREEN_WIDTH-SCREEN_WIDTH/3)),"y":random.randint(0,int(SCREEN_HEIGHT/2)),"is_alive":True,"to_right":True,"to_left":False,'velocity':random.randint(1,11)*0.1,"life_time":random.randint(1,4)})


    for ghost_img in enemies:

        enemyGhostImg=pygame.image.load(ghost_img["img"])

        ghost_img['obj']=enemyGhostImg

    # for j in range(len(enemies)):
    #     for k in range(len(enemies[:j]+enemies[j+1:])):
    #         list1=enemies[:j]+enemies[j+1:]
    #         if len(modifies_for_two_enemies_dont_overlap(enemies[j],list1[k]))>0:
    #             if modifies_for_two_enemies_dont_overlap(enemies[j],list1[k])[0]['dir']=="horiz":
    #                 enemies[j]['x']-=modifies_for_two_enemies_dont_overlap(enemies[j],list1[k])[0]['value']
    for ghost_img in enemies:
        enemyGhostX = ghost_img['x']
        enemyGhostY = ghost_img['y']

        screen.blit(ghost_img['obj'], (enemyGhostX, enemyGhostY))
    return enemies
enemies = enemies_prepare_blit(5,enemy_img_paths)


def rocket_display(x, y):
    screen.blit(rocketImg, (x, y))
    # pygame.display.flip()


def enemy_display(x,y,object,enemy_lifetime):
    screen.blit(object,(x,y))
    insert_text(str(enemy_lifetime),20,(255,120,0),(x-10,y-10))

def fire_display(x,y):
    screen.blit(fireImg,(x,y))


def is_rocket_in_screen(x, y):

    if SCREEN_WIDTH - rocketImg.get_width() >= x >= 0 and 0 <= y <= SCREEN_HEIGHT - rocketImg.get_height():
        return True
    else:
        return False




# def which_dir_is_closed(x,y)
def left_locked(x,y):
    if x<0:
        return True
    else:
        return False
def up_locked(x,y):
    if y<0:
        return True
    else:
        return False
def right_locked(x,y):
    if x>SCREEN_WIDTH-rocketImg.get_width():
        return True
    else:
        return False
def bottom_locked(x,y):
    if y >SCREEN_HEIGHT-rocketImg.get_height():
        return True
    else:
        return False
def rocket_crashed_enemy(enemy):
    # from left
    Xe = enemy['x']
    Ye = enemy['y']
    He = enemy['obj'].get_height()
    We = enemy['obj'].get_width()

    Xr = rocketX
    Yr = rocketY
    Hr = rocketImg.get_height()
    Wr = rocketImg.get_width()

    from_left= (Xr+Wr<Xe) and (Xr + Wr > Xe and Ye - He < Yr < Ye + Hr)
    from_right= (Xr>Xe+We) and (Xr < Xe + We and Ye - He < Yr < Ye + Hr)

    from_top= (Yr-Wr<Ye) and (Xe - Wr < Xr < Xe + We and Yr+Hr > Ye)
    from_bottom=(Yr>Ye+We) and (Xe - Wr < Xr < Xe + We and Yr < Ye+He)

    print(f"from left {from_left}\n from bottom {from_bottom}\n from top {from_top}\n from right {from_right}\n")
    return from_left or from_bottom or from_top or from_right
# to_right=True
# to_left=False
firing=False
running = True
not_losed=True
is_winner=False


def enemy_is_fired(enemy):
    return enemy['y'] + enemy['obj'].get_height() > fireY >= enemy['y'] and enemy['x'] < fireX < enemy['x'] + enemy[
        'obj'].get_width()


while running:
    if not_losed:
        if is_winner:
            insert_text("YOU WON!",50,(0,255,0),((screen.get_width()) / 2, (screen.get_height()) / 2))


            continue
        screen.fill((255, 255, 255))
        rocket_display(rocketX, rocketY)
        for enemy in enemies:

            enemy_display(enemy['x'], enemy['y'],enemy['obj'],enemy['life_time'])
        x_temp=rocketX
        y_temp=rocketY
        keys = pygame.key.get_pressed()

        for enemy in enemies:
            Xe = enemy['x']
            Ye = enemy['y']
            if rocket_crashed_enemy(enemy):
                not_losed=False

            if (right_locked(enemy['x'], enemy['y'])!=True and enemy["to_right"]==True):

                enemy['x'] +=enemy['velocity']
                if right_locked(enemy['x'], enemy['y'])==True:
                    enemy["to_right"]=False
                    enemy["to_left"]=True
                enemy_display(enemy['x'], enemy['y'], enemy['obj'],enemy['life_time'])
            elif(left_locked(enemy['x'], enemy['y']) != True and enemy["to_left"] == True):
                enemy['x'] -=enemy['velocity']
                if left_locked(enemy['x'], enemy['y'])==True:
                    enemy["to_right"]=True
                    enemy["to_left"]=False
                enemy_display(enemy['x'], enemy['y'], enemy['obj'],enemy['life_time'])
        if firing==True:
            fire_display(fireX, fireY)
            fireY -= 1.5
            ind=0
            for enemy in enemies:
                if enemy_is_fired(enemy):
                    print(f"tappped enemy time life :{enemy['life_time']}")

                    if enemy['life_time']==0:
                        enemies.pop(ind)
                    else:
                        enemy['life_time']-=1
                    firing=False

                ind+=1
            if fireY<0:
                firing=False
        if keys[K_SPACE]:
            fireX=rocketX+rocketImg.get_width()/2-7
            fireY=rocketY-4
            firing=True

        if keys[K_LEFT]:
            # print(f"rocket in screen:{is_rocket_in_screen(rocketX, rocketY)}")
            if not left_locked(rocketX, rocketY):
                rocketX -= 0.8

                rocket_display(rocketX, rocketY)
        if keys[K_RIGHT]:
            if not right_locked(rocketX, rocketY):
                rocketX += 0.8
                rocket_display(rocketX, rocketY)
        if keys[K_UP]:
            if not up_locked(rocketX,rocketY):
                rocketY -= 0.8
                rocket_display(rocketX, rocketY)
        if keys[K_DOWN]:
            if not bottom_locked(rocketX,rocketY):
                rocketY += 0.8
                rocket_display(rocketX, rocketY)
        if len(enemies)==0:
            is_winner=True


    else:
        insert_text("YOU LOSE!",50,(255,0,0),((screen.get_width()) / 2, (screen.get_height()) / 2),)

        # rocket()
    for event in pygame.event.get():
        # print(event)

        # Did the user hit a key?

        if event.type == KEYDOWN:
            # print(event.unicode)
            # print(event.key)

            # Was it the Escape key? If so, stop the loop.
            # if event.key == K_UP:
            #     rocketY -= 1
            #     rocket(rocketX, rocketY)
            # if event.key == K_DOWN:
            #     rocketY += 1
            #     rocket(rocketX, rocketY)
            # if event.key == K_LEFT:
            #     rocketX-=1
            #     rocket(rocketX,rocketY)
            # if event.key == K_RIGHT:
            #     rocketX += 1
            #     rocket(rocketX, rocketY)
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.

        elif event.type == QUIT:

            running = False
    pygame.display.flip()