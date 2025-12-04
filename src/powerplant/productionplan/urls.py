from django.urls import path

from .views import ProductionPlanView

app_name = "productionplan"

urlpatterns = [
    path(
        "productionplan/",
        ProductionPlanView.as_view(),
        name="productionplan",
    ),
]
