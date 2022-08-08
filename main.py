import pygame as pg
import random
import os
import sys
import math
import time

pg.font.init()
pg.mixer.init()

WIN_WIDTH = 700
WIN_HEIGHT = 600
WIN = pg.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pg.display.set_caption("Kars")

car_width,car_height = 70,80
div_width,div_height = 30,110

tree_width,tree_height = 80,150

obstacle_width,obstacle_height = 80,80
path1,path2,path3 = 180,320,460

BACKGROUND = pg.transform.scale(pg.image.load(os.path.join("game/resources/imgs","bg.png")),(WIN_WIDTH,WIN_HEIGHT))
ROAD = pg.transform.scale(pg.image.load(os.path.join("game/resources/imgs","road.png")),(400,WIN_HEIGHT))
CAR = pg.transform.rotate(pg.transform.scale(pg.image.load(os.path.join("game/resources/imgs","car.png")),(car_width,car_height)),90)
LOGO = pg.image.load(os.path.join("game/resources/imgs","logo.png"))
TREE = [pg.image.load(os.path.join("game/resources/imgs","oak.png")),pg.image.load(os.path.join("game/resources/imgs","btree.png")),pg.image.load(os.path.join("game/resources/imgs","gtree.png")),pg.image.load(os.path.join("game/resources/imgs","coco.png"))]
OBSTACLE = [pg.image.load(os.path.join("game/resources/imgs","brcd.png")),pg.image.load(os.path.join("game/resources/imgs","vlc.png")),pg.image.load(os.path.join("game/resources/imgs","hole.png"))]
OBSTACLE = [pg.transform.scale(i,(80,80)) for i in OBSTACLE]
DIV = pg.transform.scale(pg.image.load(os.path.join("game/resources/imgs/divider.png")),(div_width,div_height))
tree_no = 9
Tree_list_l = [random.choice(TREE) for _ in range(tree_no)] 
Tree_list_r = [random.choice(TREE) for _ in range(tree_no)]

obst_list = [random.choice(OBSTACLE) for _ in range(3)]

FPS = 60
vel = 5
game_speed = 8
Font = pg.font.SysFont("comicsans",40)
Fon = pg.font.SysFont("comicsans",120)
score = 0
level = 1

def Draw(car,score,div_l,div_r,tree_l,tree_r,obst,level):
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(ROAD,(150,0))
    
    score_txt = Font.render("Score: " + str(score),1,(250,250,250))
    Level_txt = Font.render("Level: "+ str(level),1,(250,250,250))

    for i in range(4):
        WIN.blit(DIV,(div_l[i].x,div_l[i].y))
        WIN.blit(DIV,(div_r[i].x,div_r[i].y))

    WIN.blit(CAR,(car.x,car.y))

    for i in range(3):
        WIN.blit(obst_list[i],(obst[i].x,obst[i].y))

    for i in range(tree_no):
        WIN.blit(Tree_list_l[i],(tree_l[i].x,tree_l[i].y))
        WIN.blit(Tree_list_r[i],(tree_r[i].x,tree_r[i].y))  

    pg.draw.rect(WIN,(10,10,100),pg.Rect(0,0,150,40))
    WIN.blit(Level_txt,(10,10))
  
    pg.draw.rect(WIN,(10,10,100),pg.Rect(550,0,150,40))
    WIN.blit(score_txt,(WIN_WIDTH-score_txt.get_width()-10,10))

    pg.display.update()

def car_movement(key,car):
    global CAR
    if key[pg.K_LEFT] and car.x -vel > 130:
        car.x -= vel
    if key[pg.K_RIGHT] and car.x + vel < 490:
        car.x += vel
    if key[pg.K_UP] and car.y - vel > 0:
        car.y -= vel
    if key[pg.K_DOWN] and car.y + vel < 540:
        car.y += vel

def div_mov(div):
    if div.y > 660:
        div.y = -110
    div.y += game_speed

def path():
    return random.choice([path1,path2,path3])

def obst_mov(obst,i):
    global score,level,game_speed
    if obst.y > 600:
        obst.y = -100
        obst.x = path()
        obst_list[i] = random.choice(OBSTACLE)
        score += 1
    if score > (level*5):
        level += 1
        game_speed += 1
    obst.y += game_speed

def tree_mov(tr,i,list):
    if tr.y > 550:
        tr.y = -65
        tree_append(list,i)
    tr.y += game_speed

def tree_append(Tree_list,i):
    Tree_list[i] = random.choice(TREE)

def dist(x1,y1,x2,y2):
    return math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

def black_screen():
    temp = 0.6
    for _ in range(1000):
        pg.draw.rect(WIN,(0,0,10),pg.Rect(0,0,700,temp))
        temp += 0.6
        pg.display.update()

def over():
    global score

    game_over = Fon.render("Game Over",1,(250,0,0))

    run = True
    while run:
        global score,level,game_speed

        WIN.blit(game_over,(150,100))
        WIN.blit(Fon.render("Score: "+ str(score),1,(250,250,0)),(160,250))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit()
        
        if pg.key.get_pressed()[pg.K_r]:
            score = 0
            level = 0
            game_speed = 8
            main() 
            pg.quit()
            sys.exit()
        
        pg.draw.rect(WIN,(250,250,250),pg.Rect(0,500,700,50))
        WIN.blit(Font.render("Press R to restart",1,(0,0,0)),(40,510))

        pg.display.update()
        

def main():

    car = pg.Rect(340,500,car_width,car_height)
    div_l = [pg.Rect(265,-110,div_width,div_height),pg.Rect(265,90,div_width,div_height),pg.Rect(265,280,div_width,div_height),pg.Rect(265,470,div_width,div_height)]
    div_r = [pg.Rect(405,-110,div_width,div_height),pg.Rect(405,90,div_width,div_height),pg.Rect(405,280,div_width,div_height),pg.Rect(405,470,div_width,div_height)]
    obst1 = [pg.Rect(path(),-100,obstacle_width,obstacle_height),pg.Rect(path(),-300,obstacle_width,obstacle_height),pg.Rect(path(),-500,obstacle_width,obstacle_height)]

    tree_l,tree_r,temp = [],[],0
    for i in range(tree_no):
        tree_l.append(pg.Rect(30,temp,tree_width,tree_height))
        tree_r.append(pg.Rect(600,temp,tree_width,tree_height))
        temp += 65


    clock = pg.time.Clock()
    run = True

    while run:

        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit()

        for i in obst1:
            if dist(car.x,car.y,i.x,i.y) < 80:
                black_screen()
                over()

        key_pressed = pg.key.get_pressed()
        car_movement(key_pressed,car)

        for i in range(4):
            div_mov(div_l[i])
            div_mov(div_r[i])

        for i in range(3):
            obst_mov(obst1[i],i)

        for i in range(tree_no):
            tree_mov(tree_l[i],i,Tree_list_l)
            tree_mov(tree_r[i],i,Tree_list_r)

        Draw(car,score,div_l,div_r,tree_l,tree_r,obst1,level)
        
    main()

if __name__ == "__main__":
    main()