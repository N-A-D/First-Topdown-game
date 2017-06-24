import heap
import pygame as pg
from settings import GRIDWIDTH, GRIDHEIGHT, TILESIZE

vec = pg.math.Vector2


class SquareGrid:
    def __init__(self):
        self.height = GRIDHEIGHT
        self.width = GRIDWIDTH
        self.walls = []
        self.enemies = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        self.connections += [vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls and node not in self.enemies

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors


class WeightedGrid(SquareGrid):
    def __init__(self):
        super().__init__()
        self.weights = {}

    def cost(self, start, end):
        if (vec(end) - vec(start)).length_squared() == 1:
            return self.weights.get(end, 0) + 10
        else:
            return self.weights.get(end, 0) + 14


class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heap.min_heap_push(heap=self.nodes, item=node, cost=cost)

    def get(self):
        return heap.min_heap_pop(heap=self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0


class Pathfinder:
    def __init__(self):
        self.frontier = PriorityQueue()
        self.path = {}
        self.cost = {}

    def a_star_search(self, graph, start, end):
        def heuristic(a, b):
            return (abs(a.x - b.x) + abs(a.y - b.y)) * 10

        def vector_to_tuple(v):
            return (int(v.x), int(v.y))

        def construct_path(came_from, start, goal):
            current = start
            path = [vec(current.x * TILESIZE, current.y * TILESIZE)]
            while current != goal:
                next = came_from[(current.x, current.y)]
                current = current + next
                path.append(vec(current.x * TILESIZE, current.y * TILESIZE))
            return path

        self.frontier = PriorityQueue()
        self.frontier.put(vector_to_tuple(start), 0)
        self.path = {}
        self.cost = {}
        self.path[vector_to_tuple(start)] = None
        self.cost[vector_to_tuple(start)] = 0
        goal = vector_to_tuple(end)

        while not self.frontier.empty():
            current = self.frontier.get()
            if current == goal:
                break
            for next in graph.find_neighbors(vec(current)):
                next = vector_to_tuple(next)
                next_cost = self.cost[current] + graph.cost(current, next)
                if next not in self.cost or next_cost < self.cost[next]:
                    self.cost[next] = next_cost
                    priority = next_cost + heuristic(end, vec(next))
                    self.frontier.put(next, priority)
                    self.path[next] = vec(current) - vec(next)
        return construct_path(self.path, end, start)
