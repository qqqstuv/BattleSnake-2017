import settings


# return all possible moves in one block surrounding area
def possibleMove(coord, snakeCoords):
	debug(settings.getMap())
	for snake in snakeCoords:
		coordinates = snake.get('coords')
		for xy in coordinates:
			settings.getMap()[xy[0]][xy[1]] = 1
	debug(settings.getMap())

def debug(name):
	print "Print in helper"
	print name
