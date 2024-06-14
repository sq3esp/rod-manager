from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.account import Account
from rodManager.dir_models.userdocument import UserDocument
from rodManager.users.validate import permission_required


class UserDocumentByUserIdView(APIView):
    @extend_schema(
        summary="Get user documents",
        description='Dostarczone dokumenty będą w poniższym formacje. Jeśli dokument jest folderem i posiada wewnątrz pliki, to w polu `items` będą zawarte dokumenty w nim zawarte. Jeśli dokument jest plikiem, to w polu `file_url` będzie zawarty link do pliku. \nPrzykład: \n```json\n[{\n    "id": 1,\n    "name": "folder",\n    "items": [{\n        "id": 2,\n        "name": "plik",\n        "file_url": "/mediafiles/userdocuments/plik.txt"\n    }]\n}]\n``` \n\n\nJeżeli folder jest pusty może zostać przekonwertowany na plik przez przesłanie pliku.\nW folderze może istnieć inny folder, struktura może być dowolnie zagnieżdżona.\nPrzykład zagnieżdżenia: \n```json\n[{\n    "id": 1,\n    "name": "folder",\n    "items": [{\n        "id": 2,\n        "name": "plik",\n        "file_url": "/mediafiles/userdocuments/plik.txt"\n    }, {\n        "id": 3,\n        "name": "folder2",\n        "items": [{\n            "id": 4,\n            "name": "plik2",\n            "file_url": "/mediafiles/userdocuments/plik2.txt"\n        }]\n    }]\n}]\n```',
    )
    @permission_required("rodManager.view_userdocument")
    def get(self, request, user_id):
        try:
            if user_id != 'myAccount':
                if user_id.isdigit():
                    user_id = Account.objects.get(id=user_id)
                else:
                    user_id = Account.objects.get(uid=user_id)
            else:
                user_id = request.user.id
        except Account.DoesNotExist:
            return Response({"error": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)
        root_documents = UserDocument.objects.filter(parent__isnull=True, user=user_id)
        data = [doc.to_dict() for doc in root_documents]
        return Response(data)
