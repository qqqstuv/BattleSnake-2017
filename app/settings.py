#Hold global data structure so that subclass can access

Map = None

def initializeMap(width, height):
	global Map
	Map = [[y for y in range(height)] for x in range(width)]

def getMap(): # not sure if should approach Python with this OOP
	global Map
	return Map