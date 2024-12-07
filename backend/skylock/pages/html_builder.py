from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from skylock.skylock_facade import SkylockFacade
from skylock.utils.url_generator import UrlGenerator


class HtmlBuilder:
    def __init__(
        self, skylock: SkylockFacade, templates: Jinja2Templates, url_generator: UrlGenerator
    ):
        self._skylock = skylock
        self._templates = templates
        self._url_generator = url_generator

    def build_main_page(self, request: Request) -> HTMLResponse:
        return self._templates.TemplateResponse(request, "index.html")

    def build_folder_contents_page(self, request: Request, folder_id: str) -> HTMLResponse:
        folder_contents = self._skylock.get_public_folder_contents(folder_id)
        folders = [
            {"name": folder.name, "url": self._url_generator.generate_url_for_folder(folder.id)}
            for folder in folder_contents.folders
        ]
        files = [
            {"name": file.name, "url": self._url_generator.generate_url_for_file(file.id)}
            for file in folder_contents.files
        ]
        return self._templates.TemplateResponse(
            request,
            "folder_contents.html",
            {
                "name": folder_contents.folder_name,
                "path": folder_contents.folder_path,
                "folders": folders,
                "files": files,
            },
        )

    def build_403_page(self, request: Request, message: str) -> HTMLResponse:
        return self._templates.TemplateResponse(
            request, "403.html", {"message": message}, status_code=403
        )

    def build_404_page(self, request: Request) -> HTMLResponse:
        return self._templates.TemplateResponse(request, "404.html", status_code=404)
