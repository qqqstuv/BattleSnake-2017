import settings, a_star, math, sys

# Return all possible moves in one block surrounding area
def handler(id, snakeCoords, food):
	graph = settings.getMap()
	graph.walls = [] # reset the map's walls to be 0
	graph.weights = {}
	head = None # [x,y]
	foodLevel = 0
	otherheads = []
	ourSnakeLength = 0
	otherSnakeLengths = []
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
			otherSnakeLengths.append(length)
			otherheads.append(snake.get('coords')[0])
	for xy in food:
		graph.food.append( (xy[0],xy[1]) )
	# print graph
	print "HEAD: ", head
	FOOD_SEARCH_THRESHOLD = max(50, 90 - ourSnakeLength * 1) # the longer the less food threshold
	final = ""

	# MOVE LOGIC
	if len(otherSnakeLengths) > 2: # if there are more than 2 other snakes
		if ourSnakeLength > second_largest(otherSnakeLengths): # if our length is ok
			final = killSnakeMove(head, otherheads, graph)
		else: # eat more
			final = getFoodMove(head, food, otherheads)
	if foodLevel < FOOD_SEARCH_THRESHOLD: # if we are hungy
		final = getFoodMove(head, food, otherheads)
	else: # kill snakes
		final = killSnakeMove(head, otherheads, graph)
	return final

def killSnakeMove(head, otherheads, graph):
	move = findEnemy(head, otherheads, graph)
	if move == None: # Could not find a snake to go to, then get Safest Move
		graph.weights = a_star.findHeatMap(head, graph.walls, graph.width, graph.height)
		move = a_star.bfsGetSafeMove(head, graph)
		print ("SAFE MOVE")
	else:
		print ("KILL MOVE")
	return directionToPoint(head, move)

def getFoodMove(head, food, otherheads):
	toFoodObject = findFood(head, food, otherheads) # (d from head to food, xy)
	movePath = applyAStar(head, toFoodObject[1])
	print("FOOD ORIENTED - FOOD OBJECT: %s MOVEPATH: %s FINAL STRING DECISION: %s" % (toFoodObject, movePath[1],final))
	return directionToPoint(head, movePath[1]) # index 1 is because 0 is our goal


def makeWall(xy, index, length):
	return ((xy[0],xy[1]), length - index)

def directionToPoint(start, goal):
	if(start[0] == goal[0] - 1):
		return 'right'
	if(start[0] == goal[0] + 1):
		return 'left'
	if(start[1] == goal[1] + 1):
		return 'up'
	if(start[1] == goal[1] - 1):
		return 'down'

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

def applyAStar(head, foodCoord):
	tupleHead = tuple(head)
	tupleFood = tuple(foodCoord)
	movePath =  a_star.a_star_search(settings.getMap(), tupleHead, tupleFood)
	return movePath

def findEnemy(head, otherheads, graph):
	for aHead in otherheads: # loop through every snakes
		neighbors = []
		isPotential = False
		for neighbor in graph.neighbors(aHead): # get possible Moves
			if a_star.bfsGetPossibleMove(graph, neighbor):
				isPotential = True
			else:
				neighbors.append(graph.neighbors(neighbor))
		if isPotential == True:
			# for neighbor in neighbors:
			# 	a_star.findHeatMap(neighbor, graph.walls, graph.width, graph.height) # This is not efficient. SHould CHange this
			return neighbors[0] # return the (x,y) we should go for
	return None
	# if everything null do bfs on own snake

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