import copy
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
    def __init__ (self,twosided = False, E = 1., eps_L = 0.01, s_start = 10, s_finish = 100, rods = [] ,nodes = []):
        self.twosided = twosided
        self.rods = rods
        self.nodes = nodes
        self.E = E
        self.eps_L = eps_L
        self.s_start = s_start
        self.s_finish = s_finish
        self.MakeMatrix()
        self.rp = [0]+self.nodes
        if self.twosided:
            self.rp+=[0]
        self.a = self.SolveK(self.rp)

    def MakeMatrix(self):
#        nnodes = len(self.nodes) + 1 + (1 if self.twosided else 0)
        nrods = len(self.rods)
        nnodes = nrods + 1
        self.K = [[ 0 for j in range(nnodes+1)] for k in range(nnodes)]
        for j in range(nrods):
            d = self.rods[j][1]*self.E/self.rods[j][0]
            self.K[j][j]+=d
            self.K[j][j+1]-=d
            self.K[j+1][j]-=d
            self.K[j+1][j+1]+=d
        self.K[0][1] = 0
        self.K[1][0] = 0
        if self.twosided:
            self.K[nnodes-1][nnodes-2] = 0
            self.K[nnodes-2][nnodes-1] = 0

    def SolveK(self,b):
        nnodes = len(self.K[0])-1
        K = copy.deepcopy(self.K)
        for k in range(nnodes):
            K[k][nnodes] = b[k]
        Gauss(K)
        return [ K[i][nnodes] for i in range(nnodes) ]

def LoadEpur(fileName):
    f = open(fileName,"r")
    ts = (f.readline().strip() == "True")
    E = float(f.readline())
    eps_L = float(f.readline())
    s_start = float(f.readline())
    s_finish = float(f.readline())
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
    return EpurData(ts,E, eps_L, s_start, s_finish, rods,nodes)


