import settings, a_star

# Return all possible moves in one block surrounding area
def handler(id, snakeCoords, food):
	settings.getMap().walls = [] # reset the map's walls to be 0
	head = None
	otherheads = []
	for snake in snakeCoords:
		coordinates = snake.get('coords')
		for xy in coordinates:
			print settings.getMap().walls
			print ([xy[0],xy[1]], 0)
			settings.getMap().walls.append( ([xy[0],xy[1]], 0) ) # tuple of (coord, weight) default 0
		if snake.get('id') == id:
			head = snake.get('coords')[0]
		else:
			otherheads.append(snake.get('coords')[0])
	for xy in food:
		settings.getMap().food.append( (xy[0],xy[1]) )
	# print settings.getMap()
	print "HEAD: ", head
	# possibleAround(head, directions)

	toFoodObject = findFood(head, food, otherheads) # (d from head to food, xy)
	print "FOOD OBJECT: ", toFoodObject
	movePath = applyAStar(head, toFoodObject[1])
	print "MOVEPATH: ", movePath
	final = directionToPoint(head, movePath[0])
	print "FINAL DECISION: " + final
	return final

def directionToPoint(start, goal):
	if(start[0] == goal[0] + 1):
		return 'right'
	if(start[0] == goal[0] - 1):
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

# Get the best food possible on the map
def getBestFood(head, food, otherheads):
	# Check distance b/w food and other snakes and get the most possible food
	closest = foodObjects[0]
	for index, foodObject in enumerate(foodObjects):
		dToFood = sys.maxint
		for i, aHead in enumerate(otherheads):
			dToFood = min (distance(foodObject[0], aHead), dToFood)
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
	came_from, cost_so_far = a_star.a_star_search(settings.getMap(), head, foodCoord)
	goal = tuple(foodCoord)
	temp = came_from.get(goal)
	movePath = []
	while temp != None:
		movePath.append(temp)
		temp = came_from.get(temp)
	movePath.reverse()
	return movePath




