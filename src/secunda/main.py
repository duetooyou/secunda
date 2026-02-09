from fastapi import FastAPI

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka


from secunda.infra.ioc import (
    ConfigProvider,
    DatabaseProvider,
    InteractorProvider,
    RepositoryProvider,
)
from secunda.presentation.routers import api_router


container = make_async_container(
        ConfigProvider(),
        DatabaseProvider(),
        RepositoryProvider(),
        InteractorProvider(),
    )

def create_app() -> FastAPI:

    fastapi_app = FastAPI(
        title="Secunda API",
        description="REST API тестовое",
        version="1.0.0",
    )
    setup_dishka(container=container, app=fastapi_app)
    fastapi_app.include_router(api_router)

    return fastapi_app


app = create_app()


def main():
    import uvicorn

    uvicorn.run("secunda.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
