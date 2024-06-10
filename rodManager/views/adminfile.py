from urllib.parse import quote

from django.http import HttpResponse
from rest_framework.views import APIView


class AdminFileView(APIView):
    def get(self, request, file_path):
        try:
            if 'managerdocuments' not in file_path:
                return HttpResponse(status=400, content="Invalid file path.")

            if not request.user.groups.filter(name__in=["MANAGER", "ADMIN"]).exists():
                return HttpResponse(status=403, content="You don't have permission to access this file.")

            # Utwórz URL przekierowania
            redirect_url = f"/media/{quote(file_path)}"

            # Utwórz odpowiedź przekierowującą do pliku
            response = HttpResponse()
            response["X-Accel-Redirect"] = redirect_url
            response["Content-Type"] = "application/octet-stream"

            return response
        except:
            return HttpResponse(status=404, content="File does not exist.")
