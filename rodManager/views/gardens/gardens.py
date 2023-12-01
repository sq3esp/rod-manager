
from telnetlib import GA
from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rodManager.dir_models.garden import Garden, GardenNameSerializer, PlotStatus, GardenSerializer
from django.core import serializers
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiParameter, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rodManager.libs.rodpagitation import RODPagination
import drf_spectacular.serializers as drfserializers




class GardensCRUD(APIView):  
    queryset = Garden.objects.all()
    serializer_class = GardenNameSerializer
    pagination_class = RODPagination
    @extend_schema(
    summary="Get gardens",
    description="Get all gardens.",
    parameters=[
        OpenApiParameter(name="page", type=OpenApiTypes.INT),
        OpenApiParameter(name="page_size", type=OpenApiTypes.INT),
    ],
    responses={
        200: OpenApiResponse(
            description="Garden list.",
            response=GardenNameSerializer(many=True),
        ),
    }
    
    )
    def get(self, request):
        paginator = RODPagination()
        if  request.user.is_authenticated:
            gardens = paginator.paginate_queryset(Garden.objects.all().order_by("id"), request)
            return paginator.get_paginated_response(GardenNameSerializer(gardens).data)
        else:
            return Response({"error": "You don't have permission to view gardens."}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
    summary="Create garden",
    request=GardenSerializer,
    responses={
        201: OpenApiResponse(
            description="Garden created."
        ),
        400: OpenApiResponse(
            description="Bad request."
        ),
        403: OpenApiResponse(
            description="Forbidden."
        ),
    }
    )
    def post(self, request):
        if request.user.is_authenticated:
            if not request.data.get("sector") or not request.data.get("avenue") or not request.data.get("number") or not request.data.get("area"):
                return Response({"error": "Sector, avenue, number, area and status are required."}, status=status.HTTP_400_BAD_REQUEST)
           
            
            if Garden.objects.filter(
                sector=request.data["sector"],
                avenue=request.data["avenue"],
                number=request.data["number"],
            ).exists():
                return Response({"error": "Garden already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            newgarden = Garden.objects.create(
                sector=request.data["sector"],
                avenue=request.data["avenue"],
                number=request.data["number"],
                area=request.data["area"],
                status=PlotStatus.AVAILABLE,
            )
            newgarden.save()
            return Response({"success": "Garden created successfully."}, status=status.HTTP_201_CREATED)
        else :
            return Response({"error": "You don't have permission to create gardens."}, status=status.HTTP_403_FORBIDDEN)
        
    
    
    @extend_schema(
    summary="Edit garden",
    parameters=[
        OpenApiParameter(name="id", type=OpenApiTypes.INT),
        OpenApiParameter(name="sector", type=OpenApiTypes.STR),
        OpenApiParameter(name="avenue", type=OpenApiTypes.STR),
        OpenApiParameter(name="number", type=OpenApiTypes.INT),
        OpenApiParameter(name="area", type=OpenApiTypes.INT),
        OpenApiParameter(name="status", type=OpenApiTypes.STR),
        OpenApiParameter(name="leaseholderID", type=OpenApiTypes.INT),
    ],
    request=inline_serializer("Garden", fields={
        "id": int,
        "sector": str,
        "avenue": str,
        "number": str,
        "area": str,
        "leaseholderID": str,
    }),
    )
    def put(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "You don't have permission to edit gardens."}, status=status.HTTP_403_FORBIDDEN)
        if not request.data["id"]:
                return Response({"error": "Garden ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data["sector"] or not request.data["avenue"] or not request.data["number"] or not request.data["area"] or not request.data["status"]:
                return Response({"error": "Sector, avenue, number, area and status are required."}, status=status.HTTP_400_BAD_REQUEST)
        if request.data["status"] not in ["dostępna", "niedostępna"]:
            return Response({"error": "Status must be dostępna or niedostępna."}, status=status.HTTP_400_BAD_REQUEST)
        if not Garden.objects.filter(
            id = request.data["id"],
            sector=request.data["sector"],
            avenue=request.data["avenue"],
            number=request.data["number"],
        ).exists():
            return Response({"error": "Garden doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
        garden = Garden.objects.get(id=request.data["id"])
        garden.leaseholderID = request.data["leaseholderID"]
        garden.status = request.data["status"]
        garden.save()
        return Response({"success": "Garden edited successfully."}, status=status.HTTP_200_OK)  
        
    @extend_schema(
    summary="Delete garden",
    parameters=[
        OpenApiParameter(name="id", type=OpenApiTypes.INT),
    ],
    responses={
        200: "Garden deleted.",
        400: "Bad request.",
        403: "Forbidden.",
    },
    )
    def delete(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "You don't have permission to delete gardens."}, status=status.HTTP_403_FORBIDDEN)
        if Garden.objects.filter(id=request.data["id"]).exists():
            Garden.objects.get(id=request.data["id"]).delete()
            return Response({"success": "Garden deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Garden doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)