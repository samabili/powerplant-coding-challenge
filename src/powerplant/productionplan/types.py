from typing import TypedDict

from .constants import PowerplantType


class ProductionPlanDict(TypedDict):
    power: float
    name: str


class FuelDict(TypedDict):
    gas: float
    kerosine: float
    co2: float
    wind: float


class PowerplantDict(TypedDict):
    name: str
    type: PowerplantType
    efficiency: float
    pmax: float
    pmin: float


class PowerplantWithPowerDict(TypedDict):
    name: str
    type: PowerplantType
    efficiency: float
    pmax: float
    pmin: float
    power: float
