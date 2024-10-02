import pygame
# from pygame.locals import *
import sys

def image_rect(place, width, height, scale, x, y):
    image = pygame.image.load(place).convert_alpha()
    image = pygame.transform.scale(image, (int(width / scale), int(height /scale)))
    rect = image.get_rect(topleft = (x,y))

    return image, rect

def meruem_animation():
    global meruemindx, meruemimage
    meruemindx += 0.1
    if meruemindx >= len(meruemlist): meruemindx = 0
    meruemimage = meruemlist[int(meruemindx)]
    
pygame.init()

screen = pygame.display.set_mode((500, 750))
pygame.display.set_caption('Flappy Meruem')
clock = pygame.time.Clock() 

font = pygame.font.Font('font/Pixeltype.ttf', 50)

bg,bg_rect = image_rect(('image/bg.png'), (437*1.2), (791*1.2), 1, 0,0)


#meruem
meruembottom = 740
meruem1, meruem1_rect = image_rect(('image/meruem/1.png'), 1300, 700, 6, 0,0)
meruem2, meruem2_rect = image_rect(('image/meruem/2.png'), 1300, 700, 6, 0,0)
meruem3, meruem3_rect = image_rect(('image/meruem/3.png'), 1300, 700, 6, 0,0)
meruem4, meruem4_rect = image_rect(('image/meruem/4.png'), 1300, 700, 6, 0,0)
meruem5, meruem5_rect = image_rect(('image/meruem/5.png'), 1300, 700, 6, 20,meruembottom)
meruemlist = [meruem1, meruem2,meruem3,meruem4,meruem5]
meruemindx = 0
meruemimage = meruemlist[meruemindx]

running = True
gravity = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit() 
            sys.exit()
        if running:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gravity = -20


    if running:
        screen.blit(bg, (0,0))
        
        meruem_animation()
        gravity += 1
        meruem5_rect.y += gravity

        if meruem5_rect.bottom >= meruembottom:
             meruem5_rect.bottom = meruembottom

        screen.blit(meruemimage, meruem5_rect)



    else:
        running = False


    pygame.display.update()
    clock.tick(60)