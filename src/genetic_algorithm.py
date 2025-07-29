import random
from route import Route
from fitness import Fitness

def generate_random_population(points, size):
    population = []

    for _ in range(size):
        shuffled_points = random.sample(points, len(points))  # Embaralha todos os pontos
        route = Route(shuffled_points)  # Cria uma nova rota com esses pontos
        population.append(route)  # Adiciona a rota à população

    return population

def tournament_selection(population, k=5):
    # Seleciona aleatoriamente k indivíduos da população
    selected = random.sample(population, k)

    # Avalia o custo total de cada rota selecionada
    best_route = selected[0]
    best_cost = Fitness(best_route).total_cost

    for route in selected[1:]:
        current_cost = Fitness(route).total_cost
        if current_cost < best_cost:
            best_route = route
            best_cost = current_cost

    # Retorna a melhor rota entre os k selecionados
    return best_route

def crossover(parent1, parent2):
    start = random.randint(0, len(parent1) - 2)
    end = random.randint(start + 1, len(parent1) - 1)
    child_points = parent1[start:end]
    for p in parent2:
        if p not in child_points:
            child_points.append(p)
    return Route(child_points)

def mutate(route, mutation_rate=0.02):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]