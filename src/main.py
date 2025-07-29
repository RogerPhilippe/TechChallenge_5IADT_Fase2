import pygame
from delivery_point import DeliveryPoint
from genetic_algorithm import *
from fitness import Fitness


# Inicializa pontos de entrega
# Cria o ponto de partida (depot)
depot = DeliveryPoint("Depot", 0, 0)

# Constantes de escala para normalização
SCALE_X = 80
SCALE_Y = 50
OFFSET_X = 50
WINDOW_HEIGHT = 600

def get_delivery_points():
    # Cria uma lista vazia para os pontos de entrega
    delivery_points = []
    used_coords = set()
    used_coords.add((0, 0))  # Garante que ninguém use a coordenada do depot

    # Adiciona 20 pontos de entrega com nomes P1 até P20
    for i in range(1, 21):
        while True:
            x = round(random.uniform(0, 10), 4)
            y = round(random.uniform(0, 10), 4)
            if (x, y) not in used_coords:
                used_coords.add((x, y))
                break
        name = f"P{i}"
        point = DeliveryPoint(name, x, y)
        delivery_points.append(point)

    # Junta o depot com os pontos criados
    return delivery_points

points = [depot] + get_delivery_points()

# Print generated delivery points
for p in points:
    print(f'name: {p.name} traffic_weight: {p.traffic_weight:.3f}')

# Parâmetros genéticos
population = generate_random_population(points, 100)
generations = 200
history = []

# Inicia Pygame
pygame.init()
screen = pygame.display.set_mode((1100, 760))
pygame.display.set_caption("SmartDelivery V2")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

def normalize(pontos):
    """
    Normaliza os pontos de entrega para as coordenadas da tela.
    Cada ponto é convertido de sua escala original (por exemplo, 0-10)
    para a escala de pixels da janela do Pygame.
    """
    normalized_points = []
    for p in pontos:
        # Converte as coordenadas do ponto para a escala da tela usando constantes
        x = int(p.x * SCALE_X + OFFSET_X)
        y = int(WINDOW_HEIGHT - p.y * SCALE_Y)
        normalized_points.append((x, y))
    return normalized_points

# Ordena a população pelo custo total da rota (menor custo primeiro)
def get_total_cost(route):
    return Fitness(route).total_cost

for gen in range(generations):
    for r in population:
        if r[0].name != "Depot":
            r.insert(0, depot)

    population.sort(key=get_total_cost) # aqui passamos a função get_total_cost como referência para sort
    best_route = population[0]
    best_time = Fitness(best_route).total_cost
    history.append(best_time)
    if best_time >= 60:
        hours = int(best_time // 60)
        minutes = int(best_time % 60)
        print(f"Geração {gen + 1}: {hours}h {minutes}min")
    else:
        print(f"Geração {gen + 1}: {best_time:.2f} minutos")

    # Começa a nova geração com a melhor rota atual, isso garante que a melhor solução não seja perdida. (elitismo)
    # Gera novos filhos (rotas)
    new_population = [best_route]
    while len(new_population) < len(population):
        p1 = tournament_selection(population)
        p2 = tournament_selection(population)
        child = crossover(p1, p2)
        mutate(child)
        new_population.append(child)
    population = new_population

    # Pygame desenho
    screen.fill((255, 255, 255))
    norm = normalize(best_route)

    # Gráfico de evolução com eixo e valores (abaixo da área da rota)
    if len(history) > 1:
        max_time = max(history)
        min_time = min(history)
        graph_x = 50
        graph_y = 650
        graph_width = 1000
        graph_height = 60

        # Fundo do gráfico com borda
        pygame.draw.rect(screen, (240, 240, 240), (graph_x - 10, graph_y - 10, graph_width + 20, graph_height + 20))
        pygame.draw.rect(screen, (0, 0, 0), (graph_x - 10, graph_y - 10, graph_width + 20, graph_height + 20), 1)

        # Eixo Y
        pygame.draw.line(screen, (0, 0, 0), (graph_x, graph_y), (graph_x, graph_y + graph_height), 1)

        def format_time_label(t):
            return f"{int(t // 60)}h{int(t % 60)}m" if t >= 60 else f"{t:.1f}"

        label_max = font.render(format_time_label(max_time), True, (0, 0, 0))
        label_min = font.render(format_time_label(min_time), True, (0, 0, 0))
        screen.blit(label_max, (graph_x + 5, graph_y - 10))
        screen.blit(label_min, (graph_x + 5, graph_y + graph_height - 10))

        for i in range(1, len(history)):
            x1 = graph_x + (i - 1) * (graph_width // max(len(history), 2))
            x2 = graph_x + i * (graph_width // max(len(history), 2))
            y1 = int(graph_y + graph_height - (graph_height * (history[i - 1] - min_time) / (max_time - min_time + 1e-5)))
            y2 = int(graph_y + graph_height - (graph_height * (history[i] - min_time) / (max_time - min_time + 1e-5)))
            if x2 < graph_x + graph_width:
                pygame.draw.line(screen, (200, 50, 50), (x1, y1), (x2, y2), 2)

    # Linhas
    for i in range(len(norm) - 1):
        pygame.draw.line(screen, (0, 150, 200), norm[i], norm[i + 1], 2)

    # Pontos
    for i, p in enumerate(best_route):
        pos = norm[i]
        pygame.draw.circle(screen, (0, 0, 255), pos, 6)
        label = font.render(p.name, True, (0, 0, 0))
        screen.blit(label, (pos[0] + 5, pos[1] - 5))

    # Texto topo
    if best_time >= 60:
        hours = int(best_time // 60)
        minutes = int(best_time % 60)
        time_label = f"{hours}h {minutes}min"
    else:
        time_label = f"{best_time:.2f} min"
    title = font.render(f"Geração {gen+1}/{generations} - Tempo total: {time_label}", True, (0, 0, 0))
    screen.blit(title, (10, 10))

    pygame.display.flip()
    clock.tick(60)
    pygame.time.wait(150)

# Resultado final
print("\nMelhor rota encontrada:")
route_str = " -> ".join(p.name for p in best_route)
print(route_str)

if best_time >= 60:
    hours = int(best_time // 60)
    minutes = int(best_time % 60)
    print(f"Tempo total: {hours}h {minutes}min")
else:
    print(f"Tempo total: {best_time:.2f} minutos")

print("\nTempos entre pontos:")
for i in range(len(best_route) - 1):
    a = best_route[i]
    b = best_route[i + 1]
    dist = a.distance_to(b)
    print(f"{a.name} ➜ {b.name} = {dist:.2f} min")

# Espera ESC ou fechar janela
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            running = False

pygame.quit()