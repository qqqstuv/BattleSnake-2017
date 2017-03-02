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
	print "HEIGHT is ", height # need this line because without this resetMap wouldnt recognize height/width

def getMap(): # not sure if should approach Python with this OOP
	global Map
	return Map

def resetMap():
	for x in range(height):
		for y in range(width):
			Map[x][y] = 0

#return if the given coord is bounded on the map
def isOutOfBound(coord):
	return (coord[0] < 0 or coord[0] >= width or coord[1] < 0 or coord[1] >= height)

#return true if the given coord overlaps with an entitiy on the map
def isOverlap(coord):
	return (Map[coord[0]] and Map[coord[0]][coord[1]])

def isCollided(coord):
	return isOutOfBound(coord)