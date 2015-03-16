import rhinoscriptsyntax as rs
import math as m
import random as r



def Main():
#input from user
    gens = rs.GetReal("how many Gens?", 4)
    if gens is None: #error Checking
        print "forgot input"
        return

    startingArr = rs.GetObjects("select starting shapes", 16)
    if gens is None: #error Checking
        print "forgot input"
        return
#input the number of objects in rhino file
    shapeOneNumber = 5
    shapeTwoNumber = 9
#save empty list for objects T & B
    objArr1 = []
    objArr2 = []
#loop to get data from rhino into python
    for i in range(0,shapeOneNumber):
        arrTemp = rs.ObjectsByName("T"+str(i)) #inputs shapes by name t0,t1,t2...shapeOneNumber
        if arrTemp is None:
            print "missing parts"
            return
        objArr1.append(arrTemp[0])
#loop to get data from rhino into python
    for i in range(0,shapeTwoNumber):
        arrTemp = rs.ObjectsByName("B"+str(i))
        if not arrTemp:
            print "missing parts"
            return
        objArr2.append(arrTemp[0])
    rs.EnableRedraw(False)
#loop through startingArr, the hsapes input by user to grow from
    for shapeRun in startingArr:
    #switch to grow as T or B
        blnObj = True
        if r.random() > .5:
            blnObj = False

        if blnObj:
            ThreeDPack(shapeRun, objArr1, gens, gens, objArr1, objArr2)#Arr1 = T, Arr2=B
            rs.DeleteObject(shapeRun)
        else:
            ThreeDPack(shapeRun, objArr2, gens, gens, objArr1, objArr2)
            rs.DeleteObject(shapeRun)


    rs.EnableRedraw(True)
#main recursive function to allow objects to grow
def ThreeDPack(target, objArr, gens, maxGen, objArr1, objArr2):

#switch to get out of recursion
    if gens>0:
#base 3 points to orient rule objects from
        arrBaseExplodedSrfs = rs.ExplodePolysurfaces(objArr[0], False)
        basePts = rs.SurfacePoints(arrBaseExplodedSrfs[1])
        base3Pts = [basePts[0], basePts[1], basePts[2]]
        rs.DeleteObjects (arrBaseExplodedSrfs)
        # targetObject

#target 3 points to orient to
        arrTargetExplodedSrfs = rs.ExplodePolysurfaces(target, False)
        targetPts = rs.SurfacePoints(arrTargetExplodedSrfs[1])
        target3Pts = [targetPts[0], targetPts[1], targetPts[2]]
        rs.DeleteObjects (arrTargetExplodedSrfs)

# orient objects 3pts no scale
        newObjs = OrientMultObjects(objArr, base3Pts, target3Pts, 1)
        rs.ObjectName (newObjs, "0") #changes object name to 0 so if code is run again, it doesn't select the wrong objects
#calculate a scale amount based on meta objects and new objects
        scale = (1 / rs.Distance(basePts[0], basePts[1])) * rs.Distance(targetPts[0], targetPts[1])
        #scale objects
        rs.ScaleObjects (newObjs, targetPts[0], [scale, scale, scale] )


#after the objects are oriented, loop through new objects & call ThreeDPack again!
        for i in range(0,len(newObjs)):
#switch to call ThreeDPack with objects B or T
            blnObjOne = True
            if r.random() > .5:
                blnObjOne = False
#another random to decide if even to grow
            if r.random() > .5:

                if blnObjOne:
#recursion happens here:
                    ThreeDPack(newObjs[i], objArr1, gens-1, maxGen, objArr1, objArr2)
                    rs.DeleteObject(newObjs[i])
                else:
                    ThreeDPack(newObjs[i], objArr2, gens-1, maxGen, objArr1, objArr2)
                    rs.DeleteObject(newObjs[i])


def OrientMultObjects(obj, ref, tar,flag):

    newObj= []

    for i in range(0,len(obj)):

        newObj.append(rs.OrientObject(obj[i],ref,tar,flag))

    return newObj

if( __name__ == "__main__" ):
    Main()
