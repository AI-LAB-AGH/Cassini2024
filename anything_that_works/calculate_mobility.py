from fuzzy_system.system import inference
import pandas as pd
from moisture import *
from soilgrips import *

def calculate_mobility_at_coordinates(mobility_parameters, coordinates, aoi, soil_moisture):
    """
    Calculate mobility at specific coordinates.
    """
    moisture = get_soil_moisture_at_coordinates(soil_moisture, aoi, coordinates)
    print("dupa")
    soil_properties = get_soil_properties(coordinates) # BOTTLENEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEECK
    print("dupa")
    sand = soil_properties.loc[soil_properties['property'] == 'sand', 'mean_value_target_unit'].iloc[0]/100
    mobility_score = calculate_mobility(mobility_parameters, sand, moisture)
    print("mobility score at coordinates", coordinates, "is", mobility_score)
    return mobility_score

def calculate_mobility(mobility_parameters, sand, moisture):
    mobility_parameters["terrain"] = calculate_trafficability_metric(sand, moisture)
    mobility_score = inference(mobility_parameters["terrain"], mobility_parameters["vehicle"], 
        mobility_parameters["weight"], mobility_parameters["speed"])
    return mobility_score
    

def calculate_trafficability_metric(sand: float, moisture: float):
    """
    soil_moisture*1.5 - 0 to 3
    soil_texture[sand]*1.5 - 0 to 3
    """
    
    trafficability_metric = sand*2 + moisture*2
    trafficability_metric = max(0, min(3, round(trafficability_metric)))
    print("calculate trafficability", trafficability_metric)
    return trafficability_metric



