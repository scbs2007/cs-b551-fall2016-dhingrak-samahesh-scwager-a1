'''
Formulation - 	The cities have been made into nodes in the graph.
		The RoadNetwork class below mainly stores a dictinary with key as the City Name and the value as the corresponding City Object.
		The City class stores all the details of a city including the city name, latitude, longitude value and a dict with key as neighboring city name and 
		value as a tuple with distance, speed limit, time of travel (computed while reading in the file), highway name.
		This tuple acts as the edge weight. 

		The initial state is the node for the start city that is entered and the goal is the end city node.
		The Cost function varies with different algorithms. It has been taken to be a constant for bfs, dfs and ids wheras it differs for a* depending on the 
		routing option as will be described below.
		State Space - Includes all the nodes in the graph.
		Successor function encodes all possible transitions of the states. All the nodes which are neighbors of a particular node are successor states.

All the algorithms bfs, dfs, ids, astar are iterative in nature - We thought it woud be best to do that instead of recursive in order to avoid the Stack Overflow error.

Problems faced - with inconsistent data. The generation of haversine distances for cities with missing latitude and longitude values was problematic.		
Simplifications - We have ignored missing speed/ length records and ignored records where the speed/ length values are 0.
More details in answers below:

Q1. Which search algorithm seems to work best for each routing options?
Ans. 
	Routing Option		Routing Algorithm which seems to works best		Comments
	--------------------------------------------------------------------------------------------------------------
	segments		A*						BFS, IDS give the same number of 
										segments as A* but take longer to find 
										the route most of the time - 
										i.e. unless the start and end city are 
										very close to each other.
	--------------------------------------------------------------------------------------------------------------
	distance		A*						All of BFS, DFS, IDS give suboptimal 
	----------------------------------------------------------------------	solutions for distance, time and
	time			A*						scenic. 
	----------------------------------------------------------------------	i.e. unless the start and end city are 
	scenic			A*						very close to each other.
	----------------------------------------------------------------------

	Note: Regardless of the routing option BFS would give the same route because the order in which the nodes are 
	inserted and removed from the fringe is fixed.
	Similar note for DFS and IDS.
	

Q2. Which algorithm is fastest in terms of the amount of computation time required by your program, and by how much, according to your experiments?
Ans. 
	Routing Option          Routing Algorithm which is fastest
                                (in terms of computation time)    
        ------------------------------------------------------------
        segments                A*				
        ------------------------------------------------------------
        distance                A*					
        ------------------------------------------------------------
        time                    A*                                              
        ------------------------------------------------------------
        scenic                  A*                                              
        ------------------------------------------------------------

	Sample for route finding from Bloomington,_Indiana to Columbus,_Ohio. Averaged execution time - code run 100 times

	Routing Option          Routing Algorithm which is fastest		Seconds taken to find route
				(in terms of computation time)			(Excluding time to create Graph)
	--------------------------------------------------------------------------------------------------------
        segments                A*                                              BFS - 0.0193
                                                                                DFS - 0.065
                                                                                IDS - 0.96
                                                                                A*  - 0.0032
	--------------------------------------------------------------------------------------------------------
        distance                A*                                              BFS - 0.0192
                                                                                DFS - 0.053
                                                                                IDS - 0.855
                                                                                A*  - 0.0018
	--------------------------------------------------------------------------------------------------------
        time                    A*                                              BFS - 0.0199
                                                                                DFS - 0.065
                                                                                IDS - 0.87
                                                                                A*  - 0.0027
	--------------------------------------------------------------------------------------------------------
        scenic                  A*                                              BFS - 0.0199
                                                                                DFS - 0.059
                                                                                IDS - 0.091
                                                                                A*  - 0.0082
	--------------------------------------------------------------------------------------------------------
	
	Note: 	A* shows a very significant improvement over all other routing algorithms. This difference keeps increasing as the distance between source and 
		destination increases.


Q3. Which algorithm requires the least memory, and by how much, according to your experiments?
Ans. 	Iterative Deepening Search requires the least amount of memory. 
	Also, depending on the start and end cities the maximum number of nodes in the fringe varies for BFS and DFS (See samples below). In the worst case the 
	maximum number of nodes that can possibly be in the fringe for DFS would be the total number of cities in the graph. Whereas it could possibly be much more 
	than that for BFS.
 	
	IDS takes 99.98% less memory than BFS for first sample below and 99.10% less memory than DFS for sample 2:

	Sample for route from Bloomington,_Indiana to Waco,_Texas:
	
	Routing Algorithm		Routing Option				Number of Nodes in Fringe
	--------------------------------------------------------------------------------------------------------
	A*				segments				201
					------------------------------------------------------------------------
					distance				165
					------------------------------------------------------------------------
					time					266
					------------------------------------------------------------------------
					scenic					510
	--------------------------------------------------------------------------------------------------------
	BFS				All routing options			434867	
	--------------------------------------------------------------------------------------------------------
	DFS				All routing options			1623
	--------------------------------------------------------------------------------------------------------
	IDS				All routing options			60
	--------------------------------------------------------------------------------------------------------

	Sample for route from Bloomington,_Indiana to Columbus,_Ohio
	
	Routing Algorithm		Routing Option				Number of Nodes in Fringe
	--------------------------------------------------------------------------------------------------------
	A*				segments				37
					------------------------------------------------------------------------
					distance				29
					------------------------------------------------------------------------
					time					26
					------------------------------------------------------------------------
					scenic					63
	--------------------------------------------------------------------------------------------------------
	BFS				All routing options			1805	
	--------------------------------------------------------------------------------------------------------
	DFS				All routing options			2682
	--------------------------------------------------------------------------------------------------------
	IDS				All routing options			24
	--------------------------------------------------------------------------------------------------------
	

Q4. Which heuristic function did you use, how good is it, and how might you make it better?
Ans.
Base Heuristic used - Calculated the distance between two points on the globe using the Haversine Formula. Also for cities and junctions which have missing latitude 
longitude values: have found out the neighbors of these locations and found used that neighbor's heuristic for this location. Also, note that if a node's all 
neighbors also do not have latitude longitude values then we look at their neighbors and so on. This heuristic is admissible because it is almost like a stright line
distance on the globe between two cities. But the actual road connecting the 2 cities would most likely not be a straight line. For:

	For segments: 	Have used the Base Heuristic * Segments per mile as the heuristic cost. This value segments per mile has been calculated by taking the total 
			length in the graph divided by the total number of segments.  
			(Total length and total number of segments is calculated while reading in the values from the file)

	For distance: 	Have used the base heuristic value. Since the Haversine formula would give a "as crow flies" distance, which would be like drawing a straight
			line on the globe, it would surely not overestimate the actual distance which would not all be straightly connected from start to end cities.

	For time: 	Have used the base heuristic value divided by the maximum allowed speed ie = 65 miles/hr as the heuristic value. This is always admissible
			because we are dividing the length by 65 which is the maximum speed allowed. So even if the actual speed of a road is less than 65 we would 
			be taking up a time value which is much less than the actual time that would be required to cover that road.

	For scenic: 	Here we try to allocate penalties for highways. We multiply the base heuristic value by 2(max speed on that road - 54) if the road segment
			has a speed limit >= 55. Else if the max. speed is < 55 we just take the base heuristic value as the heuristic. This would always be admissible
			because if the roads are highways they would be allocated higher heuristic values hence not be picked up from the priority queue.
	These heuristics give good results.

To further improve the heuristics we can instead of taking the maximum speed/average segments per mile, can look into taking those values of the route dynamically.
This is keeping in mind that there migh be incorrect data/ anomalies which would severely affect the average.


Q5. Supposing you start in Bloomington, which city should you travel to if you want to take the longest possible drive (in miles) that is still the shortest path to 	that city? (In other words, which city is furthest from Bloomington?)
Ans.
	Skagway,_Alaska.
	Used Dijkstra's to solve it. The last city that is popped from the fringe is the furthest.
	You can use the function findFarthestCityFromEnteredCity() for finding it. 
'''
from collections import deque
import sys, time, math
import heapq as hq

finalOutput = deque() #Only used to display machine readable format of route
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
		time = round(distance/speedLimit, 2)
		self.neighbors[neighborName] = (distance, speedLimit, time, nameOfHighway)
	
	def getAllInfoForNeighboringCities(self):
		return self.neighbors.items()

	def getNeighboringCitiesNames(self):
		return self.neighbors.keys()

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
		self.maxLengthOfFringe = 0 #To Calculate length of fringe
	
	def readCityGpsFile(self):
		citiesFile = open("city-gps.txt", "r")
		for line in citiesFile:
			city = line.split()
			node = City(*city)
			cityName = city[0]
			self.nodeList[cityName] = node
		citiesFile.close()

	def readRoadSegmentsFile(self):
		segmentsFile =  open("road-segments.txt", "r")
		for line in segmentsFile:
			segment = line.split()
			#Handling missing speed/length values in file - Will ignore that record.
			if("0" in segment or len(segment) is 4):
				continue
			firstCity, secondCity, length, speed, highwayName = segment
			
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
		segmentsFile.close()
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
			if(len(q) > self.maxLengthOfFringe):
				self.maxLengthOfFringe = len(q)
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
		print("\nMove from".ljust(40) + "To".ljust(40) + "On Road".ljust(35) + "Total Miles".ljust(20) + "Miles/Hr".ljust(13) + "Total Hrs." + "\n" + "-"*155)
		while(startCityObj in self.followThisRoute):
			neighboringCityObj = self.followThisRoute[startCityObj]
			distance, speed, time, highwayName = startCityObj.neighbors[neighboringCityObj.cityName]
			self.totalMiles += distance
			self.totalHours += time
			finalOutput.append(startCityObj.cityName)
			print(startCityObj.cityName.ljust(40) + neighboringCityObj.cityName.ljust(40) + highwayName.ljust(35) + str(distance).ljust(20) + str(speed).ljust(15) + str(time))
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
			if(len(q) > self.maxLengthOfFringe):
				self.maxLengthOfFringe = len(q)
		return False		

	def recursive_dls(self, currentCityObj, startCityName, endCityName, childParentDict, limit):
		if(currentCityObj.cityName == endCityName):
			self.createRouteFromDict(childParentDict, currentCityObj)
			return True
		elif limit == 0:
			return "cutoff"
		else:
			cutoff_occurred = False
			for neighboringCityName in currentCityObj.getNeighboringCitiesNames():
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
			if result == "cutoff": 
				continue
			if result == "failure":
				print("path not found :(")
				return False
			else: 
				return True
	
	def ids(self, startCityName, endCityName):
		startCityObj = self.nodeList[startCityName]
		stack = deque()
		
		for i in range(5478): #no. of cities=5478. In the worst case (impractical) we can have all cities on a single path and we want to go from root to leaf.
			visited = {} #Visited stores the cityObj as key and the depth when that city was visited as value
			childParentDict = {}
			stack.append((startCityObj, 0)) #Start City Object and Iteration Depth
			while(stack):
				currentCityObj, atDepth = stack.pop()
				if(currentCityObj.cityName == endCityName):
					self.createRouteFromDict(childParentDict, currentCityObj)
					return True
				visited[currentCityObj] = atDepth
				if(atDepth != i):
					for neighboringCityName in currentCityObj.getNeighboringCitiesNames():
						neighboringCityObj = self.nodeList[neighboringCityName]
						flag = False
						depthForThisNode = atDepth + 1
						if(neighboringCityObj not in visited or visited[neighboringCityObj] > depthForThisNode):
							if(neighboringCityObj not in visited or visited[neighboringCityObj] > depthForThisNode):
								flag = True
							stack.append((neighboringCityObj, depthForThisNode))
							visited[neighboringCityObj] = depthForThisNode
							if(neighboringCityObj not in childParentDict or flag):
								childParentDict[neighboringCityObj] = currentCityObj
					if(len(stack) > self.maxLengthOfFringe):
						self.maxLengthOfFringe = len(stack)
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
				return gScore[currentCityName] + length * 2 * (speed - 54) # Adding a penalty of 2 * (speed - 54) if it is a highway
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
					fScore[neighbor] = (gScore[neighbor] + self.calculateHaversineDistance(float(neighborCityObj.latitude), float(neighborCityObj.longitude), endLat, endLong)/65) if neighborCityObj.latitude != None else (gScore[neighbor] + self.generateHScore([(possibleGScore, neighbor, currentCityName)], endCityObj, routingOption))
				elif(routingOption == 'segments'):
					fScore[neighbor] = (gScore[neighbor] + self.calculateHaversineDistance(float(neighborCityObj.latitude), float(neighborCityObj.longitude), endLat, endLong) * self.segmentsPerMile) if neighborCityObj.latitude != None else (gScore[neighbor] + self.generateHScore([(possibleGScore, neighbor, currentCityName)], endCityObj, routingOption))
				elif(routingOption == 'scenic'):
					fScore[neighbor] = (gScore[neighbor] + self.calculateHaversineDistance(float(neighborCityObj.latitude), float(neighborCityObj.longitude), endLat, endLong) * self.getPenalty(currentCityName, neighbor)) if neighborCityObj.latitude != None else (gScore[neighbor] + self.generateHScore([(possibleGScore, neighbor,     currentCityName)], endCityObj, routingOption))
			
			if(len(pq) > self.maxLengthOfFringe):
				self.maxLengthOfFringe = len(pq)
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
				for item in [(gScore + self.calculateHaversineDistance(float(self.nodeList[neighborName].latitude), float(self.nodeList[neighborName].longitude), float(goalCityObj.latitude), float(goalCityObj.longitude))/65, neighborName) for gScore, neighborName, parent in nonJunctionCities]:
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

	def findFarthestCityFromEnteredCity(self, startCityName, routingOption):
		closedSet = set() #set of nodes already evaluated
		openSet = set([startCityName]) #set of currently discovered nodes still to be evaluated
		pq = [] #Used to find smallest fScore Value
		startCityObj = self.nodeList[startCityName]
		startLat = float(startCityObj.latitude)
		startLong = float(startCityObj.longitude)
		
		gScore = {startCityName: 0} #For each node - cost of getting from start node to that node 
		fScore = {startCityName: 0}
		
		while(openSet):
			for item in [(val, key) for key, val in fScore.items() if key in openSet]:
				hq.heappush(pq, item)
				
			currentCityName = hq.heappop(pq)[1]
			currentCityObj = self.nodeList[currentCityName]
			openSet.discard(currentCityName)
			closedSet.add(currentCityName)
			for neighbor in currentCityObj.getNeighboringCitiesNames():
				if(neighbor in closedSet):
					continue
				possibleGScore = gScore[currentCityName] + currentCityObj.neighbors[neighbor][0]
				if(neighbor not in openSet):
					openSet.add(neighbor)
				elif(possibleGScore >= gScore[neighbor]):
					continue
				gScore[neighbor] = possibleGScore
				fScore[neighbor] = gScore[neighbor]
			pq = []
	 	return currentCityName

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
	startCityName, endCityName, routingOption, routingAlgorithm = enteredValue[1:5]
	
	validateRoutingOptions(routingAlgorithm, routingOption)
	#totalTime = 0.0 #Used fo rmeasuring time of route finding for numberOfIterations
	#numberOfIterations = 100
	#for i in range(numberOfIterations):
	#	global finalOutput
	#	finalOutput = deque()
	graph = RoadNetwork()
	graph.readCityGpsFile()
	
	startTime = time.time()
	graph.readRoadSegmentsFile()
	endTime = time.time()
	validateCities(graph, startCityName, endCityName)
	
	if(startCityName == endCityName):
		print("You are already there!")
		sys.exit(0)	
	#graph.displayGraph()
	print("Created road network in: " + str(round((endTime - startTime)/60, 5)) + " min.")
	startTime = time.time()
	foundRoute = graph.findRoute(startCityName, endCityName, routingOption, routingAlgorithm)
	endTime = time.time()
	#totalTime += (endTime - startTime)
	#	continue	
	if(foundRoute):
		graph.displayRoute(startCityName)
		print("Max. Length of Fringe: " + str(graph.maxLengthOfFringe))
		print("Found route in: " + str(round((endTime - startTime)/60, 5)) + " min.")
		print("\nMachine Readable Format:\n" + " ".join(finalOutput))
	else:
		print("Path not found! :(")
	
	#print(routingOption + ", " + routingAlgorithm + ": " + str(totalTime / numberOfIterations))
	#print(graph.findFarthestCityFromEnteredCity("Bloomington,_Indiana", "distance"))
		
if __name__ == "__main__":
	main()
