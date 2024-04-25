from urllib.parse import quote

from django.http import HttpResponse
from django.views import View

# TODO sprawdzic czy w sciezce jest roddocuments jezeli tak to git a jak nie to wywal blad
class FileView(View):
    def get(self, request, file_path):
        response = HttpResponse()
        response["X-Accel-Redirect"] = f"/media/{quote(file_path)}"
        response["Content-Type"] = ""
        return response
