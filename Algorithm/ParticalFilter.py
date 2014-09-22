import os
import math
import random
import ipdb



def CostFunc(inPartical):
    Cost = list()
    return Cost

def InitialPartical(numPartical, numUnknown):
    Partical = []
    for I in range(0, numPartical):
        Partical.append([random.random() for _ in xrange(numUnknown)])

    return Partical

def ScaleVar(inPartical, inRange):
    outPartical = inPartical
    numPartical = inPartical.__len__()
    numVar      = inRange.__len__()
    for CurPartical in range(0, numPartical):
        for CurVar in range(0, numVar):
            #before scaling
            print(inPartical[CurPartical][CurVar])
            #after scaling
            LowBound   = inRange[CurVar][0]
            UpperBound = inRange[CurVar][1]
            outPartical[CurPartical][CurVar] = LowBound + (UpperBound-LowBound)*inPartical[CurPartical][CurVar]

    return outPartical

def EvaCost(inPartical):
    numPartical = inPartical.__len__()
    outCost = [1e10]*numPartical
    for indx in range(0, numPartical):
        outCost[indx] = CostFunc(inPartical[indx])
    return outCost


def CostFunc(inV):
    # ipdb.set_trace()
    X = inV[0]
    Y = inV[1]
    cost = math.pow(X-0,2) + math.pow(Y-15,2)
    return cost

def CostProb(inCost):
    from operator import div, sub, add
    minCost = min(inCost)
    totalProb = sum(map(add, inCost, [minCost]*inCost.__len__()))
    outProb = []
    for CurCost in inCost:
        Normal = 1-(CurCost + minCost)/totalProb
        outProb.append(Normal)
    ipdb.set_trace()


if __name__ == '__main__':
    Range = [ [-1, 1], \
              [10, 20], \
            ]
    numUnknown = 2
    numPartical = 5
    Partical = InitialPartical(numPartical, numUnknown)
    ScalePartical = ScaleVar(Partical, Range)
    cost = EvaCost(ScalePartical)
    CostProb(cost)
    print(ScalePartical)
    print(cost)
    ipdb.set_trace()
    os.system('pause')
