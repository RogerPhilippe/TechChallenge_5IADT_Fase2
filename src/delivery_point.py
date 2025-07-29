import random

class DeliveryPoint:
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y
        self.traffic_weight = random.uniform(1.0, 3.0)  # Simula tráfego pesado (1 a 3 minutos extras)

    def distance_to(self, other) -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx ** 2 + dy ** 2) ** 0.5

    def __repr__(self):
        return f"{self.name}({self.x:.2f}, {self.y:.2f}, w={self.traffic_weight:.1f})"