from pathlib import Path

import geopandas as gpd
import numpy as np
from shapely import box
from shapely import contains
from shapely import disjoint
from shapely import points


def deposition_coeff_from_land_occupation_data(path_data, file_name_data, land_occupation_to_deposition_coeff, msh):
    """
    read the land occupation data,
    search the land occupation at the cells of the mesh
    and return the associated deposition coefficient map

    - input:
        * paht_data: str, path to the folder that contains the land occupation data
        * file_name_data: str, name of the file that contains the land occupation data
        * land_occupation_to_deposition_coeff: dictionary, contains the deposition coefficient wrt the land occupation
        * msh: object of the class MeshRect2D
    - output:
        * deposition_coeff:
            array of shape (msh.y.size, msh.x.size),
            contains the value of the deposition coefficient at the cells of the mesh
    - TO ADD:
        * take into account the case None
        * exception to check the points are indeed in one of the polygon
        * exception to check the format of the df is as expected
        * exception to check the land occupation data and the dictionary coincide together
    """

    df = gpd.read_file(Path(path_data) / file_name_data)
    # removing the None, the associated points will then be setted to 0
    # better way to do it ?
    for i in df.index:
        if df['CLAS_SCOT'][i] is None:
            df = df.drop(i)

    xm, ym = np.meshgrid(msh.x, msh.y)
    geoms = points(xm, ym)
    msh_box = box(np.min(msh.x), np.min(msh.y), np.max(msh.x), np.max(msh.y))

    deposition_coeff = np.zeros((msh.y.size, msh.x.size), dtype=float)
    for polygon, land_occupation in zip(df['geometry'], df['CLAS_SCOT']):
        if land_occupation not in land_occupation_to_deposition_coeff.keys():
            raise ValueError(
                "The land occupation classification "
                + str(land_occupation)
                + "is not found in the dictionary containing the deposition coefficient with respect to the land occupation"
            )
        if not disjoint(msh_box, polygon):
            deposition_coeff[contains(polygon, geoms)] = land_occupation_to_deposition_coeff[str(land_occupation)]
    return deposition_coeff
