#Hold global data structure so that subclass can access


def initialize(width, height):
	global mapSize
	mapSize = [width, height]
