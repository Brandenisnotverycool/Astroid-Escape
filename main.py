import sys, pygame, random, pandas as pd
from ship import Ship
from asteroid import Asteroid
from pygame.locals import *

pygame.init()
screen_info=pygame.display.Info()
size=(width,height)=(int(screen_info.current_w*0.5), int(screen_info.current_h*0.5))
window=pygame.display.set_mode(size)
clock=pygame.time.Clock()
color=(40,0,40)
window.fill(color)
df = pd.read_csv('game_info.csv')
asteroids = pygame.sprite.Group()

numLevels=df['LevelNum'].max()

level=df['LevelNum'].min()

levelData=df.iloc[level]
asteroidCount=levelData['AsteroidCount']
player = Ship((levelData['PlayerX'], levelData['PlayerY']), 50)

def init():
    global asteroidCount,asteroids,levelData
    levelData = df.iloc[level]
    player.reset((levelData['PlayerX'], levelData['PlayerY']))
    asteroids.empty()
    asteroidCount=levelData['AsteroidCount']
    for i in range(asteroidCount):
        asteroids.add(Asteroid((random.randint(50, width-50), random.randint(50,height-50)), random.randint(15,60)))

def win():
    font=pygame.font.SysFont(None,70)
    text=font.render("Misson Success", True,(255,0,0))
    text_rect=text.get_rect()
    text_rect.center=(width/2,height/2)
    while True:
        window.fill(color)
        window.blit(text,text_rect)
        pygame.display.flip()
def main():
    global level, asteroids
    init()
    while level <= numLevels:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    player.speed[0] = 3
                if event.key == pygame.K_LEFT:
                    player.speed[0]= -3
                if event.key == pygame.K_UP:
                    player.speed[1]= -3
                if event.key == pygame.K_DOWN:
                    player.speed[1]= 3
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_RIGHT:
                    player.speed[0]= 0
                if event.key == pygame.K_LEFT:
                    player.speed[0]= 0
                if event.key == pygame.K_UP:
                    player.speed[1]= 0
                if event.key == pygame.K_DOWN:
                    player.speed[1]= 0
        window.fill(color)
        player.update()
        asteroids.update()
        gets_hit=pygame.sprite.spritecollide(player,asteroids,False)
        asteroids.draw(window)
        window.blit(player.image, player.rect)
        pygame.display.flip()

        if player.checkReset(width):
            if level == numLevels:
                break
            else:
                level += 1
                init()
        elif gets_hit:
            player.reset((levelData['PlayerX'], levelData['PlayerY']))
    win()
if __name__ == '__main__':
    main()






