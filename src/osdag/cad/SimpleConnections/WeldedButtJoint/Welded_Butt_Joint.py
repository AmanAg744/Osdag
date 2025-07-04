import numpy
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.Quantity import Quantity_NOC_RED, Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM, Graphic3d_NOM_STEEL
from OCC.Core.gp import gp_Pnt
from ...items.plate import Plate
from ...items.filletweld import FilletWeld  # Import FilletWeld class

def create_welded_butt_joint(plate_width=100, plate1_thickness=10, plate2_thickness=10, cover_thickness=8, weld_size=6, weld_length=80):
    plate_length = 1.5 * plate_width
    weld_length=plate_width
    weld_size=cover_thickness
    # --- Create the first plate ---
    origin1 = numpy.array([0.0, 0.0, 0.0])
    uDir1 = numpy.array([0.0, 0.0, 1.0])  # X direction
    wDir1 = numpy.array([1.0, 0.0, 0.0])  # Z direction

    plate1 = Plate(plate_length, plate_width, plate1_thickness)
    plate1.place(origin1, uDir1, wDir1)
    plate1_model = plate1.create_model() 

    # --- Create the second plate ---
    origin2 = numpy.array([0.0, plate_length, 0.0])
    uDir2 = numpy.array([0.0, 0.0, 1.0])
    wDir2 = numpy.array([1.0, 0.0, 0.0])

    plate2 = Plate(plate_length, plate_width, plate2_thickness)
    plate2.place(origin2, uDir2, wDir2)
    plate2_model = plate2.create_model()

    # --- Create the cover plate ---
    origin3 = numpy.array([0.0, plate_length/ 2, max(plate1_thickness, plate2_thickness)/2+cover_thickness/2])
    uDir3 = numpy.array([0.0, 0.0, 1.0])
    wDir3 = numpy.array([1.0, 0.0, 0.0])

    cover_plate = Plate(plate_length, plate_width, cover_thickness)
    #cover_plate_center_origin = origin3 + numpy.array([0, plate_length / 2, cover_thickness / 2])
    cover_plate.place(origin3, uDir3, wDir3)
    cover_plate_model = cover_plate.create_model()

    # --- Create the Fillet Welds ---
    welds_models = []

    weld_b = weld_size
    weld_h = weld_size

    # Corrected weld placement for each butt interface
    weld_origins = [
        numpy.array([(plate_width - weld_length) / 2, 0, max(plate1_thickness, plate2_thickness)/2]),  # Left weld
        numpy.array([(plate_width - weld_length) / 2, plate_length, max(plate1_thickness, plate2_thickness)/2])  # Right weld
    ]

    weld_dirs = [
        {'uDir': numpy.array([0.0, 0.0, 1.0]), 'shaftDir': numpy.array([1.0, 0.0, 0.0])},   # Upward facing weld
        {'uDir': numpy.array([0.0, 1.0, 0.0]), 'shaftDir': numpy.array([1.0, 0.0, 0.0])}   # Downward facing weld
    ]

    for i, origin in enumerate(weld_origins):
        weld = FilletWeld(weld_b, weld_h, weld_length)
        weld.place(origin, weld_dirs[i]['uDir'], weld_dirs[i]['shaftDir'])
        weld_model = weld.create_model()
        welds_models.append(weld_model)

    return plate1_model, plate2_model, cover_plate_model, welds_models

# =============================================================================
if __name__ == "__main__":
    plate1, plate2, cover_plate, welds = create_welded_butt_joint(
        plate_width=120,
        plate1_thickness=12,
        plate2_thickness=12,
        cover_thickness=10,
        weld_size=8,
        weld_length=100
    )

    # Initialize 3D viewer
    display, start_display, add_menu, add_function_to_menu = init_display()

    weld_color = Quantity_Color(0.8, 0.1, 0.1, Quantity_TOC_RGB)

    # Display all parts
    display.DisplayShape(plate1, update=True, color='silver')
    display.DisplayShape(plate2, update=True, material=Graphic3d_NOM_ALUMINIUM)
    display.DisplayShape(cover_plate, update=True, material=Graphic3d_NOM_STEEL)

    for weld_model in welds:
        display.DisplayShape(weld_model, color=weld_color, update=True)

    # Mark origin
    origin_marker = BRepPrimAPI_MakeSphere(gp_Pnt(0, 0, 0), 1.5).Shape()
    display.DisplayShape(origin_marker, color=Quantity_NOC_RED, update=True)

    display.set_bg_gradient_color([20, 20, 50], [150, 150, 170])
    display.DisableAntiAliasing()
    display.FitAll()
    start_display()
