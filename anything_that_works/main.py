from get_rgb_from_sentinel import *
from add_road_mask import *
import matplotlib.pyplot as plt
from calculate_mobility import calculate_mobility_at_coordinates
from moisture import *
from soilgrips import *
from fuzzy_system.system import inference


aoi = [18.80, 52.40, 18.90, 52.50]
soil_moisture = download_and_compute_soil_moisture(aoi)
data = get_rgb_from_sentinel("output_10pix", aoi)
masked_data = find_roads_and_generate_mask(data, aoi)
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

"""
for x in range(data.shape[0]):
    for y in range(data.shape[1]):
       print(calculate_mobility_at_coordinates(mobility_parameters, get_coordinates(data, aoi, (x, y)), aoi, soil_moisture))"""


for i in range(data.shape[1]):
    for j in range(data.shape[2]):
        if masked_data[i][j] == 1:
            data[2][i][j] = 0
            data[1][i][j] = 0
            data[0][i][j] = 0
            mobility = calculate_mobility_at_coordinates(mobility_parameters, get_coordinates(data, aoi, (i, j)), aoi, soil_moisture)
            if mobility > 0.8:
                data[2][i][j] = 2000
            else:
                data[0][i][j] = 2000
            

fig, axes = plt.subplots(ncols=1, dpi=90)
data.plot.imshow(vmin=0, vmax=2000)
axes.set_title("Original Data")

plt.tight_layout()
plt.show()