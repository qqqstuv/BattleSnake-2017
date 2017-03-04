import math
class heatMap:
    
    def __init__(self):
            pass

    def findHeatMap(self, head, headList, walls, width, height):
		num = 15 #has to be odd
		threatDepthConstant = 5 #has to be odd divided by 2
		borderWeight = 3 #borderWeight
		beta = 4 # standard coefficient for border
		theta = 1.5 # coefficient for duration
		defaultHeadWeight = theta*15 #snakeHeadWeight multiplier
		alpha = None
		for i in headList:
			walls.remove(i)
			walls.append((i[0],defaultHeadWeight))
		walls = addBorders(walls, width, height, borderWeight) #adds the borders to the list of walls
		x_Size = assignStartEnd(head, num, width)
		y_Size = assignStartEnd(head, num, height)
		heatMap = {}
		for wall in walls:
			points = pointsAroundCoord(wall, threatDepthConstant, x_Size, y_Size) #returns a list of points of the form ((x,y),weight)
			for point in points:
				if heatMap.has_key(point):
					heatMap[point] = heatMap[point] + points[point]
				else:
					heatMap[point] = points[point]
			
		for wall in walls:
			if heatMap.has_key(wall[0]):
				del heatMap[wall[0]]
		return heatMap
	
def pointsAroundCoord(wall, num, x_Size, y_Size):
	points = {}
	point = wall[0]
	startLeft = point[0] - num/2
	endLeft = point[0] + num/2
	startTop = point[1] - num/2
	endTop = point[1] + num/2
	for i in range(startLeft, endLeft+1):
		for j in range(startTop, endTop+1):
			if(i< x_Size[0] or j< y_Size[0] or (i==point[0] and j == point[1])):
				continue
			if( i> x_Size[1] or j > y_Size[1]):
				continue
			divisor = 2*math.sqrt(((abs(point[0])-abs(i))**2) + ((abs(point[1]) - abs(j))**2))
			if(divisor == 0):
					divisor = 1
			if points.has_key((i,j)):
				points[(i,j)] = points[(i,j)] + wall[1]/divisor
			else:
				points[(i,j)] = wall[1]/divisor
	
	return points
	
def addBorders(walls, width, height, borderWeight):
	for i in range(-1, width+1): #x = -1 to max, y = max
		walls.append(((i,-1),borderWeight))
	for j in range(-1, width+1):  #x = -1 to max, y = -1
		walls.append(((j,height),borderWeight))
	for k in range(0, height): #y = 0 to height-1, since x got it, and x = -1
		walls.append(((-1, k), borderWeight))
	for l in range(0, height):
		walls.append(((width,l), borderWeight)) #y = 0 to height-1, and x = width
	
	return walls

def assignStartEnd(head, num, maxDistance):
	end = head[0]+num/2
	start = head[0]-num/2
	full = False #if end and start have to be resized, it sets them to the maximums
	if start < 0:#if start is negative
		addon = abs(start) #shaves off the negative
		start = 0 #sets it to the minimum
		end = end + addon #adds to the end of x_end
		full = True #flag
	if end > maxDistance: #if end is too big
		addon = end - maxDistance #snags the extra bit
		start = start + addon #adds to start
		end = maxDistance #set to maximum
	else:
		full = False
		
	if full: #sets both to maximums
		start = 0
		end = maxDistance
	return (start, end)

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)
                
def main():
	A = heatMap()
	j = [((5,5),6),((9,9),6),((1,1),6),((1,9), 6),((9,1),6)]
	headSnakes = [((9,9),6), ((1,1),6)]
	testB = []
	testB = addBorders(testB, 3,3,5)
	if len(testB) == 16:
		print("border good")
	else:
		print("error")
		print(testB)
	wall = ((1,4),5)
	num = 3
	x_Size = (0,6)
	y_Size = (0,6)
	testA = pointsAroundCoord(wall, num, x_Size, y_Size)
	for i in range(x_Size[1]):
		print('\n')
		for k in range(y_Size[1]):
			if testA.has_key((i,k)):
				print(int(testA[(i,k)]) ),
			else:
				print('-'),
	
	
	k = (5,5)
	x = 11
	y = 11
	for i in range(x):
		print('\n')
		for k in range(y):
			passable = True
			for p in range(len(j)):
				if j[p][0] == (i,k):
					print(j[p][1]),
					passable = False
			if passable:
				print('-'),
	print('\n\nMap')
	k = (5,5)
	x = 11
	y = 11
	map = A.findHeatMap(k,headSnakes, j, x, y)
	for i in range(x):
		print('\n')
		for k in range(y):
			if map.has_key((i,k)):
				print(int(map[(i,k)]) ),
			else:
				print('-'),
		
    


if  __name__ =='__main__':main()
