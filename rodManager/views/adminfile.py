from urllib.parse import quote

from django.http import HttpResponse
from django.views import View
from rest_framework.response import Response

from rodManager.users.validate import permission_required


# TODO sprawdzic czy w sciezce jest managerdocuments jezeli tak to git a jak nie to wywal blad
class AdminFileView(View):
    @permission_required()
    def get(self, request, file_path):
        try:
            if 'managerdocuments' not in file_path:
                return HttpResponse(status=400, content="Invalid file path.")

            if not request.user.groups.filter(name__in=["MANAGER", "ADMIN"]).exists():
                return HttpResponse(status=400, content="You don't have permission to access this file.")

            # Utwórz URL przekierowania
            redirect_url = f"/media/{quote(file_path)}"

            # Utwórz odpowiedź przekierowującą do pliku
            response = HttpResponse()
            response["X-Accel-Redirect"] = redirect_url
            response["Content-Type"] = "application/octet-stream"

            return response
        except:
            return HttpResponse(status=400, content="Account does not exist.")

    # def get(self, request, file_path):
    #     response = HttpResponse()
    #     response["X-Accel-Redirect"] = f"/media/{quote(file_path)}"
    #     response["Content-Type"] = ""
    #     return response
