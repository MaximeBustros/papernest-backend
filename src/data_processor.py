from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point


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

    def _get_operators_covering_region(
        self, latitude, longitude, distance_in_meters
    ) -> set:
        gdfsel = gpd.GeoDataFrame(
            geometry=[Point(latitude, longitude)], crs="EPSG:4326"
        )
        # Convert to 3035 to add 500 Meter radius buffer then convert back to EPSG4326
        gdfsel.to_crs(crs=3035, inplace=True)
        buffer = gdfsel.buffer(distance_in_meters)
        buffer = buffer.to_crs(4326)

        gdfsel = gpd.GeoDataFrame(geometry=buffer, crs="EPSG:4326")

        # La selection gdfsel à l'aire plutot bonne
        # Main le within ne fonctionne pas :( comme prévu dans la doc
        df = self.geodataframe[
            self.geodataframe["2G"]
            == 1 & self.geodataframe.within(gdfsel.iloc[0].geometry)
        ]
        return set(df["Nom Operateur"].unique())

    def get_operators_covering_2g(self, latitude: float, longitude: float):
        """Get dataframe row of values at 500m away that have 2g enabled"""
        return self._get_operators_covering_region(
            latitude=latitude, longitude=longitude, distance_in_meters=500
        )

    def get_operators_covering_3g(self, latitude: float, longitude: float):
        """Get dataframe row of values at 300m away that have 3g enabled"""
        return self._get_operators_covering_region(
            latitude=latitude, longitude=longitude, distance_in_meters=500
        )

    def get_operators_covering_4g(self, latitude: float, longitude: float):
        """Get dataframe row of values at 200m away that have 4g enabled"""
        return self._get_operators_covering_region(
            latitude=latitude, longitude=longitude, distance_in_meters=500
        )
