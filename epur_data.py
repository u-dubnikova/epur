def Gauss(M):
    n = len(M)
    for i in range(n):
        for j in range(i,n):
            if M[j][i] != 0:
                break;
        if j != i:
            tmp = M[j]
            M[j] = M[i]
            M[i] = tmp
        d = M[i][i]
        M[i][i] = 1
        for j in range(i+1,n+1):
            M[i][j]/=d
        for j in range(i+1,n):
            d = M[j][i]
            M[j][i] = 0
            for k in range(i+1,n+1):
                M[j][k] -= d*M[i][k]
    for i in range(n-1,-1,-1):
        for j in range(i+1,n):
            M[i][n]-=M[i][j]*M[j][n]
class EpurData:
    def __init__ (self,twosided = False, rods = [] ,nodes = []):
        self.twosided = twosided
        self.rods = rods
        self.nodes = nodes
    def MakeMatrix(self):
        nnodes = len(self.nodes) + 1 + (1 if self.twosided else 0)
        nrods = len(self.rods)
        print(nnodes,nrods)
        K = [[ 0 for j in range(nnodes+1)] for k in range(nnodes)]
        for j in range(nrods):
            d = self.rods[j][1]/self.rods[j][0]
            K[j][j]+=d
            K[j][j+1]-=d
            K[j+1][j]-=d
            K[j+1][j+1]+=d
        for k in range(len(self.nodes)):
            K[k+1][nnodes] = self.nodes[k]
        K[0][1] = 0
        K[1][0] = 0
        if self.twosided:
            K[nnodes-1][nnodes-2] = 0
            K[nnodes-2][nnodes-1] = 0
        Gauss(K)
        self.a=[ K[i][nnodes] for i in range(nnodes) ]

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
        nodes.append(float(f.readline()))
    ret =  EpurData(ts,rods,nodes)
    ret.MakeMatrix()
    return ret



