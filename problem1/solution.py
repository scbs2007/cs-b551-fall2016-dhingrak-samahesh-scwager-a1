import sys

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

	def addNeighbor(self, neighborName, length, speed, nameOfHighway):
		self.neighbors[neighborName] = (length, speed, nameOfHighway)
	
	def getAllNeighboringCities(self):
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

	def readCityGpsFile(self):
		cities = open("city-gps.txt", "r").read().split("\n")
		for i in range(len(cities) - 1):
			city = cities[i].split()
			node = City(city[0], city[1], city[2])
			#print("City: " + node.cityName + " Latitude: " + node.latitude + " Longitude: " + node.longitude)
			self.nodeList[city[0]] = node
			#print("City: " + city[0] + " Latitude: " + city[1] + " Longitude: " + city[2])
		#for node, nodeObj in self.nodeList.items():	
			#print(node + ": " + nodeObj.cityName)
	
	def readRoadSegmentsFile(self):
		segments =  open("road-segments.txt", "r").read().split("\n")
		for i in range(len(segments) - 1):
			segment = segments[i].split()
			#print(segment)
			#Handling missing speed values in file
			if (len(segment) == 5):
				firstCity, secondCity, length, speed, highwayName = segment[0], segment[1], segment[2], segment[3], segment[4]
			elif (len(segment) == 4):
				firstCity, secondCity, length, highwayName = segment[0], segment[1], segment[2], segment[3]
			if(firstCity not in self.nodeList):
				self.nodeList[firstCity] = City(firstCity, None, None)
			if(secondCity not in self.nodeList):
				self.nodeList[secondCity] = City(secondCity, None, None)
			self.nodeList[firstCity].addNeighbor(secondCity, length, speed, highwayName)
			self.nodeList[secondCity].addNeighbor(firstCity, length, speed, highwayName)
		self.displayGraph()

	def displayGraph(self):
		for node, nodeObj in self.nodeList.items():
			#if(node.startswith("Y_City")):
				print(node + ": " + str(nodeObj.getAllNeighboringCities()))
	
def takeInput():
	enteredValue = sys.argv
	startCity = enteredValue[1]
	endCity = enteredValue[2]
	routingOption = enteredValue[3]
	#print(enteredValue)

takeInput()
graph = RoadNetwork()
graph.readCityGpsFile()
graph.readRoadSegmentsFile()
