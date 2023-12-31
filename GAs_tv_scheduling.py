import random

##################################### DEFINING PARAMETERS AND DATASET ################################################################
# Sample rating programs dataset for each time slot.
ratings = {
    'news': [0.1, 0.1, 0.4, 0.3, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.5, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2],
    'live_soccer': [0.0, 0.0, 0.0, 0.2, 0.1, 0.3, 0.2, 0.1, 0.4, 0.3, 0.4, 0.5, 0.4, 0.6, 0.4, 0.3, 0.4, 0.3],
    'movie_a': [0.1, 0.1, 0.2, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.4, 0.3, 0.5, 0.3, 0.4],
    'movie_b': [0.2, 0.1, 0.1, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.4, 0.5, 0.4, 0.3, 0.4, 0.5],
    'reality_show': [0.3, 0.4, 0.3, 0.4, 0.4, 0.5, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.2, 0.2, 0.3],
    'tv_series_a': [0.2, 0.3, 0.2, 0.1, 0.1, 0.2, 0.2, 0.4, 0.4, 0.3, 0.3, 0.3, 0.5, 0.6, 0.4, 0.5, 0.4, 0.3],
    'tv_series_b': [0.1, 0.2, 0.3, 0.3, 0.2, 0.3, 0.3, 0.1, 0.4, 0.3, 0.4, 0.3, 0.5, 0.3, 0.4, 0.6, 0.4, 0.3],
    'music_program': [0.3, 0.3, 0.3, 0.2, 0.2, 0.1, 0.2, 0.4, 0.3, 0.3, 0.3, 0.3, 0.2, 0.3, 0.2, 0.3, 0.5, 0.3],
    'documentary': [0.3, 0.3, 0.4, 0.3, 0.2, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.2, 0.2, 0.1, 0.1, 0.3, 0.3, 0.2],
    'Boxing': [0.4, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.3, 0.3, 0.3, 0.2, 0.3, 0.4, 0.3, 0.4, 0.6]
}

GEN = 100
POP = 50
CO_R = 0.8
MUT_R = 0.2
EL_S = 2

all_programs = list(ratings.keys()) # all programs
all_time_slots = list(range(6, 24)) # time slots

######################################### DEFINING FUNCTIONS ########################################################################
# defining fitness function
def fitness_function(schedule):
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        total_rating += ratings[program][time_slot]
    return total_rating

# initializing the population
def initialize_pop(programs, time_slots):
    if not programs:
        return [[]]

    all_schedules = []
    for i in range(len(programs)):
        for schedule in initialize_pop(programs[:i] + programs[i + 1:], time_slots):
            all_schedules.append([programs[i]] + schedule)

    return all_schedules

# selection
def finding_best_schedule(all_schedules):
    best_schedule = []
    max_ratings = 0

    for schedule in all_schedules:
        total_ratings = fitness_function(schedule)
        if total_ratings > max_ratings:
            max_ratings = total_ratings
            best_schedule = schedule

    return best_schedule

# calling the pop func.
all_possible_schedules = initialize_pop(all_programs, all_time_slots)

# callin the schedule func.
best_schedule = finding_best_schedule(all_possible_schedules)


############################################# GENETIC ALGORITHM #############################################################################

# Crossover 
def crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 2)
    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return child1, child2

# mutating
def mutate(schedule):
    mutation_point = random.randint(0, len(schedule) - 1)
    new_program = random.choice(all_programs)
    schedule[mutation_point] = new_program
    return schedule

# calling the fitness func.
def evaluate_fitness(schedule):
    return fitness_function(schedule)

# genetic algorithms with parameters



def genetic_algorithm(initial_schedule, generations=GEN, population_size=POP, crossover_rate=CO_R, mutation_rate=MUT_R, elitism_size=EL_S):
    
    population = [initial_schedule]

    for _ in range(population_size - 1):
        random_schedule = initial_schedule.copy()
        random.shuffle(random_schedule)
        population.append(random_schedule)

    for generation in range(generations):
        new_population = []

        # Elitsm
        population.sort(key=lambda schedule: fitness_function(schedule), reverse=True)
        new_population.extend(population[:elitism_size])

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = new_population

    return population[0]
  
##################################################### RESULTS ###################################################################################

# brute force
initial_best_schedule = finding_best_schedule(all_possible_schedules)

rem_t_slots = len(all_time_slots) - len(initial_best_schedule)
genetic_schedule = genetic_algorithm(initial_best_schedule, generations=GEN, population_size=POP, elitism_size=EL_S)

final_schedule = initial_best_schedule + genetic_schedule[:rem_t_slots]

print("\nFinal Optimal Schedule:")
for time_slot, program in enumerate(final_schedule):
    print(f"{all_time_slots[time_slot]:02d}:00 - Program {program}")

print("Total Ratings:", fitness_function(final_schedule))
