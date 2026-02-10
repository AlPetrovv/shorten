from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from lifespan import lifespan
from routers import api_router


def create_app():
    app = FastAPI(
        title="Shorten",
        description="Welcome to the Shorten API",
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    app.include_router(api_router)

    return app


main_app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:main_app", host="0.0.0.0", reload=True)
