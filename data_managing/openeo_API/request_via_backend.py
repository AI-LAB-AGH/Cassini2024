import sys
import requests
import json
import openeo

con = openeo.connect("openeo.dataspace.copernicus.eu")
con.authenticate_oidc()

# When connected download datacube of data we are interested in
datacube = con.load_collection(
    "SENTINEL2_L2A", #mission SENTINEL2_L2A
    spatial_extent={"west": 38.36391, "south": 47.90318, "east": 38.43927, "north": 47.94676}, #range (long,lat)  of data
    temporal_extent = ["2023-05-03", "2024-05-03"], #get states from dates between
    bands=["B08", "B11"], #choosen bands
    max_cloud_cover=85,
)

# Example joining bands
#red_band = client.load_collection('Sentinel-2', bands=['B4'])
#green_band = client.load_collection('Sentinel-2', bands=['B3'])
#blue_band = client.load_collection('Sentinel-2', bands=['B2'])
#rgb_image = red.add(green).add(blue)

ndmi_cube = (datacube.band("B08") - datacube.band("B11")) / (datacube.band("B08A") + datacube.band("B11"))

#Where to store file
file1 ='./PNGs/ukraine_ndmi_8_112.png'
file2 ='./Datacubes/ukraine_ndmi_8_112.nc'

ndmi_cube.download(file1)
ndmi_cube.download(file2)

print(f'Saved datacube to {file1}')
print(f'Saved datacube to {file2}')