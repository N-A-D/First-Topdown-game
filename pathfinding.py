import heap
from settings import GRIDWIDTH, GRIDHEIGHT, TILESIZE, vec


class Graph(object):
    """
    Graph representation of the game's tile map.
    The layout of the game is given by a two dimensional array of "tiles", where each tile is a
    64 x 64 rectangle located by its index in the the array. Each tile in the array is a node in the graph
    and there are edges between nodes iff two nodes are both passable and contained in the graph.
    """

    def __init__(self):
        """
        Creates a new graph.
        """
        self.height = GRIDHEIGHT
        self.width = GRIDWIDTH
        self.walls = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        self.connections += [vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

    def in_bounds(self, node):
        """
        Determines whether or not a given node is contained in the graph by checking to see
        if its coordinates are within the graph's width and height.
        :param node: The node under consideration
        :return: True if the graph contains, False otherwise.
        """
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        """
        Determines if a node is passable or not. Passable here means that
        there does not exist an obstacle at position the node represents.
        :param node: The node under consideration.
        :return: True if the node is not passable, False otherwise.
        """
        return node not in self.walls

    def find_neighbors(self, node):
        """
        Calculates all neighbours of a given node. Since the graph is made using
        a two dimensional array of tiles, each node can have at most 8 neighbours
        which is filtered down if any of those neighbours is impassable or not
        contained in the graph.
        :param node: The node under consideration.
        :return: A list of neighbouring nodes represented as Vector2 objects.
        """
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors


class WeightedGraph(Graph):
    """
    Weighted graph representation.
    Gives weights to the edges among neighbouring nodes.
    """

    def __init__(self):
        """
        Creates a weighted graph.
        """
        super(WeightedGraph, self).__init__()
        self.weights = {}

    def cost(self, start, end):
        """
        Calculates the cost of the edge between two nodes.
        Note: that diagonal edges are more expensive that orthogonal
        edges.
        :param start: A node.
        :param end: Another node.
        :return: An integer representing the cost of the edge.
        """
        if (vec(end) - vec(start)).length_squared() == 1:
            return self.weights.get(end, 0) + 10
        else:
            return self.weights.get(end, 0) + 14


class PriorityQueue:
    """
    Priority Queue implementation.
    Uses a heap for efficiency.
    """

    def __init__(self):
        """
        Creates an empty priority queue
        """
        self.nodes = []

    def put(self, node, cost):
        """
        Inserts a node with a cost to reach that node.
        :param node: The node travelled to.
        :param cost: The cost to travel to that node.
        :return: None
        """
        heap.min_heap_push(heap=self.nodes, item=node, cost=cost)

    def get(self):
        """
        Retrieves the node with the least cost to travel to.
        :return: Tuple containing the coordinates to travel to.
        """
        return heap.min_heap_pop(heap=self.nodes)[1]

    def empty(self):
        """
        Returns whether or not this priority queue is empty.
        :return:
        """
        return len(self.nodes) == 0


class Pathfinder:
    """
    Finds a path from point A to point B
    """

    def __init__(self):
        """
        Creates a new pathfinder.
        """
        self.frontier = PriorityQueue()
        self.path = {}
        self.cost = {}

    def a_star_search(self, graph, start, end):
        """
        A* search implementation.
        :param graph: The graph under consideration.
        :param start: The starting node in the graph
        :param end: The ending node in the graph.
        :return: A list of Vector2 objects indicating the path
                from start to end.
        """

        def heuristic(a, b):
            """
            Manhattan distance heuristic.
            :param a: Initial point
            :param b: Final point
            :return: Integer presenting the manhattan distance from a to b
            """
            return (abs(a.x - b.x) + abs(a.y - b.y)) * 10

        def vector_to_tuple(v):
            """
            Converts a vector into a tuple.
            :param v: The vector to convert
            :return: A tuple of the vector's x and y (x, y)
            """
            return (int(v.x), int(v.y))

        def construct_path(came_from, start, goal):
            """
            Constructs the path by adding onto start, all vectors
            that belong on the path.
            :param came_from: The dictionary of traversed nodes.
            :param start: The initial node.
            :param goal: The final node.
            :return: A list of Vector2 objects representing the path
                    from start to goal.
            """
            current = start
            path = [vec(current.x * TILESIZE, current.y * TILESIZE)]
            while current != goal:
                current = current + came_from[vector_to_tuple(current)]
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
        # Checks to see if there is actually a path from start to end
        # and builds the path if there is.
        if vector_to_tuple(end) in self.path:
            return construct_path(self.path, end, start)
        return None
