from geopy.geocoders import Nominatim
import math
import sys
import itertools

from database import Database


class ShortestPathFinder:
    def __init__(self, start_address, list_of_address, list_of_names):
        self.start_point = self.getLocByAddress(start_address)
        self.points = self.getPointsFromAddresses(list_of_address)
        self.names = list_of_names
        self.addresses = list_of_address
        self.graph = self.buildGraph()
        self.distances, self.predecessors = self.dijkstra(self.graph, self.start_point)

    def getLocByAddress(self, address):
        loc = Nominatim(user_agent="GetLoc")
        location = loc.geocode(address)
        pointX = location.latitude
        pointY = location.longitude
        return (pointX, pointY)

    def getPointsFromAddresses(self, addresses):
        points = []
        for address in addresses:
            points.append(self.getLocByAddress(address))
        return points

    def dist(self, x, y):
        return math.hypot(y[0] - x[0], y[1] - x[1])

    def buildGraph(self):
        graph = {}
        for i, point in enumerate(self.points):
            graph[i] = {}
            for j, other_point in enumerate(self.points):
                if i == j:
                    continue
                distance = self.dist(point, other_point)
                graph[i][j] = distance
        return graph

    def dijkstra(self, graph, start):
        distances = {}
        predecessors = {}
        unseen_nodes = list(graph.keys())
        for node in unseen_nodes:
            distances[node] = sys.maxsize
        distances[start] = 0
        while unseen_nodes:
            current_node = None
            for node in unseen_nodes:
                if current_node is None:
                    current_node = node
                elif distances[node] < distances[current_node]:
                    current_node = node
            for neighbor, distance in graph[current_node].items():
                if distances[current_node] + distance < distances[neighbor]:
                    distances[neighbor] = distances[current_node] + distance
                    predecessors[neighbor] = current_node
            unseen_nodes.remove(current_node)
        return distances, predecessors

    def get_shortest_path(self):
        current_node = self.points.index(self.start_point)
        path = []
        while current_node in self.predecessors:
            path.insert(0, current_node)
            current_node = self.predecessors[current_node]
        path.insert(0, current_node)
        path_points = [self.points[node] for node in path]
        path_names = [self.names[self.addresses.index(self.getAddressFromPoint(point))] for point in path_points]
        return path_names, path_points

    def getAddressFromPoint(self, point):
        closest_address = None
        closest_distance = float('inf')
        for i, p in enumerate(self.points):
            distance = self.dist(point, p)
            if distance < closest_distance:
                closest_distance = distance
                closest_address = self.addresses[i]
        return closest_address

    