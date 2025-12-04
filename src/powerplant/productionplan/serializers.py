from typing import Any

from rest_framework import serializers

from .constants import PowerplantType


class FuelsSerializer(serializers.Serializer):
    gas = serializers.FloatField(source="gas(euro/MWh)", min_value=0, required=True)
    kerosine = serializers.FloatField(
        source="kerosine(euro/MWh)", min_value=0, required=True
    )
    co2 = serializers.FloatField(source="co2(euro/ton)", min_value=0, required=True)
    wind = serializers.FloatField(
        source="wind(%)", min_value=0, max_value=100, required=True
    )

    def to_internal_value(self, data: Any) -> Any:
        return super().to_internal_value(
            {
                "gas": data.get("gas(euro/MWh)"),
                "kerosine": data.get("kerosine(euro/MWh)"),
                "co2": data.get("co2(euro/ton)"),
                "wind": data.get("wind(%)"),
            }
        )


class PowerPlantSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    type = serializers.ChoiceField(choices=PowerplantType.choices, required=True)
    efficiency = serializers.FloatField(min_value=0, max_value=1, required=True)
    pmax = serializers.FloatField(required=True, min_value=0)
    pmin = serializers.FloatField(required=True, min_value=0)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if attrs["pmax"] < attrs["pmin"]:
            raise serializers.ValidationError(
                {"pmax": "The value of pmax should be greater or equal to pmin."}
            )

        return attrs


class ProductionPlanRequest(serializers.Serializer):
    load = serializers.FloatField(min_value=0, required=True)
    fuels = FuelsSerializer()
    powerplants = PowerPlantSerializer(many=True, required=True, allow_empty=False)


class PowerPerPlant(serializers.ListSerializer):
    name = serializers.CharField(required=True)
    power = serializers.FloatField(min_value=0, required=True)
