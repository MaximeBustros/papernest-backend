from pathlib import Path

import geopandas as gpd


class DataProcessor:
    _instance = None

    # Implement singleton pattern
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataProcessor, cls).__new__(cls)
        return cls._instance

    def __init__(self, geojson_path: Path):
        self.load_data_from_geojson(geojson_path)

    def load_data_from_geojson(self, geojson_path):
        """Useful on initialization or if we want to load new data."""
        print(f"Loading data from {geojson_path}")
        self.geodataframe = gpd.GeoDataFrame.from_file(geojson_path)
        print("Data was loaded successfully")
