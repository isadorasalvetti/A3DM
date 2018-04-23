'''.
Exercises Lab3
Isadora Salvett
April 14
.'''

import bpy
import mathutils

########
#Utils
########

#Create F:E data
def compFaceEdges(obj): #(Faces adjacent to each edge)
    nEdgs = len(obj.data.edges)
    nFcs = len(obj.data.polygons)    
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

def compEdgesFace(obj): #(Edges inside face)
    nEdgs = len(obj.data.edges)
    nFcs = len(obj.data.polygons)
    fcEdgeList = [()] * nFcs 
    for i in range (nFcs):
        fc = obj.data.polygons[i].vertices[:]
        curList =[()] * len(fc)
        for j in range(nEdgs):
            edg = obj.data.edges[j].vertices[:]
            if (edg[0] in fc):
                if (edg[1] in fc):
                    v1 = fc.index(edg[0])
                    v2 = fc.index(edg[1])
                    if (v1 - v2 == len(fc) - 1) or (v2 - v1 == len(fc) - 1):
                        index = len(fc) -1
                    else:
                        index = min(v1, v2)
                    curList[index] = j
        fcEdgeList[i] = curList
        printOnce = 0
    return fcEdgeList                     

#Ex1 - Simple Subdivision Catmull–Clark
#New points: Baricenter for each face / mid point of each edge
def SubDivSimp(obj):
    verts = obj.data.vertices
    edgs = obj.data.edges
    faces = obj.data.polygons
    edgeFaceData = compEdgesFace(obj)
    plzNoCrash = [(0,0,0)]*20
    
    oldVert = []
    newVertF = []
    newVertE = []
    
    newFacesList = []
    
    for v in verts:
        oldVert = oldVert + [(v.co)]
      
    #For each face: add midpoint
    count = 0
    for e in edgs:
        V1 = verts[e.vertices[0]].co #edge vertices
        V2 = verts[e.vertices[1]].co
        count +=1
        x = (V1[0] + V2[0])/2
        y = (V1[1] + V2[1])/2
        z = (V1[2] + V2[2])/2
        newVertE = newVertE + [(x, y, z)]

    #For each face: add baricenter and rearrange indices
    faceCount = 0
    for f in faces:
      x, y, z = 0, 0, 0
      fVerts = f.vertices[:] #list of verts in a face (index)
      vertCount = 0
      for v in fVerts: 
        vert = verts[v].co
        x += vert[0]/len(fVerts)
        y += vert[1]/len(fVerts)
        z += vert[2]/len(fVerts)
        # Compute also ne face indices. New faces for face F: A, B, C, D:
        # 1) 0, mid 0, center F, mid 3
        # 2) 1, mid 1, center F, mid 0 (...)
        # v = current vert of the face, aEdg = edge starting at v, f = mid face vert id, dEdge = edge ending at v.
        f1 = faceCount + len(edgs) + len(oldVert)
        aEdge = edgeFaceData[faceCount][vertCount] + len(oldVert) #Edge 0
        if (count - 1 >= 0):
            bEdge = edgeFaceData[faceCount][vertCount-1] + len(oldVert) #Edge -1
        else:
            bEdge = edgeFaceData[faceCount][len(fVerts)-1] + len(oldVert)
        newFace = (v, aEdge, f1, bEdge)
        newFacesList = newFacesList + [newFace]
        vertCount += 1
      newVertF = newVertF + [(x, y, z)] #same index as the faces
      faceCount +=1
 
    coords = oldVert + newVertE + newVertF + plzNoCrash #(OLDverts, EDGEverts, FACEverts)
    print(len(oldVert))
    print(len(newVertE))
    print(0 + len(edgs) + len(faces))
    print(len(newVertF))
    print(newFacesList)
    
    me = bpy.data.meshes.new("NewMesh") #Create new mesh
    ob = bpy.data.objects.new("NewObj", me) #Create an object with that mesh
    ob.location = bpy.context.scene.cursor_location #Position object
    bpy.context.scene.objects.link(ob) #Link object to scene
    
    me.from_pydata(coords,[],newFacesList)
    me.update(calc_edges=True)

def CatClarkDiv():    
    for e in edgs:
        V1 = verts[e.vertices[0]].co #edge vertices
        V2 = verts[e.vertices[1]].co
        V3 = newVertF[faceEdgData[count][0]]
        V4 = newVertF[faceEdgData[count][1]]
        count +=1
        x = (V1[0] + V2[0] + V3[0] + V4[0])/4
        y = (V1[1] + V2[1] + V3[1] + V4[1])/4
        z = (V1[2] + V2[2] + V3[2] + V4[2])/4
        newVertE = newVertE + [(x, y, z)]

#Main:
def Main():
    curMesh = bpy.data.scenes['Scene'].objects.active
    print('Current OBJ: ' + curMesh.name)
    
    print('\n Ex1: ')
    print('Current OBJ: ' + curMesh.name)
    SubDivSimp(curMesh)
    
    
####################

Main()
