from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView

from ..dir_models.account import Account

from rest_framework.response import Response
from rest_framework import serializers, status


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

        if(request.data["code"] == "dupa"):
            response = super().post(request, *args, **kwargs)
            roles = Account.objects.get(email=request.data["email"]).groups
            response.data["roles"] = [role.name for role in roles.all()]
            return response
        else:
            return Response(
                {"error": "Code is not Correct"},
                status=status.HTTP_400_BAD_REQUEST,
            )
