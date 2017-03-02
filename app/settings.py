#Hold global data structure so that subclass can access

mapSize = None

def initializeMapSize(width, height):
	global mapSize
	mapSize = [width, height]

def getMapSize(): # not sure if should approach Python with this OOP
	global mapSize
	return mapSize