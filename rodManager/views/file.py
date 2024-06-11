from urllib.parse import quote

from django.http import HttpResponse
from django.views import View

# TODO sprawdzic czy w sciezce jest roddocuments jezeli tak to git a jak nie to wywal blad
class FileView(View):
    def get(self, request, file_path):
        try:
            if 'roddocuments' not in file_path:
                return HttpResponse(status=400, content="Invalid file path.")
            response = HttpResponse()
            response["X-Accel-Redirect"] = f"/media/{quote(file_path)}"
            response["Content-Type"] = ""
            return response
        except:
            return HttpResponse(status=404, content="File does not exist.")
