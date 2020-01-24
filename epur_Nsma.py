from epur_data import EpurData
import math
import matplotlib.pyplot as plt 

def MakeXi(edata,scur):
    if scur <= edata.s_start:
        return 0
    elif scur >= edata.s_finish:
        return 1
    else:
        return 0.5+0.5*math.cos(math.pi*(scur-edata.s_finish)/(edata.s_start-edata.s_finish))

def MakeNsma(edata,F,A):
    scur = F/A;
    xi = MakeXi(edata,scur)
    return edata.eps_L*xi*edata.E*A
 
def DrawNN(edata):
    NMax = 0
    f, (axN,axW) = plt.subplots(2,1,sharex=True)
    plt.xlabel('N(H)')
#    axN.ylabel('$N_{sma}(H)$')
#    axW.ylabel('$W_{sma}(мм)$')
    for i in range(len(edata.rods)):
        r = edata.rods[i]
        NCMax = int(edata.s_finish*r[1]/50)*50+100
        NMax = max(NMax,NCMax)
        x = range(0,NCMax,50)
        y = [MakeNsma(edata,F,r[1]) for F in x ]
        axN.plot(x,y,label='$N_{sma,'+str(i)+'}$')
    nnodes = len(edata.rp)
    x = range(0,NMax,50)
    ys = [[] for _ in range(nnodes) ]
    for F in x:
        NSma = [ MakeNsma(edata,F,r[1]) for r in edata.rods ]
        RP=[0]
        for i in range(1,len(edata.rp)-1):
            RP.append(F*edata.rp[i]-NSma[i]+NSma[i-1])
        if edata.twosided:
            RP.append(0)
        else:
            RP.append(F*edata.rp[-1]+NSma[-1])
        Wsma = edata.SolveK(RP)
        for i in range(nnodes):
            ys[i].append(Wsma[i])
    for i in range(len(ys)):
        axW.plot(x,ys[i],'--',label= '$W_{sma,'+str(i)+'}$')
    axW.legend(loc="upper left")
    axN.legend(loc="upper left")

    plt.show()
