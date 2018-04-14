'''.
Exercises Lab2
Isadora Salvett
March 14
.'''

import bpy
import mathutils
import sys
import os
import imp

from time import time

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    #print(sys.path)

import Ex6
import Ex8
imp.reload(Ex6)
imp.reload(Ex8)

def r(a):
    return int(a*1000+0.5)/1000.0



#Main:
def Main():
    
    curMesh = bpy.data.scenes['Scene'].objects.active
    
    print('\n EX.6)')
    print('Formula: V - E + F = 2 - 2 (S - G)')
    t = time()
    S = Ex6.findShells(curMesh)
    print('Genus: ', Ex6.eulerForm(curMesh, S))
    print("Script took %6.2f secs.\n\n"%(time()-t))


    print('\n EX.8)')
    t = time()
    volm = Ex8.vol(curMesh)
    print('Total volume:', r(volm))
    print("Script took %6.2f secs.\n\n"%(time()-t))


Main()
