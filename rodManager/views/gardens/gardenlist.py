from rest_framework.decorators import api_view
from rest_framework.response import Response
from rodManager.dir_models.garden import Garden
from django.core import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rodManager.users.validate import permission_required


@api_view(['GET'])
@swagger_auto_schema(
    responses={
        201: openapi.Response(
            description="Garden list.",
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_OBJECT),
        ),
        400: openapi.Response(
            description="Bad request.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
        403: openapi.Response(
            description="Forbidden.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
    },
)
@permission_required("rodManager.view_garden")
def garden_list(request):
    gardens = Garden.objects.all()
    
    return Response(serializers.serialize("json", gardens))



@api_view(['get'])
@swagger_auto_schema(
    responses= openapi.Response(
        description="Garden count.",
        type=openapi.TYPE_OBJECT,
        properties={
            "count": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    ),
    
)
@permission_required("rodManager.view_garden")
def garden_count(request):
    return Response({"count": Garden.objects.count()})
