from sentinelhub import (
    SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, MimeType, bbox_to_dimensions
)
import numpy as np
import matplotlib.pyplot as plt
import getpass


config = SHConfig()

config.sh_client_id = "sh-c555bef3-b4a2-471a-a6c5-d84bb8b3a53a"
config.sh_client_secret = "pfnK8ZC1MRtNaugZFKAbMN6V6du5WZGX"
config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
config.sh_base_url = "1RcDi6OBwY8dRXWquPL96ULSrcIuQFIc"

def download_and_compute_soil_moisture(aoi, time_interval, resolution=10):
    """
    Downloads Sentinel-1 data for the given AOI and computes soil moisture indicator.

    :param aoi: List of coordinates [min_lon, min_lat, max_lon, max_lat]
    :param time_interval: Time range for the data (e.g., "2024-01-01", "2024-12-31")
    :param resolution: Resolution in meters (default is 10m)
    :return: Soil moisture indicator matrix
    """
    bbox = BBox(bbox=aoi, crs=CRS.WGS84)
    bbox_size = bbox_to_dimensions(bbox, resolution=resolution)
    
    
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
                data_collection=DataCollection.SENTINEL1_IW,
                time_interval=time_interval
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=bbox,
        size=bbox_size,
        config=config
    )
    response = request.get_data()[0]


    vv_band = response[:, :, 0]
    vh_band = response[:, :, 1]


    max_vv = np.max(vv_band)
    min_vv = np.min(vv_band)
    sensitivity = max_vv - min_vv

    soil_moisture = (vv_band - min_vv) / sensitivity
    soil_moisture = np.clip(soil_moisture, 0, 1)  

    return soil_moisture


aoi = [73.85, 18.45, 73.95, 18.55]  
time_interval = ("2024-01-01", "2024-12-31")

soil_moisture = download_and_compute_soil_moisture(aoi, time_interval)

plt.imshow(soil_moisture, cmap="viridis")
plt.colorbar(label="Soil Moisture Indicator")
plt.title("Soil Moisture Map")
plt.show()
