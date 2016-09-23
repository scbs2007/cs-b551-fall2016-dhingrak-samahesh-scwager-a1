#!/usr/local/bin/python3
from collections import deque
import sys
import time

finalOutput = deque()#Only used to display machine readable format of route
'''
Represents all properties of a city - its name, latitude, longitude and its neighbors.
neighbors is a dictionary with name of connected city as key and a tuple (length, speed, highway name) as value.
'''
class City:
    def __init__(self, cityName, latitude, longitude):
        self.cityName = cityName
        self.latitude = latitude
        self.longitude = longitude
        self.neighbors = {}
        self.visited = False #False = unvisited, True = visited

    def addNeighbor(self, neighborName, length, speed, nameOfHighway):
        distance = float(length)
        speedLimit = float(speed)
        time = round(distance/speedLimit, 2) #round(distance/70.0, 2) if speed=="0" else round(distance/speedLimit, 2)
        self.neighbors[neighborName] = (distance, speedLimit, time, nameOfHighway)
    
    def getAllNeighboringCities(self):
        return self.neighbors.items()

    def getWeight(self, neighborName):
        return self.neighbors[neighborName]

'''
Represents the entire graph. 
nodeList is a dictionary which stores name of the city as key and the City Object as value
'''
class RoadNetwork:
    def __init__(self):
        self.nodeList = {}
        self.followThisRoute = {} #Stores Parent of every node
        self.totalMiles = 0.0
        self.totalHours = 0.0

    def readCityGpsFile(self):
        citiesFile = open("city-gps.txt", "r")
        
        for line in citiesFile:
            city = line.split()
            node = City(*city)
            self.nodeList[city[0]] = node
        
        #self.nodeList = {line.split()[0]: City(*line.split()) for line in citiesFile}
        #citiesFile.close()

    def readRoadSegmentsFile(self):
        segmentsFile =  open("road-segments.txt", "r")
        for line in segmentsFile:
            segment = line.split()
            #Handling missing speed/length values in file - Will ignore that record.
            if("0" in segment or len(segment) is 4):#segment[2] == "0" or segment[3] == "0" or len(segment) == 4:
                continue
            firstCity, secondCity, length, speed, highwayName = segment
            '''if (len(segment) == 5):
                firstCity, secondCity, length, speed, highwayName = segment
            elif (len(segment) == 4):
                firstCity, secondCity, length, highwayName = segment
            '''
            #Handling Junction names - these names are not present in city-gps.txt
            if(firstCity not in self.nodeList):
                self.nodeList[firstCity] = City(firstCity, None, None)
            if(secondCity not in self.nodeList):
                self.nodeList[secondCity] = City(secondCity, None, None)
            self.nodeList[firstCity].addNeighbor(secondCity, length, speed, highwayName)
            self.nodeList[secondCity].addNeighbor(firstCity, length, speed, highwayName)
        #segmentsFile.close()
        #self.displayGraph()

    def displayGraph(self):
        for node, nodeObj in self.nodeList.items():
            print(node + ": " + str(nodeObj.getAllNeighboringCities())+"\n")

    def findRoute(self, startCityName, endCityName, routingOption, routingAlgorithm):
        if(routingAlgorithm == "bfs"):
            return self.bfs(startCityName, endCityName)
        elif(routingAlgorithm == "dfs"):
            return self.dfs(startCityName, endCityName)
        elif(routingAlgorithm == "ids"):
            return self.ids(startCityName, endCityName)
        elif(routingAlgorithm == "recursive_ids"):
            return self.recursive_ids(startCityName, endCityName)
        else:
            return self.astar(startCityName, endCityName, routingOption)

    #Returns True if path is found, else False
    def bfs(self, startCityName, endCityName):
        childParentDict = {}
        startCityObj = self.nodeList[startCityName]
        q = deque([startCityObj])
        while(q):
            currentCityObj = q.popleft()
            currentCityObj.visited = True
            if(currentCityObj.cityName == endCityName):
                self.createRouteFromDict(childParentDict, currentCityObj)
                return True
            for neighboringCityName, edgeWeight in currentCityObj.getAllNeighboringCities():
                neighboringCityObj = self.nodeList[neighboringCityName]
                if(not neighboringCityObj.visited):
                    q.append(neighboringCityObj)
                    if(neighboringCityObj not in childParentDict):
                        childParentDict[neighboringCityObj] = currentCityObj
                
        print("Path not found! :(")
        return False

    def createRouteFromDict(self, childParentDict, endCityObj):
        while(endCityObj in childParentDict):
            parentNode = childParentDict[endCityObj]
            self.followThisRoute[parentNode] = endCityObj
            endCityObj = parentNode

    '''
    Displays the route, total miles and total time in human readable format
    '''
    def displayRoute(self, startCityName):
        startCityObj = self.nodeList[startCityName]
        print("\nMove from".ljust(40) + "To".ljust(40) + "On Road".ljust(30) + "Total Miles".ljust(20) + "Miles/Hr".ljust(13) + "Total Hrs." + "\n" + "-"*155)
        while(startCityObj in self.followThisRoute):
            neighboringCityObj = self.followThisRoute[startCityObj]
            distance, speed, time, highwayName = startCityObj.neighbors[neighboringCityObj.cityName]
            self.totalMiles += distance
            self.totalHours += time
            finalOutput.append(startCityObj.cityName)
            print(startCityObj.cityName.ljust(40) + neighboringCityObj.cityName.ljust(40) + highwayName.ljust(30) + str(distance).ljust(20) + str(speed).ljust(15) + str(time))
            startCityObj = neighboringCityObj
        print("\nTotal Travel Miles: " + str(self.totalMiles) + "\nTotal Travel Hours: " + str(self.totalHours))
        finalOutput.append(startCityObj.cityName)
        finalOutput.appendleft(str(self.totalHours))
        finalOutput.appendleft(str(self.totalMiles))

    def dfs(self, startCityName, endCityName):
        childParentDict = {}
        startCityObj = self.nodeList[startCityName]
        q = deque([startCityObj])
        while(q):
            currentCityObj = q.pop()
            if(currentCityObj.cityName == endCityName):
                self.createRouteFromDict(childParentDict, currentCityObj)
                return True
            currentCityObj.visited = True
            for neighboringCityName, edgeWeight in currentCityObj.getAllNeighboringCities():
                neighboringCityObj = self.nodeList[neighboringCityName]
                if(not neighboringCityObj.visited):
                    q.append(neighboringCityObj)
                    if(neighboringCityObj not in childParentDict):
                        childParentDict[neighboringCityObj] = currentCityObj
        print("Path not found! :(")
        return False        

    def recursive_dls(self, currentCityObj, startCityName, endCityName, childParentDict, limit):
        if(currentCityObj.cityName == endCityName):
            self.createRouteFromDict(childParentDict, currentCityObj)
            return True
        elif limit == 0:
            return "cutoff"
        else:
            cutoff_occurred = False
            for neighboringCityName, edgeWeight in currentCityObj.getAllNeighboringCities():
                neighboringCityObj = self.nodeList[neighboringCityName]
                childParentDict[neighboringCityObj] = currentCityObj
                result = self.recursive_dls(self.nodeList[neighboringCityName], startCityName, endCityName, childParentDict, limit-1)
                if result == "cutoff":
                    cutoff_occurred = True
                elif result != "failure":
                    return result
            return "cutoff" if cutoff_occurred else "failure"

    def dls(self, startCityName, endCityName, limit):
        childParentDict = {}
        return self.recursive_dls(self.nodeList[startCityName], startCityName, endCityName, childParentDict, limit)

    def recursive_ids(self, startCityName, endCityName):
        for depth in range(5478):
            print("depth", depth)
            result = self.dls(startCityName, endCityName, depth)
            print("result", result)
            if result == "cutoff": continue
            if result == "failure":
                print("path not found :(")
                return False
            else: return True
    
    def ids(self, startCityName, endCityName):
        startCityObj = self.nodeList[startCityName]
        depthCount = 0
        q = deque()
        
        for i in range(5478): # no. of cities = 5478. In the worst case (impractical) we can have all cities on a single path and we want to go from root to leaf.
            visited = {} #cannot use City.visited
            childParentDict = {}
            currentDepth = 0
            q.append((startCityObj, currentDepth))
            while(q):
                currentCityObj, atDepth = q.pop()
                
                if(currentCityObj.cityName == endCityName):
                    self.createRouteFromDict(childParentDict, currentCityObj)
                    return True
                visited[currentCityObj] = True
                if(atDepth != i):
                    for neighboringCityName, edgeWeight in currentCityObj.getAllNeighboringCities():
                        neighboringCityObj = self.nodeList[neighboringCityName]
                        if(neighboringCityObj not in visited):
                            q.append((neighboringCityObj, atDepth + 1))
                            if(neighboringCityObj not in childParentDict):
                                childParentDict[neighboringCityObj] = currentCityObj
        print("Path not found! :(")
        return False
    
    def astar(self, startCityName, endCityName, routingOption):
        return

def validateRoutingOptions(routingAlgorithm, routingOption):
    if(routingOption not in ("segments", "distance", "time", "scenic")):
        print("Incorrect routing option entered! Please enter one of segments, distance, time or scenic.")
        sys.exit(0)
    elif(routingAlgorithm not in ("bfs", "dfs", "ids", "astar")):
        print("Incorrect routing algorithm entered! Please enter one of bfs, dfs, ids or astar.")
        sys.exit(0)

def validateCities(graph, startCity, endCity):
    if(startCity not in graph.nodeList or endCity not in graph.nodeList):
        print("Invalid City name entered!")
        sys.exit(0)

def main():
    enteredValue = sys.argv
    
    '''
    if(len(sys.argv)):
        print("Please enter all arguments! Execution: python3 solution.py <Source City> <Destination City> <Routing Option> <Routing Algorithm>")
        sys.exit(0)
    '''
    startCityName = enteredValue[1]
    endCityName = enteredValue[2]
    routingOption = enteredValue[3]
    routingAlgorithm = enteredValue[4]
    #validateRoutingOptions(routingAlgorithm, routingOption)
    
    startTime = time.time()
    graph = RoadNetwork()
    graph.readCityGpsFile()
    graph.readRoadSegmentsFile()
    endTime = time.time()
    #validateCities(graph, startCityName, endCityName)
    if(startCityName == endCityName):
        print("You are already there!")
        sys.exit(0) 
    #graph.displayGraph()
    print("Created road network in: " + str((endTime - startTime)/60) + " min.")
    startTime = time.time()
    foundRoute = graph.findRoute(startCityName, endCityName, routingOption, routingAlgorithm)
    endTime = time.time()
    if(foundRoute):
        graph.displayRoute(startCityName)
        print("Found route in: " + str((endTime - startTime)/60) + " min.")
    print("\nMachine Readable Format:\n" + " ".join(finalOutput))
if __name__ == "__main__":
    main()
