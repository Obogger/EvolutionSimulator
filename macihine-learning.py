import random, time



generation_stats =[]
def clamp(number): 
    if number <= 0:
        number = 1
    return number
    
    

class Animal:
    def __init__(self, damage, defence, maxHealth, ambush):
        self.damage = damage
        self.defence = defence
        self.maxHealth = maxHealth
        self.ambush = ambush
        self.health = maxHealth
    def stats(self):
        return ("Damage: " + str(self.damage), 
                "Defence: " + str(self.defence), 
                "Max Health: " + str(self.maxHealth), 
                "Ambush: " + str(self.ambush))
        
def simulate_animals(generations,generation_linage,animals_per_generation):
    for linage in range(generation_linage):
        animal_list = [Animal(1,5,10,1) for _ in range(animals_per_generation)]

        current_animal = animal_list[0]

        for current_generation in range(generations):
            for animal in animal_list:
                turn = 1
                is_current_animal_faster = False
                if current_animal.ambush > animal.ambush:
                    is_current_animal_faster = True
                elif current_animal.ambush == animal.ambush:
                    is_current_animal_faster = True if random.randint(0,1) == 1 else False
                if is_current_animal_faster:
                    turn = 0
                while current_animal.health > 0 and animal.health > 0:
                    animal_round_defence = clamp(random.randint(animal.defence - int(animal.defence/10), animal.defence + int(animal.defence/10)))
                    current_animal_round_defence = clamp(random.randint(current_animal.defence - int(current_animal.defence/10), current_animal.defence + int(current_animal.defence/10)))
                    if turn % 2 == 0:
                        animal.health -= clamp(current_animal.damage - animal_round_defence)
                    else:
                        current_animal.health -= clamp(animal.damage - current_animal_round_defence)
                    turn += 1
                if current_animal.health <= 0:
                    current_animal = animal
                current_animal.health = current_animal.maxHealth
                
            animal_list = [Animal(clamp(random.randint(current_animal.damage - 5, current_animal.damage + 5)),
                                clamp(random.randint(current_animal.defence - 5, current_animal.defence + 5)),
                                random.randint(current_animal.maxHealth - 5, current_animal.maxHealth + 5),
                                random.randint(current_animal.ambush - 5, current_animal.ambush + 5)) for _ in range(10)]
            stats = current_animal.stats()
            generation_stats.append(stats)
        
    for linage_stat in range(int(len(generation_stats) / generations)):
        top_linage_stat = ((linage_stat + 1) * generations) - 1
        print(generation_stats[top_linage_stat], top_linage_stat)
    
while True:
    generations = int(input("Generations"))
    generation_linage = int(input("Linages"))
    animals_per_generation = int(input("Animals Per generation"))
    simulate_animals(generations,generation_linage,animals_per_generation)