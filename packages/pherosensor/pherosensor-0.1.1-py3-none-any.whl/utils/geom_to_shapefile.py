from pathlib import Path

import geopandas as gpd
import numpy as np
from shapely import box


def geom_to_shapefile(msh, name_file_out, path_out):
    """
    method to save the geometry in a shapefile with the domain as a shapely.box for visualization

    - input:
        * msh: object of the class MeshRect2D, the mesh containing the geometry to save
        * path_out: str, path to the folder in which the geometry will be saved
        * name_file_out: str, name of the file in which the geometry will be saved
    - do:
        * generate a shapely.box corresponding the the domain
        * save the geometry contained in msh and the domain's box in the file and folder given as input
    """
    msh_box = box(np.min(msh.x), np.min(msh.y), np.max(msh.x), np.max(msh.y))
    d_msh = {
        'index': [0],
        'L_x': msh.L_x,
        'L_y': msh.L_y,
        'dx': msh.dx,
        'dy': msh.dy,
        'T final': msh.T_final,
        'x origin': msh.x_vertical_interface[0],
        'y origin': msh.y_horizontal_interface[0],
        'geometry': msh_box,
    }
    df_msh = gpd.GeoDataFrame(d_msh)
    df_msh.to_file(filename=Path(path_out) / name_file_out, driver='ESRI Shapefile')
