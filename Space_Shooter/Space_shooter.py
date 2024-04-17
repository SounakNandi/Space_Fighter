import pygame
import random
import time

pygame.init()

screen_width = 600
screen_height = 800

FPS = 60
game_over = False
game_started = False
endscreen_time = 1

score = 0

font = pygame.font.Font(None, 36)
black = (0,0,0)
white = (255,255,255)

window = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Space Shooter") 

spaceship_image = pygame.image.load('picture\\spaceship.png')
spaceship_speed = 5
spaceship_x = 268
spaceship_y = 720

asteroid1_image = pygame.transform.scale(pygame.image.load('picture\\asteroid1.png'),(30,30))
asteroid2_image = pygame.transform.scale(pygame.image.load('picture\\asteroid2.png'),(50,50))
asteroid_speed = 5
asteroid_list = []
asteroid_images = [asteroid1_image,asteroid2_image]
asteroid_frequency = 0.03

bullet_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('picture\\bullet.png'),(50,30)),90)
bullet_speed = 10
bullet_list = []
bullet_fired = 0
bullet_interval = 0.5  

explosion_image = pygame.transform.scale(pygame.image.load('picture\\explosion.png'),(100,100))
explosion_list = []
explosion_time = 0.5


def draw_text(text, font, size, color, surface, x, y):

    font = pygame.font.Font(None, size)
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_screen():

    window.fill(black)
    
    if not game_started:
        draw_text("Press `SPACE` to Start", font,50, white, window, screen_width//2, 300)
        draw_text("RULES", font,40, white, window, screen_width//2, 400)
        draw_text("Press `space` to fire", font,35, white, window, screen_width//2, 440)
        draw_text("Use `left , right` arrows to move", font,35, white, window, screen_width//2, 470)
    else:
        window.blit(spaceship_image, (spaceship_x, spaceship_y))
        for asteroid in asteroid_list:
            window.blit(asteroid[2], (asteroid[0], asteroid[1]))
        for bullet in bullet_list:
            window.blit(bullet_image, (bullet[0], bullet[1]))
        for explosion in explosion_list:
            window.blit(explosion_image, (explosion[0]-explosion_image.get_width()//4, explosion[1]-explosion_image.get_width()//4))
        draw_text('score: '+str(score),font,40,white,window,80,30)
    
    pygame.display.update()

def spaceship_movement(key_pressed):

    global spaceship_x
    
    if key_pressed[pygame.K_LEFT] and spaceship_x > 5 :
        spaceship_x -= spaceship_speed
    if key_pressed[pygame.K_RIGHT] and spaceship_x < screen_width-spaceship_image.get_width()-5:
        spaceship_x += spaceship_speed

def asteroids():

    def create_asteroids():
    
        if random.random() < asteroid_frequency:
            asteroid_x = random.randint(50,500)
            asteroid_list.append([asteroid_x,0,random.choice(asteroid_images)])

    def asteroid_movement():

        global asteroid_list
        
        for asteroid in asteroid_list:
            if asteroid[2] == asteroid1_image :
                asteroid[1] += asteroid_speed + 3
                if asteroid[1] > screen_height :
                    asteroid_list.remove(asteroid)
            else:
                asteroid[1] += asteroid_speed
                if asteroid[1] > screen_height :
                    asteroid_list.remove(asteroid)

    create_asteroids()
    asteroid_movement()

def bullet(key_pressed):

    global bullet_fired,bullet_interval
    
    if key_pressed[pygame.K_SPACE]:
        if time.time() - bullet_fired > bullet_interval:
            bullet_list.append([spaceship_x + (spaceship_image.get_width()//4) ,spaceship_y])
            bullet_fired = time.time()

def bullet_movement():

    for bullet in bullet_list:
        bullet[1] -= bullet_speed

def check_collision():

    global bullet_list,asteroid_list,game_over,explosion_list,score
    
    for bullet in bullet_list:
        bullet_rect = bullet_image.get_rect(topleft=(bullet[0], bullet[1]))
        for asteroid in asteroid_list:
            asteroid_rect = asteroid[2].get_rect(topleft=(asteroid[0], asteroid[1]))
            if bullet_rect.colliderect(asteroid_rect):
                bullet_list.remove(bullet)
                asteroid_list.remove(asteroid)

                explosion_x = asteroid[0]
                explosion_y = asteroid[1]
                explosion_list.append([explosion_x, explosion_y, time.time()])

                if asteroid[2] == asteroid1_image:
                    score += 2
                else:
                    score += 1

    explosion_list = [explosion for explosion in explosion_list if time.time() - explosion[2] < explosion_time]

    for asteroid in asteroid_list:
        asteroid_rect = asteroid[2].get_rect(topleft=(asteroid[0], asteroid[1]))
        spaceship_rect = spaceship_image.get_rect(topleft=(spaceship_x, spaceship_y))
        if asteroid_rect.colliderect(spaceship_rect):
            game_over = True
            return

def main():

    global game_over,game_started,score

    clock = pygame.time.Clock()

    while not game_over:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            game_started = True
        if game_started:
            spaceship_movement(key_pressed)
            bullet(key_pressed)

            asteroids()

            bullet_movement()

            check_collision()

        draw_screen()

    window.fill(black)
    draw_text("Game Over", font,48, white, window, screen_width // 2, screen_height // 2 - 25)
    draw_text("Final Score: " + str(score), font,36, white, window, screen_width // 2, screen_height // 2 + 25)
    pygame.display.update()
    pygame.time.wait(endscreen_time*1000)


    pygame.quit()

if __name__ == '__main__':
    main()
