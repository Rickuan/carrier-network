import math

class Node:
    def __init__(self, id: int, name: str, x: int, y: int):
        self.id = id
        self.name = name
        self.x = x
        self.y = y

    def distance_to(self, other: "Node") -> int:
        return int(round(((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5))