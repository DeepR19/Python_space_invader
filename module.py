import pygame

width = 800
height = 750

# Load Enemy Image
Red_Space_Ship = pygame.image.load("./assets/pixel_ship_red_small.png")
Green_Space_Ship = pygame.image.load("./assets/pixel_ship_green_small.png")
Blue_Space_Ship = pygame.image.load("./assets/pixel_ship_blue_small.png")

# Load Player Ship
Yellow_Space_Ship = pygame.image.load("./assets/pixel_ship_yellow.png")

# lasers
Red_Laser = pygame.image.load("./assets/pixel_laser_red.png")
Green_Laser = pygame.image.load("./assets/pixel_laser_green.png")
Blue_Laser = pygame.image.load("./assets/pixel_laser_blue.png")
Yellow_Laser = pygame.image.load("./assets/pixel_laser_yellow.png")

# Background
BG = pygame.image.load("./assets/background-black.png")
BG_Main = pygame.transform.scale(BG, (width,height))

class Laser:
    def __init__(self, x, y, img):
        self.x=x
        self.y=y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >=0)

    def collision(self, obj):
        return collide(obj, self)

    

# main component to make player and enemy ships
class Ship:
    CoolDown = 30
    def __init__(self, x, y, health=100):
        self.x=x
        self.y=y
        self.health=health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter=0
    
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.coolDown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def coolDown(self):
        if self.cool_down_counter >= self.CoolDown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

# player ship
class Player(Ship):
    def __init__(self, x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img = Yellow_Space_Ship
        self.laser_img = Yellow_Laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.coolDown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthBar(window)

    def healthBar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y+ self.ship_img.get_height() +10, self.ship_img.get_width() , 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y+ self.ship_img.get_height() +10, self.ship_img.get_width() * (self.health/ self.max_health) , 10))



# enemy ships
class Enemy(Ship):
    colorMap ={
        "red": (Red_Space_Ship, Red_Laser),
        "green": (Green_Space_Ship, Green_Laser),
        "blue": (Blue_Space_Ship, Blue_Laser)
    }
    def __init__(self, x,y,color,health=100):
        super().__init__(x,y,health)
        self.ship_img, self.laser_img = self.colorMap[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offser_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (offser_x, offset_y)) != None 
