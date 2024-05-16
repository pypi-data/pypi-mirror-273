from procedure_data_tool.utils.node import Node

class Pit():
    def __init__(self, name, nace = None, nacePMID = None, label = None, drain = None, drainSealPos = None):
        self.name = name
        self.nace = nace
        self.nacePMID = nacePMID
        self.heaters = []
        self.tfsps = []
        self.tfsps_pmid = []
        self.nodes = []
        self.label = label
        self.drain = drain
        self.drainSealPos = drainSealPos 
        self.encasementDrainValve = []
        self.edvPos = []