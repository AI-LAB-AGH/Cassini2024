import openeo
import xarray
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import os


def get_rgb_from_sentinel(output_file, aoi):
    def make_connection():
        con = openeo.connect("openeo.dataspace.copernicus.eu")
        con.authenticate_oidc()
        return con

    def download_datacube(connection, output_file, aoi, chosen_bands = ["B02", "B03", "B04"]):
        today = datetime.today()
        month_ago = today - timedelta(days=30)
        time_interval = (month_ago.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))
        datacube = connection.load_collection(
        "SENTINEL2_L2A",
        spatial_extent={"west": aoi[0], "south": aoi[1], "east": aoi[2], "north": aoi[3]},
        temporal_extent = time_interval,
        bands= chosen_bands,
        max_cloud_cover=10,
    )
        datacube.download(output_file+".nc")

    if not f"{output_file}.nc" in os.listdir():
        connection = make_connection()
        download_datacube(connection, output_file, aoi)
    ds = xarray.load_dataset(f"{output_file}.nc")
    data = ds[["B04", "B03", "B02"]].to_array(dim="bands")
    data = data[:, -1, :, :]
    data = np.squeeze(data)
    return data

