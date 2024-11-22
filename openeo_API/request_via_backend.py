import sys
import requests
import json
import openeo

con = openeo.connect("openeo.dataspace.copernicus.eu")
con.authenticate_oidc()

# When connected download datacube of data we are interested in
datacube = con.load_collection(
    "SENTINEL2_L2A", #mission SENTINEL2_L2A
    spatial_extent={"west": 22.603437, "south": 49.130043, "east": 22.625155, "north": 49.137227}, #range (long,lat)  of data
    temporal_extent = ["2024-04-01", "2024-04-09"], #get states from dates between
    bands=["B02","B03", "B04", "B08", "B11"], #choosen bands
    max_cloud_cover=85,
)

# Example joining bands
#red_band = client.load_collection('Sentinel-2', bands=['B4'])
#green_band = client.load_collection('Sentinel-2', bands=['B3'])
#blue_band = client.load_collection('Sentinel-2', bands=['B2'])
#rgb_image = red_band.add(green_band).add(blue_band)



#Where to store file
file='./Datacubes/carynska_before.nc'

datacube.download(file)
print(f'Saved datacube to {file}')
