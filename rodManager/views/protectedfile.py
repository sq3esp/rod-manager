from urllib.parse import quote

from django.http import HttpResponse
from rest_framework.views import APIView

from rodManager.dir_models.userdocument import UserDocument


class ProtectedFileView(APIView):
    def get(self, request, file_path):
        try:
            if 'userdocuments' not in file_path:
                return HttpResponse(status=400, content="Invalid file path.")

            user_id = UserDocument.objects.all().filter(file=file_path).values("user_id")
            print(user_id)
            if user_id:
                user_id2 = user_id[0]["user_id"]
                if request.user.groups.filter(name__in=["MANAGER", "ADMIN"]).exists() or request.user.id == user_id2:
                    pass
                else:
                    return HttpResponse(status=403, content="You don't have permission to access this file.")
            else:
                return HttpResponse(status=404, content="File not found.")

            redirect_url = f"/media/{quote(file_path)}"

            response = HttpResponse()
            response["X-Accel-Redirect"] = redirect_url
            response["Content-Type"] = "application/octet-stream"

            return response
        except:
            return HttpResponse(status=404, content="Something went wrong.")
