class Fitness:
    def __init__(self, route):
        self.route = route
        self.total_cost = self.calculate_total_cost()

    def calculate_total_cost(self) -> float:
        cost = 0
        for i in range(len(self.route) - 1):
            a = self.route[i]
            b = self.route[i + 1]
            dist = a.distance_to(b)
            cost += dist + b.traffic_weight  # inclui o peso do ponto de destino
        return cost