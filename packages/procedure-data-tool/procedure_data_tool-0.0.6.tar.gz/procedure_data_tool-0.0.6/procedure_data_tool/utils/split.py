from procedure_data_tool.utils.node import Node

class Split(Node):
    directions = 3
    def __init__(self, ein, pit = None, jumper = None, jumperLabel = None, dvi = None):
        super().__init__(ein, pit, jumper)
        self.directions = 3; 
        self.ein = ein
        self.connections = []
        self.show = False
        self.in_tank = False
        self.onJumper = False
        self.color = "white"
        
    def EIN(self):
        return None
