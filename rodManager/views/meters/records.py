import datetime

from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.meter import Meter, MeterLastRecordSerializer
from rodManager.dir_models.record import (
    Record,
    RecordSerializer,
    RecordsValuesSerializer,
)
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


class RecordsCRUD(APIView):
    """
    Records CRUD
    """

    model = Record
    serializer_class = RecordSerializer
    pagination_class = RODPagination

    @extend_schema(
        summary="Get records",
        description="Get all records.",
        parameters=[
            OpenApiParameter(name="page", type=OpenApiTypes.INT),
            OpenApiParameter(name="page_size", type=OpenApiTypes.INT),
        ],
        responses={
            200: OpenApiResponse(
                description="Record list.",
                response=RecordSerializer(many=True),
            ),
        },
    )
    @permission_required("rodManager.view_record")
    def get(self, request):
        paginator = RODPagination()
        if request.user.is_authenticated:
            records = paginator.paginate_queryset(
                Record.objects.all().order_by("id"), request
            )
            return paginator.get_paginated_response(RecordSerializer(records).data)
        else:
            return Response(
                {"error": "You don't have permission to view records."},
                status=status.HTTP_403_FORBIDDEN,
            )

    @extend_schema(
        summary="Create record",
        request=RecordsValuesSerializer,
        responses={
            200: OpenApiResponse(
                description="Record created.",
                response=RecordSerializer,
            ),
        },
    )
    @permission_required("rodManager.add_record")
    def post(self, request):
        if request.user.is_authenticated:
            if request.data["value"] < 0:
                return Response(
                    {"error": "Value must be positive."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not request.data.get("datetime"):
                request.data["datetime"] = datetime.datetime.now()
            serializer = RecordSerializer(data=request.data)

            meter_serial = request.data.get("meter")
            if not Meter.objects.filter(serial=meter_serial).exists():
                return Response(
                    {"error": "Meter with this number does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_value = request.data.get("value")
            meter = Meter.objects.get(serial=meter_serial)
            last_value = MeterLastRecordSerializer().get_value(meter)
            if last_value and new_value < last_value:
                return Response(
                    {"error": "New value must be greater than the last recorded value."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "You don't have permission to create records."},
                status=status.HTTP_403_FORBIDDEN,
            )

    @extend_schema(
        summary="Delete record",
        description="Delete record by id.",
        parameters=[
            OpenApiParameter(name="id", type=OpenApiTypes.INT),
        ],
        responses={
            200: OpenApiResponse(
                description="Record deleted.",
            ),
        },
    )
    @permission_required("rodManager.delete_record")
    def delete(self, request, id):
        if request.user.is_authenticated:
            try:
                record = Record.objects.get(id=id)
                record.delete()
                return Response(status=status.HTTP_200_OK)
            except Record.DoesNotExist:
                return Response(
                    {"error": "Record not found."}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "You don't have permission to delete records."},
                status=status.HTTP_403_FORBIDDEN,
            )
