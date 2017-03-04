import math
class heatMap:
    
    def __init__(self):
            pass

    def findHeatMap(self, head, walls, num, width, height):
        x_Size = assignStartEnd(head, num, width)
        y_Size = assignStartEnd(head, num, height)
        heatMap = {}
        threatDepthConstant = 3

        for wall in walls:
            xCoff = -threatDepthConstant
            yCoff = -threatDepthConstant
            if wall[0][0] < x_Size[0] or wall[0][0] > x_Size[1] or wall[0][1] < y_Size[0] or wall[0][1] > y_Size[1]:
                continue
            for x in range(wall[0][0]-threatDepthConstant, wall[0][0] + threatDepthConstant):
               if(not(x<x_Size[0] or x>x_Size[1])):
                    yCoff = -threatDepthConstant
                    xCoff = xCoff + 1
                    for y in range(wall[0][1]-threatDepthConstant, wall[0][1] + threatDepthConstant):
                        if(not(y<y_Size[0] or y>y_Size[1])):
                            yCoff = yCoff + 1
                            weight = heatMap.get((x,y), 0)
                            distanceLoad = (xCoff**2+yCoff**2)**(1/2.0)
                            if distanceLoad == 0:
                                distanceLoad = 1
                            heatMap[(x,y)] = weight + wall[1]/distanceLoad
        #print(heatMap)

        return heatMap

def assignStartEnd(head, num, maxDistance):
    end = head[0]+num/2
    start = head[0]-num/2
    full = False #if end and start have to be resized, it sets them to the maxiumums
    if start < 0:#if start is negative
        addon = abs(start) #shaves off the negative
        start = 0 #sets it to the minimum
        end = end + addon #adds to the end of x_end
        full = True #flag
    elif end > maxDistance: #if end is too big
        addon = end - maxDistance #snags the extra bit
        start = start + addon #adds to start
        end = maxDistance #set to maximum
        full = True #flag
    elif full: #sets both to maximums
        start = 0
        end = maxDistance  
    return (start, end)     


                
def main():
    A = heatMap()
    j = [((4,4),16)]
    k = (4,4)
    print(A.findHeatMap(k,j,3, 10, 10))
    


if  __name__ =='__main__':main()
