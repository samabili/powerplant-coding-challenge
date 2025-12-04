import logging

from .constants import PowerplantType
from .types import FuelDict, PowerplantDict, PowerplantWithPowerDict, ProductionPlanDict

logger = logging.getLogger(__name__)


class UnknownPowerplantTypeError(Exception):
    pass


class LoadCouldNotBeMatchedError(Exception):
    pass


def plant_score(powerplant: PowerplantDict, fuel_prices: FuelDict) -> float:
    """Score the powerplants based on fuel cost and efficiency"""
    fuel_used = powerplant["pmax"] / powerplant["efficiency"]
    match powerplant["type"]:
        case PowerplantType.gasfired:
            return fuel_used * fuel_prices["gas"]
        case PowerplantType.turbojet:
            return fuel_used * fuel_prices["kerosine"]
        case PowerplantType.windturbine:
            return 0
        case _:
            logger.error(
                "This should never happen. Serializer validation should "
                "have caught invalid plant type %s.",
                powerplant["type"],
            )
            raise UnknownPowerplantTypeError(
                "Unknown powerplant type %s.", powerplant["type"]
            )


def get_actual_power(
    power: float, plant_type: PowerplantType, fuels: FuelDict
) -> float:
    """Get the actual power that the powerplant can produce"""
    return (
        power * (fuels["wind"] / 100)
        if plant_type == PowerplantType.windturbine
        else power
    )


def format_plan(powerplants: list[PowerplantWithPowerDict]) -> list[ProductionPlanDict]:
    return [
        {"name": plant["name"], "power": round(plant["power"], 1)}
        for plant in powerplants
    ]


def calculate_production_plan(
    expected_load: float, fuels: FuelDict, powerplants: list[PowerplantDict]
) -> list[ProductionPlanDict]:
    sorted_plants = sorted(powerplants, key=lambda plant: plant_score(plant, fuels))

    current_load = 0
    active_plants = []
    inactive_plants = []
    # Start by adding all the Pmax of the available powerplants and stop before you
    # overshoot the expected load
    for plant in sorted_plants:
        actual_pmax = get_actual_power(plant["pmax"], plant["type"], fuels)
        actual_pmin = get_actual_power(plant["pmin"], plant["type"], fuels)
        if actual_pmax == 0:
            continue

        if current_load + actual_pmax <= expected_load:
            current_load += actual_pmax
            active_plants.append({**plant, "power": actual_pmax})
            continue

        if current_load + actual_pmin > expected_load:
            inactive_plants.append(plant)
        else:
            power = expected_load - current_load
            current_load += power
            active_plants.append({**plant, "power": power})

        if current_load == expected_load:
            break

    if current_load == expected_load:
        return format_plan(active_plants)

    # The load is still too low.
    # All the inactive plants have a pmin too high which cause overshooting the expected load.
    # Try to reduce the power of the active plants to fit the pmin of the inactive plants.
    for active_plant in active_plants[::-1]:
        actual_pmin_active = get_actual_power(
            active_plant["pmin"], active_plant["type"], fuels
        )

        for inactive_plant in inactive_plants:
            power_to_reduce = (current_load + inactive_plant["pmin"]) - expected_load
            if actual_pmin_active - power_to_reduce > 0:
                active_plant["power"] -= power_to_reduce
                active_plants.append(
                    {**inactive_plant, "power": inactive_plant["pmin"]}
                )
                break

    if current_load != expected_load:
        logger.error(
            "Receive planning request where load could not be "
            "matched: load=%s, fuels=%s, powerplants=%s",
            expected_load,
            fuels,
            powerplants,
        )
        raise LoadCouldNotBeMatchedError()

    return format_plan(active_plants)
