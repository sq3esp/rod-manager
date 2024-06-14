import datetime
from itertools import chain

from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rodManager.dir_models.garden import Garden
from rodManager.dir_models.meter import Meter, MeterLastRecordSerializer
from rodManager.dir_models.record import Record, RecordSerializer
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required

valid_meter_types = ["woda", "prąd"]


class MetersCRUD(APIView):

    queryset = Meter.objects.all()
    serializer_class = MeterLastRecordSerializer
    pagination_class = RODPagination

    @extend_schema(
        summary="Get meters",
        description="Get all meters.",
        parameters=[
            OpenApiParameter(name="page", type=OpenApiTypes.INT),
            OpenApiParameter(name="page_size", type=OpenApiTypes.INT),
            OpenApiParameter(name="type", type=OpenApiTypes.STR),
        ],
        responses={
            200: OpenApiResponse(
                description="Meter list.",
                response=MeterLastRecordSerializer(many=True),
            ),
        },
    )
    @permission_required("rodManager.view_meter")
    def get(self, request):
        paginator = RODPagination()

        if request.user.is_authenticated:
            if request.GET.get("type"):
                no_garden_meters = Meter.objects.filter(
                    type=request.GET["type"], garden=None
                ).order_by("adress")
                otherMeters = Meter.objects.filter(type=request.GET["type"]).order_by(
                    "adress"
                )

                # Połączenie i usunięcie powtórzeń z zachowaniem kolejności
                unique_combined_list = []
                seen = set()
                for meter in chain(no_garden_meters, otherMeters):
                    if meter not in seen:
                        unique_combined_list.append(meter)
                        seen.add(meter)

                paginated_accounts = paginator.paginate_queryset(
                    unique_combined_list, request
                )

                return paginator.get_paginated_response(
                    MeterLastRecordSerializer(paginated_accounts, many=True).data
                )
            else:

                no_garden_meters = Meter.objects.filter(garden=None).order_by("adress")
                otherMeters = Meter.objects.all().order_by("adress")

                # Połączenie i usunięcie powtórzeń z zachowaniem kolejności
                unique_combined_list = []
                seen = set()
                for meter in chain(no_garden_meters, otherMeters):
                    if meter not in seen:
                        unique_combined_list.append(meter)
                        seen.add(meter)

                paginated_accounts = paginator.paginate_queryset(
                    unique_combined_list, request
                )

                return paginator.get_paginated_response(
                    MeterLastRecordSerializer(paginated_accounts, many=True).data
                )

        else:
            return Response(
                {"error": "You don't have permission to view meters."},
                status=status.HTTP_403_FORBIDDEN,
            )

    @extend_schema(
        summary="Create meter",
        request=MeterLastRecordSerializer,
        responses={
            201: OpenApiResponse(description="Meter created."),
            400: OpenApiResponse(description="Bad request."),
            403: OpenApiResponse(description="Forbidden."),
        },
    )
    @permission_required("rodManager.add_meter")
    def post(self, request):
        if request.user.is_authenticated:
            serial = request.data.get("serial")
            meter_type = request.data.get("type")
            address = request.data.get("adress")
            garden_id = request.data.get("garden")

            if not request.data.get("serial") or not request.data.get("type"):
                return Response(
                    {"error": "Serial and type are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Walidacja czy typ licznika jest poprawny
            if meter_type not in valid_meter_types:
                return Response(
                    {"error": "Type must be either 'woda' or 'prąd'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Walidacja czy istnieje licznik o podanym numerze seryjnym
            if Meter.objects.filter(serial=serial).exists():
                return Response(
                    {"error": "Meter already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Walidacja adresu
            if not address:
                return Response(
                    {"error": "Adress cannot be empty."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if garden_id:
                if not Garden.objects.filter(id=request.data["garden"]).exists():
                    return Response(
                        {"error": "Garden does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Walidacja czy w ogrodzie nie ma już meter o podanym typie
                if Meter.objects.filter(garden_id=garden_id, type=meter_type).exists():
                    return Response(
                        {"error": "Garden already has a meter of this type."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            newmeter = Meter(
                serial=serial,
                type=meter_type,
                adress=address,
                garden=Garden.objects.get(id=garden_id) if garden_id else None,
            )

            if request.data.get("value"):
                Record.objects.create(
                    meter=newmeter,
                    value=request.data["value"],
                    datetime=datetime.datetime.now(),
                )
            newmeter.save()
            return Response(
                {"message": "Meter created."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "You don't have permission to create meters."},
                status=status.HTTP_403_FORBIDDEN,
            )

    @extend_schema(
        summary="Delete meter",
        parameters=[
            OpenApiParameter(name="id", type=OpenApiTypes.INT),
        ],
        responses={
            200: OpenApiResponse(description="Meter deleted."),
            400: OpenApiResponse(description="Bad request."),
            403: OpenApiResponse(description="Forbidden."),
        },
    )
    @permission_required("rodManager.delete_meter")
    def delete(self, request):
        if not request.data.get("serial"):
            return Response(
                {"error": "Serial is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        if not Meter.objects.filter(serial=request.data["serial"]).exists():
            return Response(
                {"error": "Meter does not exist."}, status=status.HTTP_400_BAD_REQUEST
            )
        Meter.objects.get(serial=request.data["serial"]).delete()
        return Response({"message": "Meter deleted."}, status=status.HTTP_200_OK)
