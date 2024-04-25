from os import getenv
from fastapi import FastAPI, APIRouter
#
# from .database.config import engine, BaseModel

from ..jp_app.routes.user_route import router as user_router
from ..jp_app.routes.user_route import feature_flag as user_flag
from backend.src.jp_app.database.config import init_db


def router_feature_toggle(application: FastAPI, router: APIRouter, flag: str) -> None:
    """
    Enable/Disable route based on feature_flag environmental variable
    Defaults to: 'ON'

    :param application: application to be included the router
    :param router: router with endpoints
    :param flag: env var to be searched for
    :return: None
    """
    if getenv(key=flag, default="ON").upper() == "ON":
        application.include_router(router)


def get_application() -> FastAPI:
    tags = [
        {
            "name": "user",
            "description": "These are routes related for user"
        },
        {
            "name": "product",
            "description": "These are routes related for product"
        },
        {
            "name": "order",
            "description": "These are routes related for order"
        }
    ]
    init_db()
    application = FastAPI(title="JPS API",
                          openapi_tags=tags)
    router_feature_toggle(application, user_router, user_flag)
    return application


app = get_application()
