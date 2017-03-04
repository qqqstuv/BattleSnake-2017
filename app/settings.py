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
	Map = GridWithWeights(width, height)
	# diagram4 = GridWithWeights(10, 10)
	# diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
	print "HEIGHT is ", height # need this line because without this resetMap wouldnt recognize height/width

def getMap(): # not sure if should approach Python with this OOP
	global Map
	return Map

#return if the given coord is bounded on the map
def isOutOfBound(coord):
	return (coord[0] < 0 or coord[0] >= width or coord[1] < 0 or coord[1] >= height)

#return true if the given coord overlaps with an entitiy on the map
def isOverlap(coord):
	return (Map[coord[0]][coord[1]] == 1)
def isCollided(coord):
	return isOutOfBound(coord) or isOverlap(coord)

class SquareGrid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.food = []
    
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id): # self.walls contains tuple of ((x,y), weight)
        return id not in [item[0] for item in self.walls]
    
    def neighbors(self, id): # return possible neighbors around the point
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super(GridWithWeights, self).__init__(width, height)
        self.weights = {} # {(x,y), w} hold the weight of the free grid
    
    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)