import os
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

if __name__ == "__main__":
    """Extract CSV, convert Lambert93 coordinates to GPS coordinates and save to file.

    This file should allow the main program to load it as a GeoPandasDataFrame
    Allowing to treat GeoCodeJson data more easily
    """

    # Load data from CSV
    DATA_PATH = Path(
        "data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv"
    )
    print(f"Loading data from {DATA_PATH}")
    df = pd.read_csv(DATA_PATH, sep=";")

    #  Load as a geodataframe with points in lambert93
    geometry = [Point(xy) for xy in zip(df["x"], df["y"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:2154")

    # Convert lambert93 to WGS 84
    gdf.to_crs("EPSG:4326", inplace=True)

    # Save file to geojson
    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    filename = f"{current_file_directory}/../data/series.geojson"
    print(f"Writing to file {filename}")
    gdf.to_file(filename, driver="GeoJSON")
