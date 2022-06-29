from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


from app.core import config, tasks
from app.api.routes import router as api_router


def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # event handlers for startup/shutdown of server
    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    # router for the app for API
    app.include_router(api_router, prefix=config.API_PREFIX)

    # no other routers because it is functionally just a http server
    return app


app = get_application()