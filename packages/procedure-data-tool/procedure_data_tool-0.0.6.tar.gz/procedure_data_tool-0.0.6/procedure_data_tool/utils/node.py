from collections import deque

class Node:
    connections = []
    directions = 0
    pit = None
    jumper = None
    jumperLabel = None
    position = None
    onJumper = True
    dvi_credited = None
    in_tank = False
    color = 'lightgray'
    def __init__(self, ein, pit, jumper):
        self.ein = ein
        self.pit = pit
        self.jumper = jumper
        self.directions
        self.connections
        # self.dvi_credited 
        # self.dvi_used
        self.show = True
        self.in_tank = False
        self.dvi_credited = None
        self.jumperLabel
        self.position
        self.onJumper
        self.color

    def EIN(self):
        return self.ein
    
    def __str__(self):
        return self.ein
    
    def setPit(self, str):
        self.pit = str

    def setJumper(self, jumper):
        self.jumper = jumper

    def setPosition(self, route = None):
        return
    
    def connectBack(self, node):
        if node in self.connections: return
        elif len(self.connections) < self.directions: self.connect(node)
        else: 
            print(self.EIN(), "has maximum number of connections, cant connect back")
            print(type(self))
            for con in self.connections:
                print(con.EIN())
            # print(con.EIN() for con in self.connections)
        return

    def connect(self, *nodes):
        for node in nodes[:self.directions]:
            if node and node not in self.connections:
                if len(self.connections) <= self.directions:
                    self.connections.append(node)
                    node.connectBack(self)
                else:  
                    print("has maximum number of connections", self.EIN())
                    for connection in self.connections:
                        print(connection.EIN())

    # def addToPit():
    def report(self):
        print((self.EIN()), "connections: ")
        for node in self.connections:
            if (node):
                print(node.EIN())
            else:
                print("Missing Connection")
    
    def routesTo(self, target, num_routes = 1, exclude_target = None):
        paths = []
        queue = deque([[self]])

        while queue and len(paths) < num_routes:
            path = queue.popleft()
            node = path[-1]

            if node == target:
                if path not in paths:
                    paths.append(path)
                
            for connection in node.connections :
                if connection not in path and (exclude_target is None or exclude_target not in path):
                    queue.append(path + [connection])

        return paths