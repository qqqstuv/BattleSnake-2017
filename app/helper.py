import settings




# return all possible moves in one block surrounding area
def possibleMove(id, snakeCoords):
	directions = {'0': 'right', '1': 'up', '2': 'left', '3': 'down'}
	settings.resetMap() # reset the map to be 0
	head = None
	for snake in snakeCoords:
		coordinates = snake.get('coords')
		for xy in coordinates:
			settings.getMap()[xy[0]][xy[1]] = 1
		if snake.get('id') == id:
			head = snake.get('coords')[0]
	# print settings.getMap()
	print head
	possibleAround(head, directions)
	print directions
	return directions

#check four possible moves of the head
def possibleAround(head, directions):
	if settings.isCollided([head[0] + 1, head[1]]):
		del directions['0']
	if settings.isCollided([head[0], head[1] + 1]):
		del directions['1']
	if settings.isCollided([head[0] - 1, head[1]]):
		del directions['2']
	if settings.isCollided([head[0], head[1] - 1]):
		del directions['3']
