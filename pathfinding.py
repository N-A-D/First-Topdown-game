import pygame as pg

vec = pg.math.Vector2


class Heap:
    """
    Heap implementation that supports heapification of
    items with custom weights.
    """

    def __init__(self, pairs):
        """
        Creates a heap with the given list of item, value pairs.
        :param pairs: the pairs of items & their values
        """
        self.items = pairs
        self.heapify()

    def pop(self):
        """
        Returns the root of the heap then reheapifies it.
        :return: None
        """
        obj = self.items[0]
        self.items[0] = self.items[len(self.items) - 1]
        x = self.items
        self.items = self.items[0:len(self.items) - 1]
        del x
        self.heapify()
        return obj

    def push(self, pair):
        """
        Pushes an item onto the heap then reheapifies it .
        :param pair: The key-value pair to add
        :return: None
        """
        self.items.append(pair)
        self.heapify()

    def heapify(self):
        """
        Bottom up heapification algorithm
        :return:
        """
        n = len(self.items)
        for idx in range(n // 2, 0, -1):
            key = idx
            value = self.items[key - 1]
            heap = False
            while not heap and (2 * key) <= n:
                child = 2 * key
                if child < n:
                    if self.items[child - 1][1] <= self.items[child][1]:
                        child += 1
                if value[1] >= self.items[child - 1][1]:
                    heap = True
                else:
                    self.items[key - 1] = self.items[child - 1]
                    key = child
            self.items[key - 1] = value

    def heap_print(self):
        """
        Prints the contents of the heap
        :return:
        """
        print(self.items)


class PriorityQueue:
    """
    Priority queue implementation utilizing a heap.
    """

    def __init__(self):
        """
        Creates a priority queue.
        """
        self.items = []
        self.heap = Heap(self.items)

    def insert(self, node, cost):
        """
        Inserts a node along with its cost into the priority queue.
        :param node: The item.
        :param cost: The cost of the item.
        :return:
        """
        self.heap.push((node, cost))

    def retrieve(self):
        """
        Pops an item off the front of the queue.
        :return:
        """
        return self.heap.pop()

    def is_empty(self):
        """
        Checks to see if the queue is empty.
        :return: True if empty, False otherwise
        """
        return len(self.items) == 0


class Graph:
    """
    Graph implementation specific to the game.
    """

    def __init__(self, game, width, height):
        """
        Creates a graph.
        :param game: The containing game
        :param width: How wide the graph will be.
        :param height: How tall the graph will be.
        """
        self.width = width
        self.height = height
        self.wall_positions = game.wall_locations
        self.enemy_positions = game.enemy_locations
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        self.connections += [vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

    def in_bounds(self, node):
        """
        Checks if the node exists within the graph.
        :param node: The node to check
        :return: True if node is within the graph, False otherwise
        """
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        """
        Checks to see if this node is actually a wall.
        :param node: The node to check
        :return: True if node is actually a wall, False otherwise
        """
        return node not in self.wall_positions and node not in self.enemy_positions

    def find_neighbors(self, node):
        """
        Finds all neighbours of the node given all possible connections.
        :param node: The node to check
        :return: The list of neighbours of node
        """
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors


class WeightedGraph(Graph):
    """
    Weighted graph implementation that attached weights to the edges
    between nodes
    """

    def __init__(self, game, width, height):
        """
        Creates a weighted graph.
        """
        super().__init__(game, width, height)
        self.weights = {}

    def cost(self, start, end):
        """
        Returns the cost of the edge between two nodes
        :param start: The start node.
        :param end: The end node.
        :return: An integer representing the cost of the connection
                between start and end
        """
        if (vec(end) - vec(start)).length_squared() == 1:
            return self.weights.get(end, 0) + 10
        else:
            return self.weights.get(end, 0) + 14


class Pathfinder:
    def __init__(self):
        self.frontier = PriorityQueue()
        self.path = {}

    def vector_to_coordinate(self, vector):
        return (int(vector.x), int(vector.y))

    def heuristic(self, A, B):
        return (abs(A.x - B.x) + abs(A.y - B.y)) * 10

    def A_star_search(self, graph, start, end):
        path = {}
        cost = {}
        path[self.vector_to_coordinate(start)] = None
        cost[self.vector_to_coordinate(start)] = 0

        while not self.frontier.is_empty():
            current = self.frontier.retrieve()
            if current == end:
                break
            else:
                for neighbour in graph.find_neighbors(vec(current)):
                    neighbour = self.vector_to_coordinate(neighbour)
                    neighbour_cost = cost[current] + graph.cost(current, end)
                    if neighbour not in cost or neighbour_cost < cost[neighbour]:
                        cost[neighbour] = neighbour_cost
                        priority = neighbour_cost + self.heuristic(end, vec(neighbour))
                        self.frontier.insert(neighbour, priority)
                        path[neighbour] = vec(current) - neighbour
        self.path = path
