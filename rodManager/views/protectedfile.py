from urllib.parse import quote

from django.http import HttpResponse
from django.views import View
from rest_framework.response import Response

from rodManager.users.validate import permission_required

# TODO sprawdzic czy w sciezce jest userdocuments jezeli tak to git a jak nie to wywal blad
class ProtectedFileView(View):
    # @permission_required()
    # def get(self, request, file_path):
    #     try:
    #         response = HttpResponse()
    #         response["X-Accel-Redirect"] = f"/media/{quote(file_path)}"
    #         response["Content-Type"] = ""
    #
    #         # if (
    #         #     not request.user.groups.filter(name__in=["MANAGER", "ADMIN"]).exists()
    #         # ):
    #         #     return Response({"error": "You cannot view this account."}, status=403)
    #         # TODO zrobic sprawdzenie dla danego konta
    #
    #         return response
    #     except:
    #         return Response({"error": "Account does not exist."}, status=400)
    def get(self, request, file_path):
        response = HttpResponse()
        response["X-Accel-Redirect"] = f"/media/{quote(file_path)}"
        response["Content-Type"] = ""
        return response
