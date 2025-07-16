import math
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.gp import gp_Pnt


def hexagon(center, hex_v, hex_h):
    polygon = BRepBuilderAPI_MakePolygon()
    for i in range(6):
        angle = math.radians(i * 60)
        y = center.Y() + (hex_h / 2) * math.cos(angle)
        z = center.Z() + (hex_v / 2) * math.sin(angle)
        polygon.Add(gp_Pnt(center.X(), y, z))  # Keep X constant
    polygon.Close()
    return polygon.Wire()

if __name__ == '__main__':
    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()
    
    center = gp_Pnt(0, 0, 0) 
    hex_w = 5
    hex_h = 7
    hex_wire = hexagon(center, hex_w, hex_h)

    # Create hexagon face
    hex_face = BRepBuilderAPI_MakeFace(hex_wire).Face()

    # Extrude the face along X-axis
    length = 10
    extrude_vec = gp_Vec(length, 0, 0)
    hex_prism = BRepPrimAPI_MakePrism(hex_face, extrude_vec).Shape()

    display.DisplayShape(hex_prism, update=True)
    start_display()