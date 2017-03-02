import settings




# return all possible moves in one block surrounding area
def possibleMove(id, snakeCoords):
	settings.resetMap() # reset the map to be 0
	head = None
	for snake in snakeCoords:
		coordinates = snake.get('coords')
		for xy in coordinates:
			settings.getMap()[xy[0]][xy[1]] = 1
		if snake.get('id') == id:
			head = snake.get('coords')[0]
	print settings.getMap()
	print head


def debug(name):
	pass
