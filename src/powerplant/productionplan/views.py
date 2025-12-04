from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .plan import LoadCouldNotBeMatchedError, calculate_production_plan
from .serializers import ProductionPlanRequest


class ProductionPlanView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request: Request) -> Response:
        serializer = ProductionPlanRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data

        try:
            plan = calculate_production_plan(
                data["load"], fuels=data["fuels"], powerplants=data["powerplants"]
            )
        except LoadCouldNotBeMatchedError:
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data={"message": "The load could not be matched."},
            )

        return Response(plan)
