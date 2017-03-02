#Hold global data structure so that subclass can access

Map = None
height = None
width = None
def initializeMap(w, h):
	global Map
	global height
	global width
	width = w
	height = h
	Map = [[y for y in range(h)] for x in range(w)]
	resetMap()

def getMap(): # not sure if should approach Python with this OOP
	global Map
	return Map

def resetMap():
	global Map
	global height
	global width
	for x in range(height):
		for y in range(width):
			Map[x][y] = 0