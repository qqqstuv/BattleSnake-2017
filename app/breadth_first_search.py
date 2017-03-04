import a_star

# example_graph = SimpleGraph()
# example_graph.edges = {
#     'A': ['B'],
#     'B': ['A', 'C', 'D'],
#     'C': ['A'],
#     'D': ['E', 'A'],
#     'E': ['B']
# }   

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
    
    # Is the snake in bound?
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    # Are there obstacles on the way
    def passable(self, id):
        return id not in self.walls
    
    # Get the neighbors of the grid
    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()
        
# This is version number 3
# Get all the surrounding nodes from start; stop when hit goal
def breadth_first_search(graph, start, goal):
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal: #if see the goal then stop to run Dijkstra
            break
        
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next) # put in the list we gonna look at next
                came_from[next] = current # this is the path
    
    return came_from

# g = SquareGrid(30, 15)
# g.walls = DIAGRAM1_WALLS

# parents = breadth_first_search_3(g, (8, 7), (17, 2))
# draw_grid(g, width=2, point_to=parents, start=(8, 7), goal=(17, 2))