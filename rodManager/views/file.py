from urllib.parse import quote

from django.http import HttpResponse
from django.views import View
from rodManager.users.validate import permission_required


class FileView(View):
    @permission_required("rodManager.view_roddocument")
    def get(self, request, file_path):
        try:
            if 'roddocuments' not in file_path and 'images' not in file_path:
                return HttpResponse("Invalid file path.", status=400)
            response = HttpResponse()
            response["X-Accel-Redirect"] = f"/media/{quote(file_path)}"
            response["Content-Type"] = ""
            return response
        except:
            return HttpResponse(status=404, content="File does not exist.")



