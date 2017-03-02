#Hold global data structure so that subclass can access

Map = None

def initializeMap(width, height):
	global Map
	Map = [[0 for y in range(height)] for x in range(width)]
	print Map


def getMap(): # not sure if should approach Python with this OOP
	global Map
	return Map