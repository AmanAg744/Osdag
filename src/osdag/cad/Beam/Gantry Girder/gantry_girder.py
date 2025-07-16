from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_Trsf, gp_Ax1
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Display.SimpleGui import init_display
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Aspect import Aspect_GFM_VER  # Import the correct gradient mode
from cad.items.ISection import ISectionsection
from cad.items.channel import Channel

def create_gantry_girder(length, 
                        i_flange_thickness, i_web_thickness, i_width, i_depth,
                        c_flange_thickness, c_web_thickness, c_width, c_depth):
    
    # Create I-section
    i_section = create_i_section(length, i_width, i_depth, i_flange_thickness, i_web_thickness)
    
    # Create C-section
    c_section = create_c_section(length, c_width, c_depth, c_flange_thickness, c_web_thickness)
    
    # Rotate the C-section 90 degrees about its length (X-axis)
    rotation_axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0))  # Corrected: using gp_Pnt and gp_Dir
    rotation = gp_Trsf()
    rotation.SetRotation(rotation_axis, 3.14159/2)  # 90 degrees in radians (pi/2)
    rotated_c_section = BRepBuilderAPI_Transform(c_section, rotation, True).Shape()
    
    # Position the rotated C-section on top of the I-section
   
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(0, i_width/2+c_depth/2, ( i_depth-c_width+c_web_thickness)))
    transformed_c_section = BRepBuilderAPI_Transform(rotated_c_section, trsf, True).Shape()
    
    # Combine the sections
    girder = BRepAlgoAPI_Fuse(i_section, transformed_c_section).Shape()
    
    return girder

if __name__ == "__main__":
    length = 1500.0
    
    # I-section parameters
    i_width = 150.0
    i_depth = 300.0
    i_flange_thickness = 15.0
    i_web_thickness = 10.0
    
    # C-section parameters
    c_width = 50.0
    c_depth = 220.0
    c_flange_thickness = 15.0
    c_web_thickness = 10.0

    gantry_girder = create_gantry_girder(length, 
                                       i_flange_thickness, i_web_thickness, i_width, i_depth,
                                       c_flange_thickness, c_web_thickness, c_width, c_depth)

    # Visualization
    display, start_display, add_menu, add_function_to_menu = init_display()
    
    top_color = Quantity_Color(0.27, 0.27, 0.44, Quantity_TOC_RGB)  # Dark blue (#444470)
    bottom_color = Quantity_Color(0.67, 0.67, 0.67, Quantity_TOC_RGB)  # Light gray (#AAAAAA)
    # Set the gradient background (top-to-bottom)
    display.View.SetBgGradientColors(top_color, bottom_color, Aspect_GFM_VER, True)
    redd=Quantity_Color(1, 0, 0, Quantity_TOC_RGB) 

    # Show the gantry girder model
    display.DisplayShape(gantry_girder, update=True)
    display.FitAll()
    start_display()