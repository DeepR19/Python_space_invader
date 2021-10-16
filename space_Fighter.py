import pygame
from module import *
import random
pygame.font.init()

FPS = 60

main_font = pygame.font.SysFont("comicsans",50)
lost_font = pygame.font.SysFont("comicsans",70)
stroke=8

# enemies variable
enemies = []
enemy_vel = 1

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Platformer__DeepR19")

player = Player(200, 630)

clock = pygame.time.Clock()

# controls for player ship
def keyStroke():
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (player.x - stroke > 0):
        player.x -= stroke
    if (keys[pygame.K_UP] or  keys[pygame.K_w]) and (player.y - stroke - 50 > 0):
        player.y -= stroke
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (player.y + stroke + player.get_height() +30< height):
        player.y += stroke
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (player.x + stroke + player.get_width() < width):
        player.x += stroke
    if (keys[pygame.K_SPACE]):
        player.shoot()



def main():
    lives=5
    lost_count = 0
    level=0
    wave_length = 5
    runs =  True
    lost = False
    laser_vel =4

    # abstraction
    def redraw_window():
        screen.blit(BG_Main,(0,0))

        lives_label = main_font.render(f"Lives: {lives}",1, (255,255,255),)
        level_label = main_font.render(f"Level: {level}",1, (255,255,255),)

        screen.blit(lives_label, (10,0))
        screen.blit(level_label, (width - level_label.get_width() -10, 0))    
    
        # labels of screen
        for enemy in enemies:
            enemy.draw(screen)
        
        player.draw(screen)

        if lost:
            lost_label = lost_font.render("You Lost !!", 1, (255,255,255))
            screen.blit(lost_label, (width/2-lost_label.get_width()/2, 350))

        pygame.display.update()

    # main code
    while runs:
        clock.tick(FPS)
        redraw_window()
        if lives <= 0 or player.health <=0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS *3:
                runs =False
            else:
                continue

        if len(enemies)==0:
            level += 1
            wave_length += 5
            
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, width-100), random.randrange(-1500,-100), random.choice(["red","green","blue"]))
                enemies.append(enemy)

        # quit function
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keyStroke()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel , player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)
   
def main_menu():
    title_font = pygame.font.SysFont("cosmicsans",70)
    run = True
    while run:
        screen.blit(BG_Main, (0,0))
        title_label = title_font.render("Press the mouse to begin...",1, (255,255,255))
        screen.blit(title_label, (width/2 - title_label.get_width()/2, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

main_menu()