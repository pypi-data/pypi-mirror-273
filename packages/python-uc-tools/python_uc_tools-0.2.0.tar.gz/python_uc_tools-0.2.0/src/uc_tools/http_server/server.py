from fastapi import FastAPI

from .routes import base_router


class HttpServer:
    """
    The HttpServer class is used to create a FastAPI application for an HTTP server.

    It has one method, __init__, which is used to create a FastAPI application and
    include the base router.
    """

    def __init__(self) -> None:
        """
        Initialize the HttpServer.

        This method creates a FastAPI application and includes the base router.

        Returns:
            None
        """
        self.app = FastAPI()
        self.app.include_router(base_router)
