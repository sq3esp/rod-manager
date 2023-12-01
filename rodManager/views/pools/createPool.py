from datetime import datetime

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.pool import (
    Option,
    OptionSerializer,
    Pool,
    PoolSerializer,
    Vote,
)


class AddOptionSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()
    label = serializers.CharField()


class AddVotingSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    options = AddOptionSerializer(many=True)
    finish_date = serializers.DateTimeField()

    def create(self, validated_data):
        pool = Pool.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            end_date=validated_data["finish_date"],
        )
        for option in validated_data["options"]:
            Option.objects.create(
                label=option["label"], option_id=option["option_id"], pool=pool
            )
        return pool


#    def validate(self, data):
#        if data["finish_date"] < datetime.now():
#            raise serializers.ValidationError("Finish date must be in the future")
#        return data


class CreatePool(APIView):
    @extend_schema(
        summary="Add pool",
        description="Add new pool.",
        request=AddVotingSerializer,
        responses={201: PoolSerializer},
    )
    def post(self, request):
        # Trzeba tutaj uważać na date bo podaje razem ze strefą czasową
        # iso_date = request.data['finishDate']
        #
        # date_object = datetime.fromisoformat(iso_date.replace('Z', ''))
        #
        # new_votings = request.data
        # newestvoting = str(date_object)
        # new_votings['finishDate'] = newestvoting

        serializer = AddVotingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = PoolSerializer(serializer.instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
