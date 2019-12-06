class EpurData:
    def __init__ (self,twosided = False, rods = [] ,nodes = []):
        self.twosided = twosided
        self.rods = rods
        self.nodes = nodes

def LoadEpur(fileName):
    f = open(fileName,"r")
    ts = (f.readline().strip() == "True")
    nrods = int(f.readline())
    rods = []
    for i in range(nrods):
        l = float(f.readline())
        a = float(f.readline())
        rods.append([l,a])
    nnodes = nrods - 1 if ts else nrods
    nodes = []
    for i in range(nnodes):
        nodes.append(int(f.readline()))
    return EpurData(ts,rods,nodes)
