import numpy as np
import geopandas as gpd
from shapely.geometry import box
from rasterio.features import rasterize
import osmnx as ox
from affine import Affine

def add_road_mask_from_osm(img_tensor, bounding_box_coords, crs="EPSG:2180", transform=None):
    """
    Adds a road mask to an image tensor using OpenStreetMap data.

    Args:
        img_tensor (np.ndarray): The input RGB image tensor of shape (3, H, W).
        bounding_box_coords (tuple): Bounding box as (min_x, min_y, max_x, max_y).
        crs (str, optional): Coordinate reference system (CRS) of the image. Default is "EPSG:2180" (Poland).
        transform (Affine, optional): Affine transformation for the image.

    Returns:
        np.ndarray: The RGB image tensor with roads masked in the blue channel.
    """
    # Define the bounding box geometry
    min_x, min_y, max_x, max_y = bounding_box_coords
    bbox = box(min_x, min_y, max_x, max_y)

    # Fetch road data from OpenStreetMap
    road_data = ox.geometries_from_bbox(
        north=max_y, south=min_y, east=max_x, west=min_x,
        tags={'highway': True}  # Filter for road geometries
    )
    
    # Keep only line geometries (roads)
    road_data = road_data[road_data.geometry.type == 'LineString']

    # Convert to GeoDataFrame with the image CRS
    road_gdf = gpd.GeoDataFrame(geometry=road_data.geometry, crs="EPSG:4326")

    # Reproject road data to match the image CRS
    if road_gdf.crs != crs:
        road_gdf = road_gdf.to_crs(crs)

    # Rasterize the road geometries
    height, width = img_tensor.shape[1:]  # H, W from tensor shape


    road_mask = rasterize(
        [(geometry, 1) for geometry in road_gdf.geometry],
        out_shape=(height, width),
        transform=transform,
        fill=0,
        dtype="uint8"
    )

    # Overlay the road mask on the blue channel
    masked_image = np.copy(img_tensor)
    masked_image[2] = np.where(road_mask == 1, 255, img_tensor[2])  # Modify Blue Channel

    return masked_image
