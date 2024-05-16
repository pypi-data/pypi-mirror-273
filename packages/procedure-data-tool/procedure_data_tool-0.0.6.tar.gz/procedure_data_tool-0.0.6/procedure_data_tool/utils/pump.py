from procedure_data_tool.utils.node import Node

class Pump(Node):
    directions = 100
    def __init__(self, ein, pit = None, jumper = None, jumperLabel = None, dvi = None):
        super().__init__(ein, pit = None, jumper = None) 
        self.ein = ein
        self.directions = 100 
        self.node_1 = None
        self.connections = []
        self.show = True
        self.dvi_credited 
        self.dvi_used = False
        self.in_tank = True
        self.color = "mediumpurple"