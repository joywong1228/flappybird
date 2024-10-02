import pygame
import sys
import random

class Button():
    def __init__(self, x,y, w, h,scale, image):
        self.image = pygame.transform.scale(image,(int(w / scale), int(h /scale)))
        self.rect = self.image.get_rect(center = (x,y))

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        elif pygame.key.get_pressed()[pygame.K_SPACE] == 1:
            action = True
        
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, scale, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.list = []
        self.indx = 0
        for num in range(1, 5):
            img = pygame.transform.scale((pygame.image.load(f'image/meruem/{num}.png').convert_alpha()), (int(width / scale), int(height /scale)))
            self.list.append(img)
        self.image = self.list[self.indx]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.gravity = 0
        self.clicked = False

    def update(self):

        if flying:
            #gravity
            self.gravity += 1.2
            self.rect.y += int(self.gravity)
            if self.gravity > 8:
                self.gravity = 8
            if self.rect.bottom >= (screenh-20):
                self.rect.bottom = (screenh-20)

        if not gameover:
            #jump
            keys = pygame.key.get_pressed()
            if (pygame.mouse.get_pressed()[0] == 1 or keys[pygame.K_SPACE]) and not self.clicked:
                self.clicked = True
                self.gravity = -18
            elif not (pygame.mouse.get_pressed()[0] == 1 or keys[pygame.K_SPACE]):
                self.clicked = False

            #animation
            self.indx += 0.1
            if self.indx >= len(self.list):
                self.indx = 0
            self.image = self.list[int(self.indx)]

            #rotate (not good look)
            # self.image = pygame.transform.rotate(self.list[int(self.indx)], self.gravity * -1)
        else:
             self.image = pygame.transform.rotate(self.list[int(self.indx)], self.gravity + 90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, scale, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale((pygame.image.load('image/pillar.png').convert_alpha()),(int(width / scale), int(height /scale)))
        self.rect = self.image.get_rect()
        #position
        pipegap = 265
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipegap / 2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipegap / 2)]
        
    def update(self):
        self.rect.x -= scrollspeed
        if self.rect.right < 0:
            self.kill() 
                
def image_rect(place, width, height, scale, x, y):
    image = pygame.image.load(place).convert_alpha()
    image = pygame.transform.scale(image, (int(width / scale), int(height /scale)))
    rect = image.get_rect(center=(x, y))
    return image, rect

def text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def reset():
    pipegroup.empty()
    meruem.rect.x = 1
    meruem.rect.y = (screenh/2)
    score = 0
    return score

pygame.init()

screenw = 600
screenh = 950
screen = pygame.display.set_mode((screenw, screenh))
pygame.display.set_caption('Flappy Meruem')
clock = pygame.time.Clock()

font = pygame.font.Font('font/Pixeltype.ttf', 60)
white = (255,255,255)

bg, bg_rect = image_rect('image/bg.png', screenw, screenh, 1, 0, 0)
restartimg = pygame.image.load('image/restart.png').convert_alpha()

meruemgroup = pygame.sprite.Group()
meruem = Player(1300, 700, 7.5, 1, (screenh/2))
meruemgroup.add(meruem)

pipegroup = pygame.sprite.Group()
running = True
flying = False
gameover = False
passpipe = False
score = 0

scrollspeed = 5
pipfrequency = 1500
lastpipe = pygame.time.get_ticks() - pipfrequency
restartbutton = Button(screenw//2, screenh//2 ,999, 266, 5,restartimg)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN) and not flying:
            if not flying and not gameover:
                flying = True        

    if running:
        screen.blit(bg, (0, 0))
        
        meruemgroup.draw(screen)
        meruemgroup.update()

        pipegroup.draw(screen)


        if len(pipegroup) > 0:
            if meruemgroup.sprites()[0].rect.left > pipegroup.sprites()[0].rect.left:
                if meruemgroup.sprites()[0].rect.right > pipegroup.sprites()[0].rect.right:
                    if not passpipe:
                        passpipe = True
                if passpipe:
                     if meruemgroup.sprites()[0].rect.left > pipegroup.sprites()[0].rect.right:
                         score += 1
                         passpipe = False

        text(str(score), font, white, int(screenw/2), 30)


        if flying:
            currenttime = pygame.time.get_ticks()
            pipegroup.update()

            if currenttime - lastpipe > pipfrequency:
                pipeh = random.randint(-180, 180)
                btm_pipe = Pipe(screenw,(400)+ pipeh,100,650, 1, 1)
                top_pipe = Pipe(screenw,(400)+ pipeh,100,650, 1, -1)
                pipegroup.add(btm_pipe)
                pipegroup.add(top_pipe)

                lastpipe = currenttime


            if meruem.rect.bottom >= (screenh-20):
                gameover = True
                flying = False

            if pygame.sprite.groupcollide(meruemgroup, pipegroup, False, False) or meruem.rect.top < 0: #if true then it will delete the group
                gameover = True

    if gameover:
        if restartbutton.draw():
            gameover = False
            score = reset()


    pygame.display.update()
    clock.tick(60)
