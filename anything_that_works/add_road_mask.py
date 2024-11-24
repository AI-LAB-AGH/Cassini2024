import numpy as np
import osmnx as ox
import geopandas as gpd
from shapely.geometry import box
from rasterio.features import rasterize

def find_roads_and_generate_mask(img_tensor, bounding_box_coords, tags=None, crs="EPSG:4326"):
    """
    Finds all road geometries within a bounding box using OpenStreetMap data and generates a road mask on an image.

    Args:
        img_tensor (np.ndarray): Input tensor of shape (C, H, W), where C is the number of channels.
        bounding_box_coords (tuple): Bounding box as (min_x, min_y, max_x, max_y) in the specified CRS.
        tags (dict, optional): OSM tags to filter the roads. Default is {"highway": True} to get all road types.
        crs (str, optional): Coordinate reference system (CRS) of the bounding box. Default is "EPSG:4326" (WGS84).

    Returns:
        np.ndarray: A binary road mask of shape (H, W) with roads highlighted.
    """
    if img_tensor.ndim != 3:
        raise ValueError("Input tensor must have 3 dimensions (C, H, W).")
    
    _, H, W = img_tensor.shape 
    
    if tags is None:
        tags = {"highway": True}  

    
    bounding_box = box(*bounding_box_coords)

    
    roads_gdf = ox.features_from_polygon(bounding_box, tags)
    
    
    transform = (
        (bounding_box_coords[2] - bounding_box_coords[0]) / W, 0, bounding_box_coords[0],
        0, -(bounding_box_coords[3] - bounding_box_coords[1]) / H, bounding_box_coords[3]
    )
    shapes = ((geom, 1) for geom in roads_gdf.geometry if geom.is_valid)

    road_mask = rasterize(
        shapes=shapes,
        out_shape=(H, W),
        transform=transform,
        fill=0,
        default_value=1,
        dtype=np.uint8
    )

    return road_mask

# Example usage
#bounding_box = (18.65, 52.25, 18.86, 52.46)  # Bounding box coordinates (min_x, min_y, max_x, max_y)
#img_tensor = np.zeros((3, 256, 256))  # Example image tensor (C, H, W)
#road_mask = find_roads_and_generate_mask(img_tensor, bounding_box)
#print(road_mask)
