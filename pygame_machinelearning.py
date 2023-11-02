
import pygame
import random
import time
import math
import numpy as np
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
        self.maxhealth = 5000
        self.health = self.maxhealth
        self.x = x
        self.y = y
        self.angle = angle
        self.pasty = y
        self.pastx = x
        self.acceleration = [0,0]
        self.currentSpeed = [0,0]
        self.max_speed = 200
        self.hitbox = pygame.Rect(self.x,self.y,50,50)
        self.vision_distance = 500
        self.Brain([[1]],1,1,1)
    def draw_animal(self):
        if len(animal_array) > 100:
            animal_array.pop(0)
        screen.blit(self.img, (self.x, self.y))
        def debug():
            text_font = pygame.font.SysFont(None, 24)
            text = ["HEALTH = " + str(self.health),
                    "ACCEL = " + str(self.acceleration), 
                    "SPEED = " + str(self.currentSpeed)]
            offset = 40
            for lines in text:
                text_img = text_font.render(lines, True, "BLACK")
                screen.blit(text_img, (self.x, self.y-offset))
                offset +=20
            pygame.draw.rect(screen, (255,0,0), self.hitbox,2)
            pygame.draw.circle(screen, (0,0,255), (self.x + self.img.get_width() / 2, self.y + self.img.get_height() / 2), self.vision_distance,2)
        debug()
    class Brain():
        def __init__(self, hnw, hnb, onw, onb):
            hidden_nodes_weights = []
            for _ in hnw:
                hidden_nodes_weights.append([])
                for weight in hnw:
                    hidden_nodes_weights[len(hidden_nodes_weights)-1].append(weight + random.randint(-1,1))
                    
                    
        #0 = AngleToFood in degrees
        input_nodes = [0]
        #0 = Simple Sigmoid Nuron
        #1 = Uncapped sigmoind nuron (input * weight + bias)
        hidden_nodes = [1]
        hidden_nodes_weights = [[1]]
        hidden_nodes_bias = [[5]]
        #0 = Direction
        output_nodes = [0]
        output_nodes_weights = [[1.5]]
        output_nodes_bias = [[5]]
        
        def think(self):
            input_pass = 0
            current_hidden_node_output = [0 for _ in range(100)]
            for input_type in self.input_nodes:
                current_node = 0
                match input_type:
                    case 0:
                        current_input = angle_to_food_degrees()
                for nuron_type in self.hidden_nodes:
                    match nuron_type:
                        case 1:
                            current_hidden_node_output[current_node] = uncapped_simple_nuron(current_input, self.output_nodes_weights[current_node][input_pass], self.hidden_nodes_bias[current_node][input_pass])  
                    current_node += 1
                input_pass += 1
    
            for output_type in self.output_nodes:
                output_pass = 0
                total_value = 0
                for hidden_node_pass in range(len(self.hidden_nodes)):
                    total_value += uncapped_simple_nuron(current_hidden_node_output[hidden_node_pass], self.output_nodes_weights[output_pass][hidden_node_pass], self.output_nodes_bias[output_pass][hidden_node_pass])
                match output_type:
                    case 0:
                        direction_output(total_value)
                output_pass += 1
class Food():
    def __init__(self,x,y):
        raw_image = pygame.image.load("food.png")
        self.img = pygame.transform.scale(raw_image, (50,50))
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x,self.y,50,50)
    def draw_food(self):
        if len(food_array) > 5:
            food_array.pop()
        screen.blit(self.img, (self.x, self.y))

def angle_to_food_degrees():
    new_angle = math.degrees(np.arctan2((current_animal.x -food_array[0].x), (current_animal.y -food_array[0].y))) + 180
    return new_angle
def uncapped_simple_nuron(input, weight, bias):
    print(input, weight, bias)
    output = input * weight + bias
    return output
def direction_output(angle):
            try: 
                new_acceleration = calcualte_vector_from_angle(angle, current_animal.max_speed)
                new_acceleration = speed_loss(current_animal.currentSpeed, current_animal.max_speed, new_acceleration)
                current_animal.acceleration = new_acceleration
            except:
                pass

def animal_move(current_animal):
    current_animal.pastx = current_animal.x
    current_animal.pasty = current_animal.y
    current_animal.currentSpeed[0] += current_animal.acceleration[0] / 10
    current_animal.currentSpeed[1] += current_animal.acceleration[1] / 10
    current_animal.x += current_animal.currentSpeed[0] * delta_time
    current_animal.y += current_animal.currentSpeed[1] * delta_time
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
            current_animal.pastx = current_animal.x 
            current_animal.pasty = current_animal.y
            current_animal.acceleration = [0, 0]
            current_animal.hitbox = pygame.Rect(current_animal.x, current_animal.y, current_animal.hitbox[2],current_animal.hitbox[3])
            #animal.x += (current_animal.movement_deltaX * delta_time) * 5
            #animal.y += (current_animal.movement_deltaX * delta_time) * 5
            #animal.hitbox = pygame.Rect(animal.x, animal.y, animal.hitbox[2],animal.hitbox[3])
    for food in food_array:
        if current_animal.hitbox.colliderect(food.hitbox):
            food_array.remove(food)
            current_animal.health = current_animal.maxhealth
            new_animal = Animal(current_animal.x-60, current_animal.y, random.randint(0,360))
            #animal_array.append(new_animal)
            for animal in animal_array:
                if new_animal.hitbox.colliderect(animal.hitbox) and new_animal != animal:
                    animal.y -= 70
def spawn_animal():
    open = True
    animal = Animal(random.randint(500,500), 500,random.randint(0,360))
    for current_animal in animal_array:
        if animal.hitbox.colliderect(current_animal.hitbox):
            open = False
    if open:
        animal_array.append(animal)
def spawn_food():
    food = Food(random.randint(0,SCREEN_WIDTH -50), random.randint(0,SCREEN_HEIGHT- 50))
    food_array.append(food)

def speed_loss(current_speed_vector, max_speed, acceleration):
    current_speed_tangent = math.sqrt(math.pow(current_speed_vector[0],2) + math.pow(current_speed_vector[1],2))
    print(current_speed_tangent)
    friction = current_speed_tangent / max_speed
    acceleration = [acceleration[0] - (friction * current_speed_vector[0]), acceleration[1] - (friction * current_speed_vector[1])]
    return acceleration

def calcualte_vector_from_angle(angle, max_speed):
    x = math.sin(math.radians(angle)) * max_speed
    y = math.cos(math.radians(angle)) * max_speed
    vector = [x,y]
    return vector
    
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
        current_animal.brain.think()
        animal_move(current_animal)
        current_animal.health -= 1
        if current_animal.health <= 0:
            animal_array.remove(current_animal)
        current_animal.draw_animal()
    for current_food in food_array:
        current_food.draw_food()
    if FOOD_COOLDOWN <= 0:
        spawn_food()
        FOOD_COOLDOWN = 50
    pygame.display.flip()
    delta_time = clock.tick(144) / 1000
    FOOD_COOLDOWN -= 1
