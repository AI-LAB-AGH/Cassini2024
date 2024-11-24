import requests
import pandas as pd



   
def fetch_data(coordinates):
     return requests.get(f"https://rest.isric.org/soilgrids/v2.0/properties/query?lon={coordinates[0]}&lat={coordinates[1]}&property=bdod&property=cec&property=cfvo&property=clay&property=nitrogen&property=ocd&property=ocs&property=phh2o&property=sand&property=silt&property=soc&property=wv0010&property=wv0033&property=wv1500&depth=0-5cm&depth=5-15cm&depth=15-30cm&value=mean&value=uncertainty").json()

def get_soil_properties(coordinates: tuple[float, float]) -> pd.DataFrame:
    """
    Fetches and processes soil property data for a given geographic location.

    This function retrieves soil property information for specified coordinates,
    processes the data, and returns it as a pandas DataFrame. It calculates
    the mean values and uncertainties for each soil property across all
    specified depth layers, converting the measurements into both mapped and
    target units.

    Parameters:
    ----------
    coordinates : tuple[float, float]
        A tuple containing the longitude and latitude of the location 
        (longitude, latitude).

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing the following columns:
        - latitude: Latitude of the location.
        - longitude: Longitude of the location.
        - property: Name of the soil property (e.g., "bdod", "cec").
        - mapped_unit: Original unit of measurement for the soil property.
        - mean_value_mapped_unit: Average value of the property across depths in the mapped unit.
        - mean_uncertainty_mapped_unit: Average uncertainty across depths in the mapped unit.
        - target_unit: Converted unit of measurement for the soil property.
        - mean_value_target_unit: Average value of the property in the target unit.
        - mean_uncertainty_target_unit: Average uncertainty in the target unit.

    Soil Properties Description:
    ----------------------------
    Below is a detailed description of the soil properties:

    1. **bdod** (Bulk Density of the Oven-Dried Soil):
        - **Description**: Bulk density refers to the mass of soil per unit volume, including the air space.
        - **Mapped Unit**: `cg/cm³` (centigrams per cubic centimeter).
        - **Target Unit**: `kg/dm³` (kilograms per cubic decimeter).
        - **Importance**: Indicates soil compaction, which can affect root penetration and water movement.

    2. **cec** (Cation Exchange Capacity):
        - **Description**: Measures the soil's ability to retain and exchange positively charged ions (cations) such as potassium, calcium, and magnesium.
        - **Mapped Unit**: `mmol(c)/kg` (millimoles of charge per kilogram of soil).
        - **Target Unit**: `cmol(c)/kg` (centimoles of charge per kilogram of soil).
        - **Importance**: High CEC indicates fertile soil with a good capacity to retain essential nutrients.

    3. **cfvo** (Coarse Fragments Volume):
        - **Description**: Proportion of the soil volume occupied by particles larger than 2mm (e.g., gravel, stones).
        - **Mapped Unit**: `cm³/dm³` (cubic centimeters per cubic decimeter).
        - **Target Unit**: `cm³/100cm³` (percentage by volume).
        - **Importance**: High CFVO values can hinder root growth and water retention.

    4. **clay**:
        - **Description**: Percentage of soil particles smaller than 0.002 mm in diameter.
        - **Mapped Unit**: `g/kg` (grams per kilogram).
        - **Target Unit**: `%` (percentage).
        - **Importance**: Affects water retention, nutrient availability, and soil structure.

    5. **nitrogen**:
        - **Description**: Total nitrogen content in the soil.
        - **Mapped Unit**: `cg/kg` (centigrams per kilogram).
        - **Target Unit**: `g/kg` (grams per kilogram).
        - **Importance**: Essential for plant growth, nitrogen is a critical macronutrient.

    6. **ocd** (Organic Carbon Density):
        - **Description**: Amount of organic carbon stored in the soil per unit volume.
        - **Mapped Unit**: `dg/dm³` (decigrams per cubic decimeter).
        - **Target Unit**: `hg/m³` (hectograms per cubic meter).
        - **Importance**: Indicative of soil fertility and its ability to support microbial life.

    7. **phh2o** (pH in Water):
        - **Description**: Soil pH measures the acidity or alkalinity of the soil when mixed with water.
        - **Mapped Unit**: `pH*10` (pH multiplied by 10 for precision).
        - **Target Unit**: `-` (dimensionless pH scale).
        - **Importance**: Affects nutrient availability and microbial activity in the soil.

    8. **sand**:
        - **Description**: Percentage of soil particles between 0.05 mm and 2 mm in diameter.
        - **Mapped Unit**: `g/kg` (grams per kilogram).
        - **Target Unit**: `%` (percentage).
        - **Importance**: Sand influences drainage and aeration but contributes little to nutrient retention.

    9. **silt**:
        - **Description**: Percentage of soil particles between 0.002 mm and 0.05 mm in diameter.
        - **Mapped Unit**: `g/kg` (grams per kilogram).
        - **Target Unit**: `%` (percentage).
        - **Importance**: Contributes to soil fertility and water retention.

    10. **soc** (Soil Organic Carbon):
        - **Description**: Total organic carbon content in the soil.
        - **Mapped Unit**: `dg/kg` (decigrams per kilogram).
        - **Target Unit**: `g/kg` (grams per kilogram).
        - **Importance**: Essential for nutrient cycling, microbial activity, and soil structure.

    11. **wv0010** (Water Volume at -10 kPa):
        - **Description**: Soil water content retained at a matric potential of -10 kPa.
        - **Mapped Unit**: `(10^-2 cm³/cm³)*10`.
        - **Target Unit**: `10^-2 cm³/cm³`.
        - **Importance**: Indicates available water content for plant roots under light tension.

    12. **wv0033** (Water Volume at -33 kPa):
        - **Description**: Soil water content retained at a matric potential of -33 kPa (field capacity).
        - **Mapped Unit**: `(10^-2 cm³/cm³)*10`.
        - **Target Unit**: `10^-2 cm³/cm³`.
        - **Importance**: Indicates field capacity, the maximum water the soil can hold after drainage.

    13. **wv1500** (Water Volume at -1500 kPa):
        - **Description**: Soil water content retained at a matric potential of -1500 kPa (wilting point).
        - **Mapped Unit**: `(10^-2 cm³/cm³)*10`.
        - **Target Unit**: `10^-2 cm³/cm³`.
        - **Importance**: Represents the permanent wilting point, beyond which plants cannot extract water."""


    data_dict = fetch_data(coordinates)
    records = []
    for layer in data_dict["properties"]["layers"]:
        property_name = layer["name"]
        depths = layer["depths"]
        mean = 0
        mean_uncertainty = 0
        depth_count = 0

        for depth in depths:
            depth_label = depth["label"]
            mean_value = depth["values"]["mean"]
            uncertainty = depth["values"]["uncertainty"]
            mean += mean_value
            mean_uncertainty += uncertainty
            depth_count += 1

        average_mean = mean / depth_count if depth_count > 0 else None
        mean_uncertainty = mean_uncertainty / depth_count if depth_count > 0 else None
        records.append({
            "latitude": coordinates[1],
            "longitude": coordinates[0],
            "property": property_name,
            "mapped_unit": layer["unit_measure"]["mapped_units"],
            "mean_value_mapped_unit": average_mean,
            "mean_uncertainty_mapped_unit": mean_uncertainty,
            "target_unit": layer["unit_measure"]["target_units"],
            "mean_value_target_unit": average_mean / layer["unit_measure"]["d_factor"],
            "mean_uncertainty_target_unit": mean_uncertainty / layer["unit_measure"]["d_factor"],
        })

    df = pd.DataFrame(records)
    return df


"""
df = get_soil_properties((18.3448, 52.2079))
print(df)
df.to_csv("soil_properties.csv", index=False)
"""
