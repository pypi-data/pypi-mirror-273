from procedure_data_tool.utils.node import Node

class TankReturn(Node):
    directions = 1
    def __init__(self, ein, pit = None, jumper = None, jumperLabel = None, dvi = None):
        super().__init__(ein, pit, jumper) 
        self.ein = ein
        self.directions = 1 
        self.node_1 = None
        self.connections = []
        self.show = True
        self.dvi_credited 
        self.dvi_used = False
        self.in_tank = True
        self.color = "limegreen"

        # HAVE EIN OUTPUT JUST THE LABEL (Last character)
        def EIN(self):
            return None
