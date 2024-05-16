from procedure_data_tool.utils.node import Node

class Valve(Node):
    connections = []
    directions = 0
    def __init__(self, ein, pit = None, jumper = None, jumperLabel = None, dvi = None):
        super().__init__(ein, pit= pit, jumper = jumper) 
        self.connections
        self.directions
        self.show = True
        self.in_tank = False
        self.jumper = jumper
        self.jumperLabel = jumperLabel
        self.dvi_credited = dvi
                
        