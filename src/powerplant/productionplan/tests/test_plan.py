from functools import reduce

from django.test import TestCase

from powerplant.productionplan.constants import PowerplantType

from ..plan import LoadCouldNotBeMatchedError, calculate_production_plan
from ..types import FuelDict, PowerplantDict


class ProductionPlanTests(TestCase):
    def test_one_plant_with_pmax_under_expected_load(self):
        fuels: FuelDict = {"gas": 13.4, "kerosine": 50.8, "co2": 20, "wind": 60}

        plants: list[PowerplantDict] = [
            {
                "name": "gasfiredbig1",
                "type": PowerplantType.gasfired,
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            }
        ]

        with self.assertRaises(LoadCouldNotBeMatchedError):
            calculate_production_plan(
                expected_load=500, fuels=fuels, powerplants=plants
            )

    def test_one_plant_with_pmin_above_expected_load(self):
        fuels: FuelDict = {"gas": 13.4, "kerosine": 50.8, "co2": 20, "wind": 60}

        plants: list[PowerplantDict] = [
            {
                "name": "gasfiredbig1",
                "type": PowerplantType.gasfired,
                "efficiency": 0.53,
                "pmin": 550,
                "pmax": 1000,
            }
        ]

        with self.assertRaises(LoadCouldNotBeMatchedError):
            calculate_production_plan(
                expected_load=500, fuels=fuels, powerplants=plants
            )

    def test_one_plant_with_load_under_min(self):
        fuels: FuelDict = {"gas": 13.4, "kerosine": 50.8, "co2": 20, "wind": 60}

        plants: list[PowerplantDict] = [
            {
                "name": "gasfiredbig1",
                "type": PowerplantType.gasfired,
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            }
        ]

        with self.assertRaises(LoadCouldNotBeMatchedError):
            calculate_production_plan(expected_load=50, fuels=fuels, powerplants=plants)

    def test_happy_flow_1(self):
        fuels: FuelDict = {"gas": 13.4, "kerosine": 50.8, "co2": 20, "wind": 60}

        plants: list[PowerplantDict] = [
            {
                "name": "gasfiredbig1",
                "type": PowerplantType.gasfired,
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
            {
                "name": "gasfiredbig2",
                "type": PowerplantType.gasfired,
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
            {
                "name": "gasfiredsomewhatsmaller",
                "type": PowerplantType.gasfired,
                "efficiency": 0.37,
                "pmin": 40,
                "pmax": 210,
            },
            {
                "name": "tj1",
                "type": PowerplantType.turbojet,
                "efficiency": 0.3,
                "pmin": 0,
                "pmax": 16,
            },
            {
                "name": "windpark1",
                "type": PowerplantType.windturbine,
                "efficiency": 1,
                "pmin": 0,
                "pmax": 150,
            },
            {
                "name": "windpark2",
                "type": PowerplantType.windturbine,
                "efficiency": 1,
                "pmin": 0,
                "pmax": 36,
            },
        ]

        plants_plan = calculate_production_plan(
            expected_load=480, fuels=fuels, powerplants=plants
        )
        print(plants_plan)

        calculated_load = reduce(
            lambda load, plant: plant["power"] + load, plants_plan, 0
        )

        self.assertEqual(calculated_load, 480)

    def test_happy_flow_2(self):
        fuels: FuelDict = {
            "gas": 13.4,
            "kerosine": 50.8,
            "co2": 20,
            "wind": 0,
        }
        plants: list[PowerplantDict] = [
            {
                "name": "gasfiredbig1",
                "type": PowerplantType.gasfired,
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
            {
                "name": "gasfiredbig2",
                "type": PowerplantType.gasfired,
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
            {
                "name": "gasfiredsomewhatsmaller",
                "type": PowerplantType.gasfired,
                "efficiency": 0.37,
                "pmin": 40,
                "pmax": 210,
            },
            {
                "name": "tj1",
                "type": PowerplantType.turbojet,
                "efficiency": 0.3,
                "pmin": 0,
                "pmax": 16,
            },
            {
                "name": "windpark1",
                "type": PowerplantType.windturbine,
                "efficiency": 1,
                "pmin": 0,
                "pmax": 150,
            },
            {
                "name": "windpark2",
                "type": PowerplantType.windturbine,
                "efficiency": 1,
                "pmin": 0,
                "pmax": 36,
            },
        ]

        plants_plan = calculate_production_plan(
            expected_load=480, fuels=fuels, powerplants=plants
        )

        calculated_load = reduce(
            lambda load, plant: plant["power"] + load, plants_plan, 0
        )

        self.assertEqual(calculated_load, 480)
        self.assertTrue(all(plant["power"] > 0 for plant in plants_plan))

    def test_happy_flow_3(self):
        fuels: FuelDict = {"gas": 13.4, "kerosine": 50.8, "co2": 20, "wind": 60}
        plants: list[PowerplantDict] = [
            {
                "name": "gasfiredbig1",
                "type": PowerplantType.gasfired,
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
            {
                "name": "gasfiredbig2",
                "type": PowerplantType.gasfired,
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
            {
                "name": "gasfiredsomewhatsmaller",
                "type": PowerplantType.gasfired,
                "efficiency": 0.37,
                "pmin": 40,
                "pmax": 210,
            },
            {
                "name": "tj1",
                "type": PowerplantType.turbojet,
                "efficiency": 0.3,
                "pmin": 0,
                "pmax": 16,
            },
            {
                "name": "windpark1",
                "type": PowerplantType.windturbine,
                "efficiency": 1,
                "pmin": 0,
                "pmax": 150,
            },
            {
                "name": "windpark2",
                "type": PowerplantType.windturbine,
                "efficiency": 1,
                "pmin": 0,
                "pmax": 36,
            },
        ]

        plants_plan = calculate_production_plan(
            expected_load=910, fuels=fuels, powerplants=plants
        )

        calculated_load = reduce(
            lambda load, plant: plant["power"] + load, plants_plan, 0
        )

        self.assertEqual(calculated_load, 910)
