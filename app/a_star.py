import collections, heapq, Queue


class SimpleGraph:
    def __init__(self):
        self.edges = {}
    
    def neighbors(self, id):
        return self.edges[id]

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


# graph is a GridWithWeights, a child of SquareGrid
def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    # graph.weights = update(start, graph.walls) # Update based on where the head is

    # possibleMoves = graph.neighbors(id)
    # if possibleMoves.length == 2:
    #     WeightList = []
    #     for possibleMove in possibleMoves:
    #         WeightList.append(bfsGetWeight(graph, possibleMove), possibleMove ) )


    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current # set the parent of the neighbour, which is the current node
    
    return came_from, cost_so_far

def bfsGetWeight(graph, start):
    MAX_INSTANCE = 20
    instance = 0 # number of instances we are going to look
    totalWeight = 0
    q = Queue.Queue()
    visited = set(start)
    while not q.empty() and instance < MAX_INSTANCE:
        grid = q.get()
        instance += 1
        totalWeight += graph.weights.get(grid, 0)
        for node in graph.neighbors(start):
            if node not in visited:
                visited.add(node)
    return totalWeight