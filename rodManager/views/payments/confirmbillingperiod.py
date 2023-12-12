from django.db.models import F, Max, Q
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.billingperiod import BillingPeriod
from rodManager.libs.rodpagitation import RODPagination
from rodManager.users.validate import permission_required


class BillingPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingPeriod
        fields = "__all__"


class AddBillingPeriodSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    payment_date = serializers.DateField()

    class Meta:
        model = BillingPeriod
        fields = ["start_date", "end_date", "payment_date"]

    def create(self, validated_data):
        billingperiod = BillingPeriod.objects.create(
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            payment_date=validated_data["payment_date"],
        )
        billingperiod.save()
        return billingperiod


class ConfirmBillingPeriodView(APIView):
    @extend_schema(
        summary="Confirm billing period",
        description="Confirm billing period in the system.",
        responses=BillingPeriodSerializer,
    )
    # @permission_required()
    def post(self, request, billing_period_id):
        if billing_period_id is None:
            return Response(
                {"error": "billing_period_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        billingperiod = get_object_or_404(BillingPeriod, pk=billing_period_id)
        if billingperiod.is_confirmed:
            return Response(
                {"error": "Billing period is already confirmed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # TUTAJ DZIEJE SIĘ CAŁA MAGIA DOPISYWANIA UŻYTKOWNIKOM OPŁAT NA STANY KONT
        billingperiod.is_confirmed = True
        billingperiod.save()
        return Response(BillingPeriodSerializer(billingperiod).data)