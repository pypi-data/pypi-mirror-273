from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.config import Settings

app = FastAPI(
    title=Settings.metadata.project.name,
    version=Settings.metadata.project.version,
    summary=Settings.metadata.project.description,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # hide schemas section
        "operationsSorter": "method",
        # Function=(a => a). Apply a sort to the operation list of each API.
        # It can be 'alpha' (sort by paths alphanumerically),
        # 'method' (sort by HTTP method) or a
        # function (see Array.prototype.sort() to know how sort function works).
        # Default is the order returned by the server unchanged.
    },
    default_response_class=ORJSONResponse,
)
