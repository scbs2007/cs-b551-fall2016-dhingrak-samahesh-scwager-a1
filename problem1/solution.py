#!/usr/local/bin/python3
'''
Answers:
1.

2.

3.

4.

5.
'''
from collections import deque #, OrderedDict
#from tempfile import TemporaryFile
import sys, time, math
#import numpy as np
import heapq as hq

finalOutput = deque()#Only used to display machine readable format of route
'''
Represents all properties of a city - its name, latitude, longitude and its neighbors.
neighbors is a dictionary with name of connected city as key and a tuple (length, speed, time, highway name) as value.
'''
class City:
	def __init__(self, cityName, latitude, longitude):
		self.cityName = cityName
		self.latitude = latitude
		self.longitude = longitude
		self.neighbors = {}
		self.visited = False #False = unvisited, True = visited

	def addNeighbor(self, neighborName, length, speed, nameOfHighway):
		distance = int(length)
		speedLimit = float(speed)
		time = round(distance/speedLimit, 2) #round(distance/70.0, 2) if speed=="0" else round(distance/speedLimit, 2)
		self.neighbors[neighborName] = (distance, speedLimit, time, nameOfHighway)
	
	def getAllInfoForNeighboringCities(self):
		return self.neighbors.items()

	def getNeighboringCitiesNames(self):
		return self.neighbors.keys()

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
		self.totalMiles = 0
		self.totalHours = 0.0
		self.totalGraphDistance = 0 #Total Road Length of Graph
		self.totalGraphSegments = 0 #Total edges in Graph
		self.segmentsPerMile = 0.0 #Average segments per mile in graph
		#self.haversine = np.zeros(shape=(5498, 5498)) #[[0.0 for x in range(5478)] for y in range(5478)] #To store precomputed distance between cities
		#self.cityIntegerMapping = {} 
	'''
	#Used to create the haversine array - Precomputed this distance for each pair of city to save on computation time during finding the route using a*
	def prePopulateHaversineMatrix(self):
		self.haversine = np.load("haversineDistances.npy")

	#Used to create the haversineDistances.npy file
	def createHaversineDistanceFile(self):
		cityNameList = self.nodeList.keys()
		for name1 in cityNameList:
			for name2 in cityNameList:
				cityObj1 = self.nodeList[name1]
				cityObj2 = self.nodeList[name2]
				if name1 == name2:
					self.haversine[self.cityIntegerMapping[name1]][self.cityIntegerMapping[name2]] = 0.0
				if name1.startswith("Jct") or name2.startswith("Jct"):
					continue
				#self.haversine[self.cityIntegerMapping[name1]][self.cityIntegerMapping[name2]] = self.calculateHaversineDistance(float(cityObj1.latitude), float(cityObj1.longitude), float(cityObj2.latitude), float(cityObj2.longitude))
		np.save("haversineDistances", self.haversine)
		sys.exit(0)
	'''
	
	def readCityGpsFile(self):
		citiesFile = open("city-gps.txt", "r")
		#dictFile = open("dictFile.txt", "w")
		#count = 0
		for line in citiesFile:
			city = line.split()
			node = City(*city)
			cityName = city[0]
			self.nodeList[cityName] = node
			#self.cityIntegerMapping[cityName] = count
			#count += 1
		'''
		dictFile.write("self.cityIntegerMapping = {")
		for k, v in self.cityIntegerMapping.items():
			dictFile.write("'"+k+"'" + ":" + str(v) +",")
		dictFile.write("}")
		dictFile.close()
		sys.exit(0)
		'''
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
			self.totalGraphDistance += int(length)
			self.totalGraphSegments += 1
			
		self.segmentsPerMile = self.totalGraphSegments / float(self.totalGraphDistance)
		#segmentsFile.close()
		#self.displayGraph()

	def displayGraph(self):
		for node, nodeObj in self.nodeList.items():
			print(node + ": " + str(nodeObj.getAllInfoForNeighboringCities())+"\n")

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
			for neighboringCityName in currentCityObj.getNeighboringCitiesNames():
				neighboringCityObj = self.nodeList[neighboringCityName]
				if(not neighboringCityObj.visited):
					q.append(neighboringCityObj)
					if(neighboringCityObj not in childParentDict):
						childParentDict[neighboringCityObj] = currentCityObj
				
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
		print("\nTotal Travel Miles: " + str(self.totalMiles) + "\nTotal Travel Hours: " + str(round(self.totalHours,4)))
		finalOutput.append(startCityObj.cityName)
		finalOutput.appendleft(str(round(self.totalHours,4)))
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
			for neighboringCityName in currentCityObj.getNeighboringCitiesNames():
				neighboringCityObj = self.nodeList[neighboringCityName]
				if(not neighboringCityObj.visited):
					q.append(neighboringCityObj)
					if(neighboringCityObj not in childParentDict):
						childParentDict[neighboringCityObj] = currentCityObj
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
		q = deque()
		
		for i in range(5478): # no. of cities = 5478. In the worst case (impractical) we can have all cities on a single path and we want to go from root to leaf.
			visited = {} #Visited stores the cityObj as key and the depth when that city was visited as value
			childParentDict = {}
			q.append((startCityObj, 0)) #Start City Object and Iteration Depth
			while(q):
				#print("Stack: " + " ".join([obj.cityName for obj,d in q]))
				currentCityObj, atDepth = q.pop()
				#print("DEPTH: " + str(atDepth) + "Popped: " + currentCityObj.cityName)
				if(currentCityObj.cityName == endCityName):
					self.createRouteFromDict(childParentDict, currentCityObj)
					return True
				visited[currentCityObj] = atDepth
				if(atDepth != i):
					for neighboringCityName in currentCityObj.getNeighboringCitiesNames():
						neighboringCityObj = self.nodeList[neighboringCityName]
						#print("Visited: " + " ".join([obj.cityName for obj in visited]))
						flag = False
						depthForThisNode = atDepth + 1
						if(neighboringCityObj not in visited or visited[neighboringCityObj] > depthForThisNode):
							if(neighboringCityObj in visited and visited[neighboringCityObj] > depthForThisNode):
								flag = True
							q.append((neighboringCityObj, depthForThisNode))
							visited[neighboringCityObj] = depthForThisNode
							if(neighboringCityObj not in childParentDict or flag):
								childParentDict[neighboringCityObj] = currentCityObj
				#print("---")
		return False
	
	def checkMissingLatLongValues(self, startCityName, endCityName):
		if self.nodeList[startCityName].latitude == None: 
			print("Entered start city is missing latitude longitude entries")
			sys.exit(0)
		elif self.nodeList[endCityName].latitude == None: 
			print("Entered end city is missing latitude longitude entries")
			sys.exit(0)
	
	def findPossibleGScore(self, routingOption, gScore, currentCityName, neighbor):
		if(routingOption == 'distance'):
			return gScore[currentCityName] + self.nodeList[currentCityName].neighbors[neighbor][0]
		elif(routingOption == 'time'):
			return gScore[currentCityName] + self.nodeList[currentCityName].neighbors[neighbor][2]
		elif(routingOption == 'segments'):
			return gScore[currentCityName] + 1
		elif(routingOption == 'scenic'):
			length, speed = self.nodeList[currentCityName].neighbors[neighbor][1:3]
			if(speed >= 55):	
				return gScore[currentCityName] + length * 2 * (speed - 54) # Adding a penalty of (speed - 55) if it is a highway
			else:
				return gScore[currentCityName] + length		

	def astar(self, startCityName, endCityName, routingOption):
		self.checkMissingLatLongValues(startCityName, endCityName)
		closedSet = set() #set of nodes already evaluated
		openSet = set([startCityName]) #set of currently discovered nodes still to be evaluated
		childParentDict = {} #for route
		pq = [] #Used to find smallest fScore Value
		startCityObj = self.nodeList[startCityName]
		endCityObj = self.nodeList[endCityName]
		startLat = float(startCityObj.latitude)
		startLong = float(startCityObj.longitude)
		endLat = float(endCityObj.latitude)
		endLong = float(endCityObj.longitude)
		
		gScore = {startCityName: 0} #For each node - cost of getting from start node to that node 
		fScore = {startCityName: 0} #Should have been = self.calculateHaversineDistance(startLat, startLong, endLat, endLong)} but it does not matter on the first iteration. #For each node - gscore + hscore
		
		while(openSet):
			for item in [(val, key) for key, val in fScore.items() if key in openSet]:
				hq.heappush(pq, item)
				
			currentCityName = hq.heappop(pq)[1]
			currentCityObj = self.nodeList[currentCityName]
			if(currentCityName == endCityName):
				self.createRouteFromDict(childParentDict, currentCityObj)
				return True
			openSet.discard(currentCityName)
			closedSet.add(currentCityName)
			for neighbor in currentCityObj.getNeighboringCitiesNames():
				if(neighbor in closedSet):
					continue
				possibleGScore = self.findPossibleGScore(routingOption, gScore, currentCityName, neighbor)
				#possibleGScore = gScore[currentCityName] + currentCityObj.neighbors[neighbor][0]
				if(neighbor not in openSet):
					openSet.add(neighbor)
				elif(possibleGScore >= gScore[neighbor]):
					continue
				neighborCityObj = self.nodeList[neighbor]
				childParentDict[neighborCityObj] = currentCityObj
				gScore[neighbor] = possibleGScore
				if(routingOption == 'distance'):
					fScore[neighbor] = (gScore[neighbor] + self.calculateHaversineDistance(float(neighborCityObj.latitude), float(neighborCityObj.longitude), endLat, endLong)) if neighborCityObj.latitude != None else (gScore[neighbor] + self.generateHScore([(possibleGScore, neighbor, currentCityName)], endCityObj, routingOption))
				elif(routingOption == 'time'):
					fScore[neighbor] = (gScore[neighbor] + self.calculateHaversineDistance(float(neighborCityObj.latitude), float(neighborCityObj.longitude), endLat, endLong)/70) if neighborCityObj.latitude != None else (gScore[neighbor] + self.generateHScore([(possibleGScore, neighbor, currentCityName)], endCityObj, routingOption))
				elif(routingOption == 'segments'):
					fScore[neighbor] = (gScore[neighbor] + self.calculateHaversineDistance(float(neighborCityObj.latitude), float(neighborCityObj.longitude), endLat, endLong) * self.segmentsPerMile) if neighborCityObj.latitude != None else (gScore[neighbor] + self.generateHScore([(possibleGScore, neighbor, currentCityName)], endCityObj, routingOption))
				elif(routingOption == 'scenic'):
					fScore[neighbor] = (gScore[neighbor] + self.calculateHaversineDistance(float(neighborCityObj.latitude), float(neighborCityObj.longitude), endLat, endLong) * self.getPenalty(currentCityName, neighbor)) if neighborCityObj.latitude != None else (gScore[neighbor] + self.generateHScore([(possibleGScore, neighbor,     currentCityName)], endCityObj, routingOption))
			pq = [] # Have to do this because there's no inbuilt way to update priority of a value in pq
		return False

	def getPenalty(self, city1, city2):
		speed = self.nodeList[city1].neighbors[city2][1]
		if(speed >= 55):
			return 2 * (speed - 54)
		return 1
			
	def getEdgeWeight(self, cityName, item, routingOption):
		if(routingOption == 'time'):
			return self.nodeList[cityName].neighbors[item][2]
		elif(routingOption == 'distance'):
			return self.nodeList[cityName].neighbors[item][0]
		elif(routingOption == 'segments'):
			return 1
		else:
			distance, speed = self.nodeList[cityName].neighbors[item][0:2]
			if(speed >= 55):
				return 2 * (speed - 54) * distance
			return distance

	#Finding the closest city from the junction (having lat, long values) between the goal and the junction. If all of those are junction look at the next evel and so on. 
	def generateHScore(self, cityObjects, goalCityObj, routingOption):
		neighboringCities = []
		nonJunctionCities = []
		pq = []
		for (gScore, cityName, parentCityName) in cityObjects:
			neighboringCities.extend([(gScore + self.getEdgeWeight(cityName, item, routingOption), item, cityName) for item in self.nodeList[cityName].getNeighboringCitiesNames() if item != parentCityName])
			
		for (gScore, cityName, parentCityName) in neighboringCities:
			if (not cityName.startswith('Jct') and self.nodeList[cityName].latitude != None):
				nonJunctionCities.append((gScore, cityName, parentCityName))
		if(nonJunctionCities):
			#Found non junction cities
			if(routingOption == 'distance'):
				for item in [(gScore + self.calculateHaversineDistance(float(self.nodeList[neighborName].latitude), float(self.nodeList[neighborName].longitude), float(goalCityObj.latitude), float(goalCityObj.longitude)), neighborName) for gScore, neighborName, parent in nonJunctionCities]:
					hq.heappush(pq, item)
				return hq.heappop(pq)[0]
			elif(routingOption == 'time'):
				for item in [(gScore + self.calculateHaversineDistance(float(self.nodeList[neighborName].latitude), float(self.nodeList[neighborName].longitude), float(goalCityObj.latitude), float(goalCityObj.longitude))/70, neighborName) for gScore, neighborName, parent in nonJunctionCities]:
					hq.heappush(pq, item)
				return hq.heappop(pq)[0]
			elif(routingOption == 'segments'):
				for item in [(gScore + self.calculateHaversineDistance(float(self.nodeList[neighborName].latitude), float(self.nodeList[neighborName].longitude), float(goalCityObj.latitude), float(goalCityObj.longitude)) * self.segmentsPerMile, neighborName) for gScore, neighborName, parent in nonJunctionCities]:
					hq.heappush(pq, item)
				return hq.heappop(pq)[0]
			else:
				for item in [(gScore + self.calculateHaversineDistance(float(self.nodeList[neighborName].latitude), float(self.nodeList[neighborName].longitude), float(goalCityObj.latitude), float(goalCityObj.longitude)) * self.getPenalty(parent, neighborName), neighborName) for gScore, neighborName, parent in nonJunctionCities]:
					hq.heappush(pq, item)
				return hq.heappop(pq)[0]
		else:
			#Did not find neighboring non junction cities
			return self.generateHScore(neighboringCities, goalCityObj, routingOption)

	def calculateHaversineDistance(self, lat1degrees, long1degrees, lat2degrees, long2degrees):
		#Radius of the Earth = 3959 miles - https://www.google.com/search?q=radius+of+the+earth%3F&ie=utf-8&oe=utf-8
		#Distance between two points on the globe = https://en.wikipedia.org/wiki/Haversine_formula

		lat1radians = math.radians(lat1degrees)
		long1radians = math.radians(long1degrees)
		lat2radians = math.radians(lat2degrees)
		long2radians = math.radians(long2degrees)
		return round(2 * 3959 * math.asin(math.sqrt(pow(math.sin((lat2radians - lat1radians) / 2), 2) + math.cos(lat1radians) * math.cos(lat2radians) * pow(math.sin((long2radians - long1radians) / 2), 2))), 3)


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
	startCityName, endCityName, routingOption, routingAlgorithm = enteredValue[1:5]
	#validateRoutingOptions(routingAlgorithm, routingOption)
	startTime = time.time()
	graph = RoadNetwork()
	graph.readCityGpsFile()
	
	#graph.haversine = graph.createHaversineDistanceFile()
	#if routingAlgorithm == "astar":
	#	graph.prePopulateHaversineMatrix()
	
	graph.readRoadSegmentsFile()
	endTime = time.time()
	#validateCities(graph, startCityName, endCityName)
	if(startCityName == endCityName):
		print("You are already there!")
		sys.exit(0)	
	#graph.displayGraph()
	print("Created road network in: " + str(round((endTime - startTime)/60, 5)) + " min.")
	startTime = time.time()
		
	foundRoute = graph.findRoute(startCityName, endCityName, routingOption, routingAlgorithm)
	endTime = time.time()
	if(foundRoute):
		graph.displayRoute(startCityName)
		print("Found route in: " + str(round((endTime - startTime)/60, 5)) + " min.")
		print("\nMachine Readable Format:\n" + " ".join(finalOutput))
	else:
		print("Path not found! :(")
		
if __name__ == "__main__":
	main()
