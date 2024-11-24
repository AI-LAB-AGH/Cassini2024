from get_rgb_from_sentinel import *
from add_road_mask import *
import matplotlib.pyplot as plt
from calculate_mobility import calculate_mobility_at_coordinates
from moisture import *
from soilgrips import *
from fuzzy_system.system import inference


aoi = [18.85, 52.45, 18.86, 52.46]
soil_moisture = download_and_compute_soil_moisture(aoi)
data = get_rgb_from_sentinel("output", aoi)
#masked_data = add_road_mask_from_osm(data, aoi)
def get_coordinates(image, aoi, pixel):
    """
    Get coordinates of some pixel in the image
    """
    x = aoi[0] + pixel[0] * (aoi[2] - aoi[0]) / image.shape[0]
    y = aoi[1] + pixel[1] * (aoi[3] - aoi[1]) / image.shape[1]
    return (x, y)

mobility_parameters = {
    "terrain": 0,
    "vehicle": 0,
    "weight": 22000,
    "speed": 80
}

for x in range(data.shape[0]):
    for y in range(data.shape[1]):
       print(calculate_mobility_at_coordinates(mobility_parameters, get_coordinates(data, aoi, (x, y)), aoi, soil_moisture))


