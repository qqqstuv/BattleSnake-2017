import settings, numpy

# Return all possible moves in one block surrounding area
def handler(id, snakeCoords, food):
	directions = {'0': 'right', '1': 'up', '2': 'left', '3': 'down'}
	settings.resetMap() # reset the map to be 0
	head = None
	otherheads = []
	for snake in snakeCoords:
		coordinates = snake.get('coords')
		for xy in coordinates:
			settings.getMap()[xy[0]][xy[1]] = 1
		if snake.get('id') == id:
			head = snake.get('coords')[0]
		else:
			otherheads.append(snake.get('coords')[0])
	for xy in food:
		settings.getMap()[xy[0]][xy[1]] = 2
	# print settings.getMap()
	print head
	possibleAround(head, directions)
	print directions
	return directions

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
	a = numpy.array(a)
	b = numpy.array(b)
	return numpy.linalg.norm(a-b)

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
	





