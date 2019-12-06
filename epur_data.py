class EpurData:
    def __init__ (self,twosided = False, data = [] ):
        self.twosided = twosided
        self.data = data

def LoadEpur(fileName):
    f = open(fileName,"r")
    ts = (f.readline().strip() == "True")
    rods = int(f.readline())
    data = []
    for x in range(rods):
        l = float(f.readline())
        a = float(f.readline())
        data.append([l,a])
    return EpurData(ts,data)

