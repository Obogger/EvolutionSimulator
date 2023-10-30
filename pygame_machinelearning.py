import pygame
import random
import time
import math
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_HEIGHT,SCREEN_WIDTH))



icon = pygame.image.load("man.png")
pygame.display.set_caption("Evolution")
pygame.display.set_icon(icon)


class Animal():
    def __init__(self,x,y, angle):
        raw_image = pygame.image.load("man2.png")
        self.img = pygame.transform.scale(raw_image, (50,50))
        self.x = x
        self.y = y
        self.angle = angle
        self.pasty = y
        self.pastx = x
        self.movement_deltaX = 0
        self.movement_deltaY = 0
        self.speed = 250
        self.hitbox = pygame.Rect(self.x,self.y,50,50)
        
    def draw_animal(self):
        if len(animal_array) > 100:
            animal_array.pop(0)
        screen.blit(self.img, (self.x, self.y))
        #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)

class Food():
    def __init__(self,x,y):
        raw_image = pygame.image.load("food.png")
        self.img = pygame.transform.scale(raw_image, (50,50))
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x,self.y,50,50)
    def draw_food(self):
        if len(food_array) > 15:
            food_array.pop(0)
        screen.blit(self.img, (self.x, self.y))



def animal_move(current_animal):
    current_animal.pastx = current_animal.x
    current_animal.pasty = current_animal.y
    current_animal.x += current_animal.movement_deltaX * delta_time
    current_animal.y += current_animal.movement_deltaY * delta_time
    if current_animal.x < 0:
        current_animal.x = 0
    if current_animal.x > SCREEN_WIDTH - (current_animal.img.get_width()):
        current_animal.x = SCREEN_WIDTH - (current_animal.img.get_width())
    if current_animal.y < 0:
        current_animal.y = 0
    if current_animal.y > SCREEN_HEIGHT - (current_animal.img.get_height()):
        current_animal.y = SCREEN_HEIGHT - (current_animal.img.get_height())
    current_animal.hitbox[0] = current_animal.x
    current_animal.hitbox[1] = current_animal.y
    check_collision(current_animal)
      
def check_collision(current_animal):
    for animal in animal_array:
        if current_animal.hitbox.colliderect(animal.hitbox) and current_animal != animal:
            current_animal.x = current_animal.pastx
            current_animal.y = current_animal.pasty
            current_animal.movement_deltaX = -current_animal.movement_deltaX
            current_animal.movement_deltaY = -current_animal.movement_deltaY
            current_animal.hitbox = pygame.Rect(current_animal.x, current_animal.y, current_animal.hitbox[2],current_animal.hitbox[3])
            #animal.x += (current_animal.movement_deltaX * delta_time) * 5
            #animal.y += (current_animal.movement_deltaX * delta_time) * 5
            #animal.hitbox = pygame.Rect(animal.x, animal.y, animal.hitbox[2],animal.hitbox[3])
    for food in food_array:
        if current_animal.hitbox.colliderect(food.hitbox):
            food_array.remove(food)
def spawn_animal():
    open = True
    animal = Animal(random.randint(500,500), 500,random.randint(0,360))
    for current_animal in animal_array:
        if animal.hitbox.colliderect(current_animal.hitbox):
            open = False
    if open:
        animal_array.append(animal)
        x, y = calcualte_vector_from_angle(animal.angle, animal.speed)
        animal.movement_deltaX += x
        animal.movement_deltaY += y
def spawn_food():
    food = Food(random.randint(0,SCREEN_WIDTH), random.randint(0,SCREEN_HEIGHT))
    food_array.append(food)

def calcualte_vector_from_angle(angle, speed):
    x = math.cos(math.radians(angle)) * speed
    y = math.sin(math.radians(angle)) * speed
    return x,y

def animal_choose_movement(current_animal):
    current_animal.angle += random.randint(-10,10)
    x, y = calcualte_vector_from_angle(current_animal.angle, current_animal.speed)
    current_animal.movement_deltaX = x
    current_animal.movement_deltaY = y
    
running = True
    
delta_time = 0

animal_array = []
food_array = []

FOOD_COOLDOWN = 50
while running:
    screen.fill((0,100,50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                spawn_animal()
    for current_animal in animal_array:
        animal_choose_movement(current_animal)
        animal_move(current_animal)
        current_animal.draw_animal()
    for current_food in food_array:
        current_food.draw_food()
    if FOOD_COOLDOWN <= 0:
        spawn_food()
        FOOD_COOLDOWN = 50
    pygame.display.flip()
    delta_time = clock.tick(144) / 1000
    FOOD_COOLDOWN -= 1
