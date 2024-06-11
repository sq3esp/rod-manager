import uuid

from django.http import HttpResponse
from drf_spectacular.utils import OpenApiResponse, extend_schema
from requests import Response
from rest_framework import serializers, status
from rest_framework_simplejwt.views import TokenObtainPairView

from ..dir_models.account import Account
from ..libs.mailsending import send_mail_from_template

from ..dir_models.two_step_login import TwoStepLogin
from django.utils import timezone
from datetime import timedelta


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class CustomLogin(TokenObtainPairView):
    @extend_schema(
        summary="Login",
        description="Login to the system.",
        request=CustomLoginSerializer,

    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:

            timeRequest = 15
            user = Account.objects.get(email=request.data.get("email"))

            TwoStepLogin.objects.filter(user=user).delete()
            TwoStepLogin.objects.filter(valid_until__lt=timezone.now()).delete()
            token = uuid.uuid4()
            request = TwoStepLogin.objects.create(
                user=user,
                valid_until=timezone.now() + timedelta(minutes=timeRequest),
                token=token,
            )
            request.save()


            send_mail_from_template(
                "second_login",
                "Logowanie Dwuetapowe",
                [
                    "tomek@plociennik.info", "roszkolgaming@gmail.com"
                ],
                {
                    "code": str(request.token),
                    "time": str(timeRequest)
                },
            )
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400, content="Bad request.")
