import collections, heapq, Queue, math


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
    # print "DEBUG GRAPH WEIGHTS:", graph.weights
    # print "GRAPH WALLS", graph.walls
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
    
    # Get the movePath list
    temp = came_from.get(goal)
    movePath = []
    while temp != None:
        movePath.append(temp)
        temp = came_from.get(temp)
    movePath.reverse()
    movePath.append(goal) # add it so that the snake doesn't get confused at the last one it eats

    # print "DEBUG MOVEPATH", movePath
    if len(movePath) == 1: # if there is no possible move generated from AStar
        move = bfsGetSafeMove(start, graph)
        movePath.append(move[0])
        print ("SAFE MOVE")
    else:
        print ("FOOD MOVE")
    return movePath


# return (x,y) with min bfs value
def bfsGetSafeMove(start, graph):
    possibleMoves = graph.neighbors(start)
    WeightList = []
    for possibleMove in possibleMoves:
        WeightList.append((bfsGetWeight(graph, possibleMove), possibleMove))
    move = min(WeightList, key = lambda t: t[1])
    return move[1]

def bfsGetWeight(graph, start):
    MAX_INSTANCE = 40
    instance = 0 # number of instances we are going to look
    totalWeight = 0
    q = Queue.Queue()
    visited = set(start)
    while not q.empty() and instance < MAX_INSTANCE:
        grid = q.get()
        instance += 1
        totalWeight += graph.weights.get(grid, 0)
        for node in graph.neighbors(grid):
            if node not in visited:
                visited.add(node)
                q.put(node)
    return totalWeight


# Pass in the next move, return if there is a guaranteed dead end after MAX_INSTANCE bfs entries
def bfsGetPossibleMove(graph, head):
    MAX_INSTANCE = 40
    visitedInstance = 0 # number of instances we are going to look
    q = Queue.Queue()
    visited = set(head)
    while not q.empty() and visitedInstance < MAX_INSTANCE:
        grid = q.get() # pop the top thing
        for neighbour in graph.neighbors(grid): # get the neighbors
            if neighbour not in visited:
                visited.add(neighbour)
                q.put(neighbour)
            else:
                for possibleWall in grap.neighbors(neighbour):
                    possibleWallObject = graph.weights.get(possibleWall, 0) # get possible wall
                    if possibleWallObject != 0: # if we found a wall
                        distanceFromStart = heuristic(possibleWall, head) # get # of moves to get to neighbour 
                        if possibleWallObject[1] < distanceFromStart: # if by the time get there the wall is gone
                            visited.add(possibleWall)
                            q.put(possibleWall)
        visitedInstance += 1
    if visitedInstance < MAX_INSTANCE:
        return False
    return True

# Do heatMap in enemy's head and see if they have down side
def bfsEnemy(graph, head):
    pass


# walls is [((x,y), weight)]
def findHeatMap(head, headList, walls, width, height):
    # print ("OTHER heads and duration", headList)
    # print ("GRAPH walls ", walls)
    num = 27 #has to be odd
    threatDepthConstant = 5 #has to be odd divided by 2
    borderWeight = 3 #borderWeight
    beta = 4 # standard coefficient for border
    theta = 1.5 # coefficient for duration
    defaultHeadWeight = theta*15 #snakeHeadWeight multiplier
    alpha = None

    for i in headList:
        try:
            walls.remove(i)
            walls.append((i[0],i[1]+defaultHeadWeight))
        except Exception, e:
            walls.append((i[0],i[1]+defaultHeadWeight))
            print ("DEBUG", i)
    walls = addBorders(walls, width, height, borderWeight) #adds the borders to the list of walls
    x_Size = assignStartEnd(head, num, width)
    y_Size = assignStartEnd(head, num, height)
    heatMap = {}
    for wall in walls:
        points = pointsAroundCoord(wall, threatDepthConstant, x_Size, y_Size) #returns a list of points of the form ((x,y),weight)
        for point in points:
            if heatMap.has_key(point):
                heatMap[point] = heatMap[point] + points[point]
            else:
                heatMap[point] = points[point]
        

    for wall in walls:
        if heatMap.has_key(wall[0]):
            del heatMap[wall[0]]
    return heatMap
    
def pointsAroundCoord(wall, num, x_Size, y_Size):
    points = {}
    point = wall[0]
    startLeft = point[0] - num/2
    endLeft = point[0] + num/2
    startTop = point[1] - num/2
    endTop = point[1] + num/2
    for i in range(startLeft, endLeft+1):
        for j in range(startTop, endTop+1):
            if(i< x_Size[0] or j< y_Size[0] or (i==point[0] and j == point[1])):
                continue
            if( i> x_Size[1] or j > y_Size[1]):
                continue
            divisor = 2*math.sqrt(((abs(point[0])-abs(i))**2) + ((abs(point[1]) - abs(j))**2))
            if(divisor == 0):
                divisor = 1
            if points.has_key((i,j)):
                points[(i,j)] = points[(i,j)] + wall[1]/divisor
            else:
                points[(i,j)] = wall[1]/divisor
    return points
    
def addBorders(walls, width, height, borderWeight):
    for i in range(-1, width+1): #x = -1 to max, y = max
        walls.append(((i,-1),borderWeight))
    for j in range(-1, width+1):  #x = -1 to max, y = -1
        walls.append(((j,height),borderWeight))
    for k in range(0, height): #y = 0 to height-1, since x got it, and x = -1
        walls.append(((-1, k), borderWeight))
    for l in range(0, height):
        walls.append(((width,l), borderWeight)) #y = 0 to height-1, and x = width
    
    return walls

def assignStartEnd(head, num, maxDistance):
    end = head[0]+num/2
    start = head[0]-num/2
    full = False #if end and start have to be resized, it sets them to the maximums
    if start < 0:#if start is negative
        addon = abs(start) #shaves off the negative
        start = 0 #sets it to the minimum
        end = end + addon #adds to the end of x_end
        full = True #flag
    if end > maxDistance: #if end is too big
        addon = end - maxDistance #snags the extra bit
        start = start + addon #adds to start
        end = maxDistance #set to maximum
    else:
        full = False
        
    if full: #sets both to maximums
        start = 0
        end = maxDistance
    return (start, end)