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

def faceNedgesByVert(vertCount, faces, edges): #(Faces and edges adjacent to vert)
    facesPerVert = [()] * vertCount
    edgesPerVert = [()] * vertCount
    for vIndex in range(vertCount):
        eIndex = 0
        fIndex = 0
        for eIndex, e in enumerate(edges):
            if (vIndex in e.vertices[:]):
                edgesPerVert[vIndex] = edgesPerVert[vIndex] + (eIndex, )
        for fIndex, f in enumerate(faces):
            if (vIndex in f.vertices[:]):
                facesPerVert[vIndex] = facesPerVert[vIndex] + (fIndex, )
    return facesPerVert, edgesPerVert                   

#Ex1 - Simple Subdivision Catmull–Clark
#New points: Baricenter for each face / mid point of each edge
def SubDivSimp(obj):
    verts = obj.data.vertices
    edgs = obj.data.edges
    faces = obj.data.polygons
    
    oldVert = []
    newVertF = []
    newVertE = []
    
    newFacesList = []
    
    for v in verts:
        oldVert = oldVert + [(v.co)]
      
    #For each face: add midpoint
    for count, e in enumerate(edgs):
        V1 = verts[e.vertices[0]].co #edge vertices
        V2 = verts[e.vertices[1]].co
        count +=1
        x = (V1[0] + V2[0])/2
        y = (V1[1] + V2[1])/2
        z = (V1[2] + V2[2])/2
        newVertE = newVertE + [(x, y, z)]

    edgeFaceData = compEdgesFace(obj) #edges per face
    #For each face: add baricenter and rearrange indices
    for faceCount, f in enumerate(faces):
      x, y, z = 0, 0, 0
      fVerts = f.vertices[:] #list of verts in a face (index)
      for vertCount, v in enumerate(fVerts): 
        vert = verts[v].co
        x += vert[0]/len(fVerts)
        y += vert[1]/len(fVerts)
        z += vert[2]/len(fVerts)
        # Compute also ne face indices. New faces for face F: A, B, C, D:
        # 1) 0, mid 0, center F, mid 3
        # 2) 1, mid 1, center F, mid 0 (...)
        # v = current vert of the face, aEdg = edge starting at v, f = mid face vert id, dEdge = edge ending at v.
        f1 = faceCount + len(edgs) + len(verts)
        aEdge = edgeFaceData[faceCount][vertCount] + len(verts) #Edge 0
        if (vertCount - 1 >= 0):
            bEdge = edgeFaceData[faceCount][vertCount-1] + len(verts) #Edge -1
        else:
            bEdge = edgeFaceData[faceCount][len(fVerts)-1] + len(verts)
        newFace = (v, aEdge, f1, bEdge)
        newFacesList = newFacesList + [newFace]
      newVertF = newVertF + [(x, y, z)] #same index as the faces
 
    coords = oldVert + newVertE + newVertF #(OLDverts, EDGEverts, FACEverts)    
    return coords, newFacesList           

#Ex2 - Catmull–Clark
#New points: Baricenter for each face / mid point of each edge
def CatmullClarkDiv(obj):
    verts = obj.data.vertices
    edgs = obj.data.edges
    faces = obj.data.polygons
    
    oldVert = []
    newVertF = []
    newVertE = []
    midpointE = []
    
    newFacesList = []

    #For each face: add baricenter
    for faceCount, f in enumerate(faces):
      x, y, z = 0, 0, 0
      fVerts = f.vertices[:] #list of verts in a face (index)
      for vertCount, v in enumerate(fVerts): #Loop through face verts
        vert = verts[v].co
        x += vert[0]/len(fVerts)
        y += vert[1]/len(fVerts)
        z += vert[2]/len(fVerts)
      newVertF = newVertF + [(x, y, z)] #same index as the faces
 
    faceEdgAdj = compFaceEdges(obj) #edges per face
    #For each edge: calculate new edge verts    
    for eCount, e in enumerate(edgs):
        eFaces = faceEdgAdj[eCount] #faces adjacent to this edge
        V1 = verts[e.vertices[0]].co #edge vertices
        V2 = verts[e.vertices[1]].co
        V3 = newVertF[eFaces[0]] #face verts from adjacent faces
        V4 = newVertF[eFaces[1]]
        x = (V1[0] + V2[0] + V3[0] + V4[0])/4
        y = (V1[1] + V2[1] + V3[1] + V4[1])/4
        z = (V1[2] + V2[2] + V3[2] + V4[2])/4
        newVertE = newVertE + [(x, y, z)]
        
    #For each face: add midpoint
    for count, e in enumerate(edgs):
        V1 = verts[e.vertices[0]].co #edge vertices
        V2 = verts[e.vertices[1]].co
        count +=1
        x = (V1[0] + V2[0])/2
        y = (V1[1] + V2[1])/2
        z = (V1[2] + V2[2])/2
        midpointE = midpointE + [(x, y, z)] 
           
    edgeFaceData = compEdgesFace(obj)        
    #For each face: rearrange indices
    for faceCount, f in enumerate(faces):
      fVerts = f.vertices[:] #list of verts in a face (index)
      for vertCount, v in enumerate(fVerts): #Loop through face verts
        # Compute also the face indices. New faces for face F: A, B, C, D:
        # 1) 0, mid 0, center F, mid 3
        # 2) 1, mid 1, center F, mid 0 (...)
        # v = current vert of the face, aEdg = edge starting at v, f = mid face vert id, dEdge = edge ending at v.
        f1 = faceCount + len(edgs) + len(verts)
        aEdge = edgeFaceData[faceCount][vertCount] + len(verts) #Edge 0
        if (vertCount - 1 >= 0):
            bEdge = edgeFaceData[faceCount][vertCount-1] + len(verts) #Edge -1
        else:
            bEdge = edgeFaceData[faceCount][len(fVerts)-1] + len(verts)
        newFace = (v, aEdge, f1, bEdge)
        newFacesList = newFacesList + [newFace]
    
    FEv = faceNedgesByVert(len(verts), faces, edgs)
    facesPerVert = FEv[0] #Array of indices of faces per vert
    edgesPerVert = FEv[1] #Array of indices of edges per vert
    #For each original vert: calculate new position
    for vIndex, v in enumerate(verts):
        #Average of new verts on all faces touching P, 
        #average of all midpoints on edges touching P (not new Edge points!), 
        #original point / n (weighted)
        xF, yF, zF, xE, yE, zE = 0, 0, 0, 0, 0, 0
        n = len(facesPerVert[vIndex]) #N of faces per vert.
        for vF in facesPerVert[vIndex]: #for each vF face on this vert...
            xF += newVertF[vF][0]/n
            yF += newVertF[vF][1]/n
            zF += newVertF[vF][2]/n
        for vE in edgesPerVert[vIndex]: #for each vE edge on this vert...
            xE += midpointE[vE][0]/n
            yE += midpointE[vE][1]/n
            zE += midpointE[vE][2]/n
        F = (xF, yF, zF) # avrgFaceVerts
        R = (xE, yE, zE) # avrgEdgeVerts
        P = v.co[:] # original Point
        newVert = ((F[0] + 2*R[0] + (n-3)*P[0]) / n, 
                   (F[1] + 2*R[1] + (n-3)*P[1]) / n, 
                   (F[2] + 2*R[2] + (n-3)*P[2]) / n)     
        oldVert = oldVert + [(newVert)]
            
    coords = oldVert + newVertE + newVertF #(OLDverts, EDGEverts, FACEverts)
    return coords, newFacesList

def lerpOBJ(vertsSimp, vertsCC, param):
    # interpolate verts coordinates. Face indices will remain the same.
    interpCoords = []
    if (len(vertsSimp) != len(vertsCC)):
        print ("Lerp received incorrect data.")
        return
    for i in range (len(vertsSimp)):
        #value = (C * A) + ((1-C) * B)
        X = (param * vertsSimp[i][0]) + ((1-param) * vertsCC[i][0])
        Y = (param * vertsSimp[i][1]) + ((1-param) * vertsCC[i][1])
        Z = (param * vertsSimp[i][2]) + ((1-param) * vertsCC[i][2])
        interpCoords = interpCoords + [(X, Y, Z)]
    return interpCoords

def createObj(data):
    #data[0] = COORDS, data[1] = FACES
    me = bpy.data.meshes.new("NewMesh") #Create new mesh
    ob = bpy.data.objects.new("NewObj", me) #Create an object with that mesh
    ob.location = bpy.context.scene.cursor_location #Position object
    bpy.context.scene.objects.link(ob) #Link object to scene
    
    me.from_pydata(data[0],[],data[1])
    me.update(calc_edges=True)

#Main:
def Main():
    curMesh = bpy.data.scenes['Scene'].objects.active
    print('Current OBJ: ' + curMesh.name)
    
    #Create the subdivided data.
    simpleSubMesh = SubDivSimp(curMesh)
    CCSubMesh = CatmullClarkDiv(curMesh)
    
    #Interpolate the vertices of the meshes
    lerpMesh = (lerpOBJ(simpleSubMesh[0], CCSubMesh[0], 0.5), simpleSubMesh[0])
    createObj(lerpMesh)
    
       
####################

Main()
