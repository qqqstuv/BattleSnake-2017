import settings, a_star, math, sys, dijkstra, operator

# Return all possible moves in one block surrounding area
def handler(id, snakeCoords, food):
	graph = settings.getMap()
	graph.walls = [] # reset the map's walls to be 0
	graph.weights = {}
	head = None # [x,y]
	foodLevel = 0
	ourSnakeLength = 0
	otherheads = []
	otherSnakeLengths = []
	otherheadsAndHealth = []
	otherheadsAndDuration = []
	for snake in snakeCoords:
		coordinates = snake.get('coords')
		length = len(coordinates)
		for index, xy in enumerate(coordinates):
			# print graph.walls
			# print ([xy[0],xy[1]], 0)
			graph.walls.append(makeWall(xy, index, length)) # tuple of (coord, duration) default 0
		if snake.get('id') == id: # Our snake
			head = snake.get('coords')[0]
			foodLevel = snake.get('health_points')
			ourSnakeLength = length
		else:
			otherheadsAndDuration.append(makeWall(snake.get('coords')[0], 0,length)) # tuple of (coord, duration) default 0
			otherSnakeLengths.append(length)
			otherheadsAndHealth.append((snake.get('coords')[0], snake.get('health_points')))

	for xy in food:
		graph.food.append( (xy[0],xy[1]) )
	#Sort snakehead list based on health
	otherheadsAndHealth.sort(key=lambda headAndHealth: headAndHealth[1])
	otherheads = [headAndHealth[0] for headAndHealth in otherheadsAndHealth]

	FOOD_SEARCH_THRESHOLD = max(50, 95 - ourSnakeLength * 1) # the longer the less food threshold
	final = ""

	# MOVE LOGIC
	if len(otherSnakeLengths) > 2: # if there are more than 2 other snakes
		if ourSnakeLength > second_largest(otherSnakeLengths): # if our length is ok
			final = killSnakeMove(head, otherheadsAndDuration, otherheads, graph)
		else: # eat more
			final = getFoodMove(head, otherheadsAndDuration, food, otherheads, graph)
	else: # there are 2 other snakes or less
		if foodLevel < FOOD_SEARCH_THRESHOLD: # if we are hungry
			final = getFoodMove(head, otherheadsAndDuration, food, otherheads, graph)
		else: # kill snakes
			final = killSnakeMove(head, otherheadsAndDuration, otherheads, graph)
	return final

# Find a snake and try to corner it
def killSnakeMove(head, otherheadsAndDuration, otherheads, graph):
	move = None
	move = findEnemy(head, otherheadsAndDuration, otherheads, graph)
	if move == None: # Could not find a snake to go to, then get Safest Move
		updateHeatMap(head, otherheadsAndDuration, graph, otherheads)
		move = a_star.bfsGetSafeMove(head, graph)
		print ("SAFE MOVE")
	else:
		print ("KILL MOVE")
	return directionToPoint(head, move)

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def updateHeatMap(head, otherheadsAndDuration, graph, otherheads):
	graph.weights = merge_two_dicts( graph.weights, a_star.findHeatMap(head, otherheadsAndDuration, graph.walls, graph.width, graph.height)) 


def findEnemy(head, otherheadsAndDuration, otherheads, graph):
	for aHead in otherheads: # loop through every snakes, snakes are sorted base on health
		visited = [] # visited nodes 
		updateHeatMap(aHead, otherheadsAndDuration, graph, otherheads)
		# add possible route through customized bfs on the head
		came_from, cost_so_far = dijkstra.dijkstra_search(graph, tuple(aHead))
		for key in sorted(cost_so_far.iterkeys()): # loop through lowest to highest key
			if a_star.heuristic(key, head) < a_star.heuristic(key, aHead):
				return key # return the (x,y) we should go for
	return None
	# if everything null do bfs on own snake

def getFoodMove(head, otherheadsAndDuration, food, otherheads, graph):
	toFoodObject = findFood(head, food, otherheads) # (d from head to food, xy)
	updateHeatMap(head, otherheadsAndDuration, graph, otherheads)
	movePath = applyAStar(head, toFoodObject[1])
	final = directionToPoint(head, movePath[1])
	# print("FOOD ORIENTED - FOOD OBJECT: %s MOVEPATH: %s FINAL STRING DECISION: %s" % (toFoodObject, movePath[1],final))
	return final # index 1 is because 0 is our goal

def applyAStar(head, foodCoord):
	tupleHead = tuple(head)
	tupleFood = tuple(foodCoord)
	movePath =  a_star.a_star_search(settings.getMap(), tupleHead, tupleFood)
	return movePath

def makeWall(xy, index, length):
	return ((xy[0],xy[1]), length - index)

def directionToPoint(start, goal):
	neighbors = settings.getMap().neighbors(start)
	for index in neighbors:
		if goal == index:
			if(start[0] == goal[0] - 1):
				return 'right'
			if(start[0] == goal[0] + 1):
				return 'left'
			if(start[1] == goal[1] + 1):
				return 'up'
			if(start[1] == goal[1] - 1):
				return 'down'
	return neighbors[0]

# Check four possible moves of the head
def possibleAround(head, directions):
	if settings.isCollided([head[0] + 1, head[1]]):
		del directions['0']
	if settings.isCollided([head[0], head[1] + 1]):
		del directions['3']
	if settings.isCollided([head[0] - 1, head[1]]):
		del directions['2']
	if settings.isCollided([head[0], head[1] - 1]):
		del directions['1']

# Calculate distance between 2 points
def distance(a,b):
	return math.hypot(a[0] - b[0], a[1] - b[1])

# Get the best food possible on the map, foodObjects: list of (distance bw head, [x,y])
def getBestFood(head, foodObjects, otherheads):
	# Check distance b/w food and other snakes and get the most possible food
	closest = foodObjects[0]
	for index, foodObject in enumerate(foodObjects):
		dToFood = sys.maxint
		for i, aHead in enumerate(otherheads):
			dToFood = min (distance(foodObject[1], aHead), dToFood)
		if dToFood > foodObject[0]:
			closest = foodObject
			return closest
	return closest

def findFood(head, food, otherheads):
	# Find closest food
	foodObjects = []
	for xy in food:
		foodObjects.append((distance(xy, head), xy))
	foodObjects.sort(key=lambda tup: tup[0])
	bestFoodObject = getBestFood(head, foodObjects, otherheads)
	return bestFoodObject

def second_largest(numbers):
    count = 0
    m1 = m2 = float('-inf')
    for x in numbers:
        count += 1
        if x > m2:
            if x >= m1:
                m1, m2 = x, m1            
            else:
                m2 = x
    return m2 if count >= 2 else None