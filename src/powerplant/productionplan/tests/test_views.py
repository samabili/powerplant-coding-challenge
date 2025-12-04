from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class PowerplantViewTests(APITestCase):
    def test_pmax_smaller_than_pmin(self):
        endpoint = reverse("productionplan:productionplan")

        response = self.client.post(
            endpoint,
            data={
                "load": 480,
                "fuels": {
                    "gas(euro/MWh)": 13.4,
                    "kerosine(euro/MWh)": 50.8,
                    "co2(euro/ton)": 20,
                    "wind(%)": 60,
                },
                "powerplants": [
                    {
                        "name": "gasfiredbig1",
                        "type": "gasfired",
                        "efficiency": 0.53,
                        "pmin": 100,  # Larger than pmax!
                        "pmax": 50,
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["powerplants"][0],
            {"pmax": ["The value of pmax should be greater or equal to pmin."]},
        )

    def test_load_could_not_be_matched(self):
        endpoint = reverse("productionplan:productionplan")

        response = self.client.post(
            endpoint,
            data={
                "load": 480,
                "fuels": {
                    "gas(euro/MWh)": 13.4,
                    "kerosine(euro/MWh)": 50.8,
                    "co2(euro/ton)": 20,
                    "wind(%)": 60,
                },
                "powerplants": [
                    {
                        "name": "gasfiredbig1",
                        "type": "gasfired",
                        "efficiency": 0.53,
                        "pmin": 50,
                        "pmax": 100,
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.json()["message"], "The load could not be matched.")
