import asyncio
import logging
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from project.core.config import settings
from project.api.clients_routes import router as clients_router
from project.api.hotels_routes import router as hotels_router
from project.api.roomtype_routes import router as roomtypes_router
from project.api.rooms_routes import router as rooms_router
from project.api.bookings_routes import router as bookings_router
from project.api.stays_routes import router as stays_router
from project.api.service_routes import router as services_router
from project.api.service_usage_routes import router as service_usage_router
from project.api.feedback_routes import router as feedback_router
from project.api.payment_types_routes import router as payment_types_router
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app_options = {}
    if settings.ENV.lower() == "prod":
        app_options = {
            "docs_url": None,
            "redoc_url": None,
        }
    if settings.LOG_LEVEL in ["DEBUG", "INFO"]:
        app_options["debug"] = True

    app = FastAPI(root_path=settings.ROOT_PATH, **app_options)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключение всех маршрутов
    app.include_router(clients_router, prefix="/api", tags=["Clients APIs"])
    app.include_router(hotels_router, prefix="/api", tags=["Hotels APIs"])
    app.include_router(roomtypes_router, prefix="/api", tags=["RoomTypes APIs"])
    app.include_router(rooms_router, prefix="/api", tags=["Rooms APIs"])
    app.include_router(bookings_router, prefix="/api", tags=["Bookings APIs"])
    app.include_router(stays_router, prefix="/api", tags=["Stays APIs"])
    app.include_router(services_router, prefix="/api", tags=["Services APIs"])
    app.include_router(service_usage_router, prefix="/api", tags=["Service Usage APIs"])
    app.include_router(feedback_router, prefix="/api", tags=["Feedback APIs"])
    app.include_router(payment_types_router, prefix="/api", tags=["Payment Types APIs"])
    return app


app = create_app()


async def run() -> None:
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    logger.debug(f"{settings.postgres_url}=")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
