"""All internal API methods for admin only."""
from typing import Dict, List

from fastapi.responses import ORJSONResponse

import models
from routers.internal import APIRouter

router = APIRouter(
    prefix="/internal/admin",
    tags=["admin"],
    responses={418: {
        "description": "I'm an administrator"
    }},
    default_response_class=ORJSONResponse,
)


@router.get("/")
def read_table_info() -> Dict[str, List[str]]:
    response = dict()
    for model in models.__all__:
        key = getattr(models, model).__tablename__
        value = getattr(models, model).__table__.c.keys()
        response[key] = value
    return response
