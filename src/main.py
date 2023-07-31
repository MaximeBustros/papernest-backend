from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Query

from data_processor import DataProcessor
from services.address_data_gouv import AddressDataGouvService

app = FastAPI()
DATA_PATH = Path("data/series.geojson")
data_processor = DataProcessor(DATA_PATH)


@app.get("/")
def get_network_availability(
    q: str = Query(..., description="Address to check network availability")
):
    if not q:
        raise HTTPException(status_code=400, detail="Address is required")

    geojson_address = AddressDataGouvService.get_one_address(q)
    latitude: float = geojson_address["features"][0]["geometry"]["coordinates"][0]
    longitude: float = geojson_address["features"][0]["geometry"]["coordinates"][1]

    operators_2g: set = data_processor.get_operators_covering_2g(latitude, longitude)
    operators_3g: set = data_processor.get_operators_covering_3g(latitude, longitude)
    operators_4g: set = data_processor.get_operators_covering_4g(latitude, longitude)

    # Format result
    list_of_operators: set = operators_2g.intersection(operators_3g).intersection(
        operators_4g
    )
    result = {
        operator: {"2G": False, "3G": False, "4G": False}
        for operator in (list_of_operators)
    }
    for op in operators_2g:
        result[op]["2G"] = True
    for op in operators_3g:
        result[op]["3G"] = True
    for op in operators_3g:
        result[op]["4G"] = True

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
