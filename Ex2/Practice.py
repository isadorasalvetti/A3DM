'''.
Exercises Lab2
Isadora Salvett
March 14
.'''

import bpy
import mathutils

#Ex1:
def compCentroid(obj):
    nVerts = len(obj.data.vertices)
    x, y, z = 0, 0, 0
    for i in range(nVerts):
        coord=obj.data.vertices[i].co
        x += coord[0]
        y += coord[1]
        z += coord[2]
        #print (coord) 
        
    centroid = (r(x/nVerts), r(y/nVerts), r(z/nVerts)) 
    return centroid

#Ex2:
def compVertVar(obj):
    nEdgs = len(obj.data.edges)
    nVerts = len(obj.data.vertices)
    vertVal = [0] * nVerts
    minVert = (0.0, 0.0, 0.0)
    maxVert = (0.0, 0.0, 0.0)
    
    for i in range(nEdgs):
        vertVal[obj.data.edges[i].vertices[0]] += 1
        vertVal[obj.data.edges[i].vertices[1]] += 1
        
    return max(vertVal), min(vertVal), sum(vertVal)/len(vertVal)

#Ex3
#Create F:E data
def compFaceEdges(obj):
    nEdgs = len(obj.data.edges)
    nFcs = len(obj.data.polygons)
    
    #What faces are adjacent to each edge
    edgFcAdj = [()] * nEdgs
    
    for i in range (nEdgs):
        edg = obj.data.edges[i].vertices[:]
        for j in range (nFcs):
            fc = obj.data.polygons[j].vertices[:]
            
            #Check if edge belongs to face
            if (edg[0] in fc):
                if (edg[1] in fc):
                    tot=len(fc)
                    v1=fc.index(edg[0])
                    v2=fc.index(edg[1])
                    if  v1-v2 == 1 or v1-v2 == len(fc)-1:
                        edgFcAdj[i] = (j,) + edgFcAdj[i] 
                    elif v2-v1 == 1 or v2-v1 == len(fc)-1:
                        edgFcAdj[i] = edgFcAdj[i] + (j,)
                        
    return edgFcAdj
    
#Non-mifold edge: edges with less than 2 or more than 3 neighbooring faces.        
def countManifold(fcAdj):
    nEdgs = len(fcAdj)        
    mfold = 0
    bound = 0
    nonMfold = 0
    
    for i in range (nEdgs):
        if len(fcAdj[i]) == 2:
            mfold += 1
        elif len(fcAdj[i]) == 1:
            bound += 1
        else:
            nonMfold += 1
  
    return (mfold, bound, nonMfold)

#Ex4
#Concave or convex? | if dot product < 0, angle > 90 : convex
def concaveConvex(obj, fcAdj):
    polys = obj.data.polygons
    aveEdg = 0 #No of concave edges
    vexEdg = 0 #No of convex edges
    plane = 0
    for i in range(len(fcAdj)):
        if len(fcAdj[i]) == 2:
            n1 = polys[fcAdj[i][0]].normal
            n2 = polys[fcAdj[i][1]].normal
            cp = n1.cross(n2)
            cp = cp[0] + cp[1] + cp[2]

            if cp > 0:
                vexEdg += 1;
            elif cp < 0:
                aveEdg += 1;
            elif cp == 0:
                plane += 1;
            
    return (vexEdg, aveEdg, plane)

#############################

class Node: #Object structure
    def __init__ (self, value):
        self.value = value #Tuple of vert indexes in face
    def __str__(self):
        return self.value

#############################
# Union find code:
#############################

def MakeSet(x): #Initialize Tree
     x.parent = x
     x.rank   = 0 

def Union(x, y): #Unite shells
     xRoot = Find(x)
     yRoot = Find(y)
     if xRoot.rank > yRoot.rank:
         yRoot.parent = xRoot
         return 1
     elif xRoot.rank < yRoot.rank:
         xRoot.parent = yRoot
         return 1            
     elif xRoot != yRoot: # Unless x and y are already in same set, merge them
         yRoot.parent = xRoot
         xRoot.rank = xRoot.rank + 1
         return 1 
     return 0 #No new unions.

def Find(x): #Find parent
     if x.parent == x:
        return x
     else:
        x.parent = Find(x.parent)
        return x.parent

#############################
# Source:
# http://code.activestate.com/recipes/215912-union-find-data-structure/    
#############################

#Ex5
def findShells(obj):
    n = 0 #Number of unions
    nPolys = len(obj.data.polygons) 
    polys = [()] * len(obj.data.polygons)        
    for i in range(len(polys)): #Initialize object array.
        polys[i] = Node(obj.data.polygons[i].vertices[:])
    for i in range(len(polys)):
        MakeSet(polys[i]) #initialize set of faces (vert indexes).  
    for p in range (nPolys):
        for q in range (nPolys):
            if p != q: #Dont compare with itself.
                A = polys[p]
                B = polys[q]
                if Find(A) == Find(B): #Unite if parents are the same.
                    n += Union (A, B)
                else:
                    n += polyLoop(A, B, n) #********                                                            
    return nPolys - n #Return starting no of sets - unions = number of subsets.

def polyLoop(A, B, n): #********
    for i in range (len(A.value)): #Union if share same vert.
        for j in range (len(B.value)):
            if A.value[i] == B.value[j]:
                return Union (A, B) #Stop compaing after first match. Return 1 if union happened.
    return 0 #No new unions.
                            
############################




#Ex6    
def eulerForm(obj, S):
    #F + V = E + R + 2(S - G)
    #g = e+r-f-v/2 +s
    R = 0
    V = len(obj.data.vertices)
    E = len(obj.data.edges)
    F = len(obj.data.polygons)
    G = (E + R - F - V)/2 + S
    return G

#Ex7
def area(obj):
    area = 0
    polys = obj.data.polygons
    
    for i in range(len(polys)):
        area += polys[i].area

    return area

#Ex8
#Vol = 1/3 sx (v1x + v2x + v3x) dS
#sx/area = normal

def vol(obj):
    vol = 0
    for i in range (len(obj.data.polygons)): #for each poly:
        nVerts = len(obj.data.polygons[i].vertices) #Amount of verts in this poly
        vertsX = [()] * nVerts #Verts X array
        sx = obj.data.polygons[i].area * obj.data.polygons[i].normal[0] #Calculate poly's sx
        for j in range (nVerts): #For all verts in this poly
            vertInd = obj.data.polygons[i].vertices[j]
            vertsX[j] = obj.data.vertices[vertInd].co[0]  #Add x of each vert to array
        vol +=  sx * (sum(vertsX))/nVerts   
    return vol
    
        
        
#Round
def r(a):
    return int(a*1000+0.5)/1000.0
   

#Main:
def Main():
    curMesh = bpy.data.scenes['Scene'].objects.active
    print('Current OBJ: ' + curMesh.name)
    
    print('\n EX.1)')
    print('Centroid: ', compCentroid(curMesh))
    
    print('\n EX.2)')
    vVar = compVertVar(curMesh)
    print('Max Valence: ', vVar[0])
    print('Min Valence: ', vVar[1])
    print('Average Valence: ', r(vVar[2]))
    compVertVar(curMesh)
    
    print('\n EX.3)')
    edgeData = countManifold(compFaceEdges(curMesh))
    print('Manifold Edges: ', edgeData[0])
    print('Border Edges: ', edgeData[1])
    print('Non-manifold Edges: ', edgeData[2])
    
    print('\n EX.4)')
    faceEdgeData = compFaceEdges(curMesh)
    print('Concave Edge: ', concaveConvex(curMesh, faceEdgeData)[0])
    print('Convex Edge: ', concaveConvex(curMesh, faceEdgeData)[1])
    print('Planar Edge: ', concaveConvex(curMesh, faceEdgeData )[2])
    
    print('\n EX.5)')
    print('Shells/ Union finding')
    print('Shells: ', findShells(curMesh))
    
    print('\n EX.6)')
    print('Formula: V - E + F = 2 - 2 (S - G)')
    S = findShells(curMesh)
    print('Genus: ', eulerForm(curMesh, S))
    
    print('\n EX.7)')
    print('Surface area:', area(curMesh))
    
    print('\n EX.8)')
    print('Total volume:', vol(curMesh))
    
####################

Main()