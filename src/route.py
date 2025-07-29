class Route(list):
    def __repr__(self):
        return " -> ".join(p.name for p in self)