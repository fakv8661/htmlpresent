from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
templates_present = Jinja2Templates(directory="templates/presentations")