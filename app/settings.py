#Hold global data structure so that subclass can access

mapSize = None

def initialize(width, height):
	global mapSize
	mapSize = [width, height]
