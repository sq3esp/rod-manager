

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView

from ..dir_models.account import Account

from rest_framework.response import Response
from rest_framework import serializers, status

from ..dir_models.two_step_login import TwoStepLogin
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from rodManager.dir_models.account import Account
from rodManager.dir_models.passwordreset import PasswordReset
from rodManager.libs.mailsending import send_mail_from_template


class CustomLoginSerializer2(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    code = serializers.CharField(required=True)


class CustomLogin2(TokenObtainPairView):
    @extend_schema(
        summary="Second_Login",
        description="Second_Login to the system.",
        request=CustomLoginSerializer2,
        responses={
            200: OpenApiResponse(
                description="Login successful.",
                response={
                    "type": "object",
                    "properties": {
                        "refresh": {"type": "string"},
                        "access": {"type": "string"},
                        "roles": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                },
            ),
            400: OpenApiResponse(
                description="Bad request.",
                response={
                    "type": "object",
                    "properties": {"error": {"type": "string"}},
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):

        if request.data.get("code") is None:
            return Response(
                {"error": "code is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        TwoStepLogin.objects.filter(valid_until__lt=timezone.now()).delete()

        if not TwoStepLogin.objects.filter(token=request.data.get("code")).exists():
            return Response(
                {"error": "Token expired or does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        twoStep = TwoStepLogin.objects.get(token=request.data.get("code"))
        if (twoStep.user.email == request.data.get("email")):
            response = super().post(request, *args, **kwargs)
            roles = Account.objects.get(email=request.data["email"]).groups
            response.data["roles"] = [role.name for role in roles.all()]
            return response
        else:
            return Response(
                {"error": "Code is not Correct"},
                status=status.HTTP_400_BAD_REQUEST,
            )
