import c4d
#Welcome to the world of Python

def main():
    myObj = op.GetDown()
    if not myObj: return None

    hClone = op.GetAndCheckHierarchyClone(hh, myObj, c4d.HIERARCHYCLONEFLAGS_ASPOLY, False)

    if not hClone['dirty']:
        return hClone['clone']

    clone = hClone['clone']
    nbr = c4d.utils.Neighbor()
    nbr.Init(clone)

    pntCnt = clone.GetPointCount()
    polyCnt = clone.GetPolygonCount()
    exPnts = []
    exPolys = []
    for x in range(pntCnt):
        polys = nbr.GetPointPolys(x)
        if len(polys) > 8:
            exPolys.extend(polys) # adds individual polys to new list
            exPnts.append(x)
    
    #remove duplicates
    exPolys = list(dict.fromkeys(exPolys))
    exPnts = list(dict.fromkeys(exPnts))
            
    newPntCnt = pntCnt - len(exPnts)
    newPolyCnt = polyCnt - len(exPolys)
    newObj = c4d.PolygonObject(newPntCnt, newPolyCnt)
    
    newPntMap = dict()
    pntIndex = 0
    for x in range(pntCnt):
        if x not in exPnts:
            newObj.SetPoint(pntIndex, clone.GetPoint(x))
            newPntMap[x] = pntIndex
            pntIndex += 1
    
    polyIndex = 0
    for x in range(polyCnt):
        if x not in exPolys:
            polygon = clone.GetPolygon(x)
            polygon.a = newPntMap[polygon.a]
            polygon.b = newPntMap[polygon.b]
            polygon.c = newPntMap[polygon.c]
            try:
                polygon.d = newPntMap[polygon.d]
            except:
                print 'polygon %s is not a quad' % (x)
        
            newObj.SetPolygon(polyIndex, polygon)
            polyIndex += 1
    
    return newObj