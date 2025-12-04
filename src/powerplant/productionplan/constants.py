from django.db.models import TextChoices


class PowerplantType(TextChoices):
    gasfired = "gasfired", "Gas fired"
    turbojet = "turbojet", "Turbojet"
    windturbine = "windturbine", "Wind turbine"
