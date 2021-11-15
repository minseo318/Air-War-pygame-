import pygame
import random
import math
import os
import sys
import time

FPS=60
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
screen_width=1920
screen_height=1080


#게임 시작
def runGame():
    global screen,clock,sprite_group,bullets,mobs,difficulty,score,player
    
    background=pygame.image.load("Image/sky.png")
    background=pygame.transform.scale(background,(1920,1080))
    
    time=0
    timer=0
    difficulty=1
    score=0
    
    sprite_group=pygame.sprite.Group()
    bullets=pygame.sprite.Group()
    mobs=pygame.sprite.Group()
       
    #플레이어 생성
    player=PlayerShip()
    sprite_group.add(player)
    
    #게임 루프
    running=True
    while running:
        
        for event in pygame.event.get():
            #키설정
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    player.shoot(sprite_group,bullets)
            
            #게임종료
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYUP: 
                if event.key==pygame.K_ESCAPE:
                    running=False
        
        #충돌 판정
        hits=pygame.sprite.groupcollide(mobs,bullets,True,True)
        for hit in hits:
            score+=100
        
        hits=pygame.sprite.spritecollide(player,mobs,False)
        for hit in hits:
            hit.kill()
            player.life-=1
            if player.life<=0:
                game_over()
        
        sprite_group.update()   
        screen.blit(background,(0,0))
        
        text(screen)
       
        sprite_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        
        #타이머
        time+=1
        if time>50/difficulty:
            score+=1
            mob_spawn()
            time=0
        
        timer+=1
        if timer%100==0:
            difficulty+=1
        
    pygame.quit()
    sys.exit()

#초기 설정
def initGame():
    global screen,clock
    
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
    pygame.init()
    screen=pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("제목")
    clock=pygame.time.Clock()
    
def game_over():
    screen.fill(WHITE)
    Font=pygame.font.Font("Font.ttf",200)
    gameover=Font.render("GAME OVER",True,RED)
    score_text=Font.render("점수 : "+str(score),True,BLACK)
    screen.blit(score_text,(100,170))
    life_text=Font.render("LEVEL : "+str(difficulty),True,BLACK)
    screen.blit(life_text,(100,0)) 
    gameover_rect=gameover.get_rect()
    gameover_rect.centerx=screen_width/2
    gameover_rect.centery=screen_height/2
    screen.blit(gameover,gameover_rect)
    pygame.display.update()
    time.sleep(3)
    print("점수"+str(score))
    print("LEVEL:"+str(difficulty))
    pygame.quit()
    sys.exit()
    
def mob_spawn():
    enemy=Mob()
    sprite_group.add(enemy)
    mobs.add(enemy)
    
def text(screen):
    #폰트
    Font=pygame.font.Font("Font.ttf",50)
    difficulty_text=Font.render("LEVEL : "+str(difficulty),True,BLACK)
    screen.blit(difficulty_text,(screen_width-200,0)) 
    score_text=Font.render("점수 : "+str(score),True,BLACK)
    screen.blit(score_text,(30,00)) 
    life_text=Font.render("LIFE : "+str(player.life),True,BLACK)
    screen.blit(life_text,(30,50)) 
    
#플레이어
class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("Image/player.png")
        self.rect=self.image.get_rect()
        self.rect.width*=2
        self.rect.height*=2
        self.image=pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
        
        self.rect.centerx=screen_width / 2
        self.rect.centery=screen_height - 100
        self.dx=0
        self.dy=0
        
        self.life=5
        self.speed=17
        
    def update(self):
        self.dx=0
        self.dy=0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.dx=-self.speed
        if keystate[pygame.K_d]:
            self.dx=self.speed
        if keystate[pygame.K_w]:
            self.dy=-self.speed
        if keystate[pygame.K_s]:
            self.dy=self.speed
        self.rect.x+=self.dx
        self.rect.y+=self.dy
        if self.rect.right>=screen_width:
            self.rect.right=screen_width
        if self.rect.left<=0:
            self.rect.left=0
        if self.rect.bottom>=screen_height:
            self.rect.bottom=screen_height
        if self.rect.top<=0:
            self.rect.top=0
        
    def shoot(self,all_sprites,bullets):
        bullet=Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x,player_y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("Image/bullet.png")
        self.rect=self.image.get_rect()
        self.rect.width*=2
        self.rect.height*=2
        self.image=pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
        
        self.rect.bottom=player_y
        self.rect.centerx=player_x
        self.dy=-20

    def update(self):
        self.rect.y+=self.dy
        if self.rect.bottom<=0:
            self.kill()
            
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        mob_list=[]
        for i in range(1,6):
            mob_list.append(pygame.image.load("Image/enemy"+str(i)+".png"))
        self.image=random.choice(mob_list)
        self.rect=self.image.get_rect()
        self.rect.width*=2
        self.rect.height*=2
        self.image=pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
        
        self.rect.x=random.randrange(screen_width-self.rect.width)
        self.rect.y=-100
        
        self.speed=1
        self.dx=random.randint(-5,5*self.speed)
        self.dy=random.randint(5,20*self.speed)
    
    def update(self):
        self.rect.x+=self.dx
        self.rect.y+=self.dy
        
        if self.rect.top>=screen_height:
            self.kill()
        
initGame()
runGame()