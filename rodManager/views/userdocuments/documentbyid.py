from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account
from rodManager.dir_models.userdocument import UserDocument


class UpdateUserDocumentSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    name = serializers.CharField(allow_null=False, required=False)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=UserDocument.objects.filter(file=""),
        allow_null=True,
        required=False,
    )
    file = serializers.FileField(allow_null=True, required=False)

    def update(self, instance, validated_data):
        instance.user = validated_data.get("user", instance.user)
        instance.name = validated_data.get("name", instance.name)
        instance.parent = validated_data.get("parent", instance.parent)
        if validated_data.get("file", None):
            if instance.file:
                instance.file.delete()
        instance.file = validated_data.get("file", instance.file)
        instance.save()
        return instance


class UserDocumentByIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=UserDocument.objects.all(), allow_null=True
    )
    file = serializers.FileField(allow_null=True, required=False)


class UserDocumentByIdView(APIView):
    @extend_schema(
        summary="Put user document",
        description="Put user document by id.",
        request=UpdateUserDocumentSerializer,
    )
    def put(self, request, document_id):
        try:
            user_id = request.data.get("user")
            document = UserDocument.objects.get(user=user_id)
        except Account.DoesNotExist:
            return Response({"error": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)
        except UserDocument.DoesNotExist:
            return Response({"error": f"User document does not exist."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateUserDocumentSerializer(document, data=request.data)
        serializer.is_valid(raise_exception=True)
        response = UserDocumentByIdSerializer(serializer.save()).data
        return Response(response)

    @extend_schema(
        summary="Delete user document",
        description="Delete user document by id.",
        responses={204: None},
    )
    def delete(self, request, document_id):
        try:
            document = UserDocument.objects.get(user=document_id)
        except UserDocument.DoesNotExist:
            return Response({"error": f"User document does not exist."}, status=status.HTTP_404_NOT_FOUND)
        if document.file:
            document.file.delete()
        document.delete()
        return Response(status=204)
