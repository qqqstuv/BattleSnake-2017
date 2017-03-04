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

def findHeatMap(head, walls, numSnakes, width, height):
    if numSnakes == 1:
        num = 21
    elif numSnakes == 2:
        num = 21
    elif numSnakes == 3:
        num = 13
    else:
        num = 7

    x_Size = assignStartEnd(head, num, width)
    y_Size = assignStartEnd(head, num, height)
    heatMap = {}
    threatDepthConstant = 3

    for wall in walls:
        xCoff = 1
        yCoff = 1
        if wall[0][0] < x_Size[0] or wall[0][0] > x_Size[1] or wall[0][1] < y_Size[0] or wall[0][1] > y_Size[1]:
            continue
        for x in range(wall[0][0]-threatDepthConstant, wall[0][0] + threatDepthConstant):
            xCoff = xCoff + 1
            if(not(x<x_Size[0] or x>x_Size[1])):
                for y in range(wall[0][1]-threatDepthConstant, wall[0][1] + threatDepthConstant):
                    yCoff = yCoff + 1
                    if(not(y<y_Size[0] or y>y_Size[1])):
                        weight = heatMap.get((x,y), 0)
                        heatMap[(x,y)] = weight + wall[1]/((xCoff**2 + yCoff**2)**(1/2.0))

    return heatMap

def assignStartEnd(head, num, maxDistance):
    end = head[0]+num/2
    start = head[0]-num/2
    full = False #if end and start have to be resized, it sets them to the maxiumums
    if start < 0:#if start is negative
        addon = abs(start) #shaves off the negative
        start = 0 #sets it to the minimum
        end = end + addon #adds to the end of x_end
        full = True #flag
    elif end > maxDistance: #if end is too big
        addon = end - maxDistance #snags the extra bit
        start = start + addon #adds to start
        end = maxDistance #set to maximum
        full = True #flag
    elif full: #sets both to maximums
        start = 0
        end = maxDistance  
    return (start, end)  
