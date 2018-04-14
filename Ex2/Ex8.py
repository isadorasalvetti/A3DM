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