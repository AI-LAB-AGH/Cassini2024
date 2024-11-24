from sentinelhub import (
    SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, MimeType, bbox_to_dimensions
)
import numpy as np
import matplotlib.pyplot as plt
import getpass
from datetime import datetime, timedelta


def download_and_compute_soil_moisture(aoi, resolution=10):
    """
    Downloads Sentinel-1 data for the given AOI and computes soil moisture indicator.

    :param aoi: List of coordinates [min_lon, min_lat, max_lon, max_lat]
    :param time_interval: Time range for the data (e.g., "2024-01-01", "2024-12-31")
    :param resolution: Resolution in meters (default is 10m)
    :return: Soil moisture indicator matrix
    """
    bbox = BBox(bbox=aoi, crs=CRS.WGS84)
    bbox_size = bbox_to_dimensions(bbox, resolution=resolution)


    config = SHConfig()
    config.sh_client_id = "sh-87bb9deb-0438-41ad-b0c4-e2ad6bc95821"
    config.sh_client_secret = "FpgoisOekNjml6OY6dktA9jxkmvVMWKD"
    config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    config.sh_base_url = "https://sh.dataspace.copernicus.eu"
    config.save("cdse")
    
    today = datetime.today()
    month_ago = today - timedelta(days=30)
    time_interval = (month_ago.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))

    
    evalscript = """
    //VERSION=3
    function setup() {
        return {
            input: ["VV", "VH"],
            output: { bands: 2 }
        };
    }
    
    function evaluatePixel(sample) {
        return [sample.VV, sample.VH];
    }
    """
    request = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL1.define_from(
    "s1_vv_vh",
    bands=("VV", "VH"),  
    service_url=config.sh_base_url
),
                time_interval=time_interval
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=bbox,
        size=bbox_size,
        config=config
    )
    response = request.get_data()[-1]


    vv_band = response[:, :, 0]
    vh_band = response[:, :, 1]


    max_vv = np.max(vv_band)
    min_vv = np.min(vv_band)
    sensitivity = max_vv - min_vv

    soil_moisture = (vv_band - min_vv) / sensitivity
    soil_moisture = np.clip(soil_moisture, 0, 1)  

    return soil_moisture

def get_soil_moisture_at_coordinates(soil_moisture_matrix, aoi, coordinates, resolution=10):
    """
    Retrieves soil moisture value at specific coordinates.

    :param soil_moisture_matrix: 2D numpy array of soil moisture values
    :param aoi: List of coordinates [min_lon, min_lat, max_lon, max_lat]
    :param coordinates: List of tuples [(lon1, lat1), (lon2, lat2), ...]
    :param resolution: Resolution in meters (default is 10m)
    :return: Dictionary with coordinates as keys and soil moisture as values
    """
    min_lon, min_lat, max_lon, max_lat = aoi
    num_rows, num_cols = soil_moisture_matrix.shape

    lon_res = (max_lon - min_lon) / num_cols
    lat_res = (max_lat - min_lat) / num_rows

    lat, lon = coordinates
    
    results = {}
    if not (min_lon <= lon <= max_lon and min_lat <= lat <= max_lat):
        results[(lon, lat)] = None
        
        
    col = int((lon - min_lon) / lon_res)
    row = int((max_lat - lat) / lat_res)

    try:
        return soil_moisture_matrix[row, col]
    except IndexError:
        return soil_moisture_matrix[-1, -1]
    

"""
aoi = [73.80, 18.40, 73.90, 18.50]
soil_moisture = download_and_compute_soil_moisture(aoi)
print(get_soil_moisture_at_coordinates(soil_moisture, aoi, [(73.85, 18.45)]))
aoi = [73.85, 18.46, 73.86, 18.47]  #west, south, east, north
soil_moisture = download_and_compute_soil_moisture(aoi)
print(soil_moisture)
plt.imshow(soil_moisture, cmap="viridis")
plt.colorbar(label="Soil Moisture Indicator")
plt.title("Soil Moisture Map")
plt.show()"""