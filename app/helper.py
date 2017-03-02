import settings




# return all possible moves in one block surrounding area
def possibleMove(coord, snakeCoords):
	settings.resetMap()
	for snake in snakeCoords:
		coordinates = snake.get('coords')
		for xy in coordinates:
			settings.getMap()[xy[0]][xy[1]] = 1
	print settings.getMap()

def debug(name):
	pass
