#Ex6    
#F + V = E + R + 2(S - G)

def eulerForm(obj, S):
    R = 0
    V = len(obj.data.vertices)
    E = len(obj.data.edges)
    F = len(obj.data.polygons)
    G = (E + R - F - V)/2 + S
    return G

	
#Code from Ex5:
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
