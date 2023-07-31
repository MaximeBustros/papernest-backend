"""This module is used for providing a service for querying https://adresse.data.gouv.fr/api."""

import requests
from fastapi import HTTPException


class AddressDataGouvService:
    API_BASE_URL = "https://api-adresse.data.gouv.fr/search/"

    @staticmethod
    def get_one_address(address_query: str) -> dict:
        try:
            url = f"{AddressDataGouvService.API_BASE_URL}?q={address_query}&limit=1"
            response = requests.get(url)
            response.raise_for_status()
            json_response = response.json()
            if (
                not json_response
                or "features" not in json_response
                or not json_response["features"]
            ):
                raise HTTPException(
                    status_code=400, detail=f"No address was found for {address_query}"
                )
            return json_response
        except requests.RequestException as e:
            raise Exception(f"Failed to query address: {e}") from e
