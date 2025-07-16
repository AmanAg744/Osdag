import math
import numpy
from OCC.Core.gp import gp_Pnt, gp_Vec,gp_Trsf
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from items.Hexagon_beam import hexagon
from cad.items.ISection import ISection 
from cad.items.notch import Notch
from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()


# Creating I section
B = 40  # width of flanges
T = 3  # flanges sthickness
D = 50 # hright of beam ( falnege thickness +web height)
t = 2  #web thickness
R1 = 5 # notch radius
R2 = 5
alpha = 1
length = 500 # length of beam
width = 10  #notch 
hight = 10  #notch
notchObj = Notch(R1, hight, width, length)

origin = numpy.array([0.,0.,0.])
uDir = numpy.array([1.,0.,0.])
shaftDir = numpy.array([0.,1.,0.])

ISec = ISection(B, T, D, t, R1, R2, alpha, length, notchObj)
place = ISec.place(origin, uDir, shaftDir)
point = ISec.compute_params()
prism = ISec.create_model()


# Define the translation vector (shift by +20 in X and +25 in Z) to keep it in origin
translation_vector = gp_Vec(20, 0, 25)

# Create a transformation
trsf = gp_Trsf()
trsf.SetTranslation(translation_vector)

# Apply the transformation to the prism
translated_prism = BRepBuilderAPI_Transform(prism, trsf, True).Shape()


#display.DisplayShape(translated_prism, update=True)


#creating hexagon pattern:

a=5 # edge gap
b=30 # length of flat horizontal edge 
c=5 # gap between two hexagon
e=3 # distance between flat edge and middle corner
j=5 # gap between flast edge and flange of i section
hex_v = D-2*j  #horizontal length of hexagon
hex_h = 2*e+b  #vertical length of hexagon
tw = 30  # extrtrude cut length

n=round((length-2*b+c)/(2*e+b+c))

# List to hold all hexagonal prisms
hex_prisms = []
# Create 10 hexagons along X-axis
for i in range(n):
    center = gp_Pnt(0,hex_h/2+a + i * (hex_h+c), D/2)  # shift X each time
    hex_wire = hexagon(center, hex_v, hex_h)
    hex_face = BRepBuilderAPI_MakeFace(hex_wire).Face()
    extrude_vec = gp_Vec(tw, 0, 0)
    hex_prism = BRepPrimAPI_MakePrism(hex_face, extrude_vec).Shape()
    hex_prisms.append(hex_prism)

# Display all prisms
#for prism in hex_prisms:
#    display.DisplayShape(prism, update=False)
    
#extrude cutting
beam=translated_prism
for cutter in hex_prisms:
    beam = BRepAlgoAPI_Cut(beam, cutter).Shape()

display.DisplayShape(beam, update=True)

display.FitAll()
start_display()
