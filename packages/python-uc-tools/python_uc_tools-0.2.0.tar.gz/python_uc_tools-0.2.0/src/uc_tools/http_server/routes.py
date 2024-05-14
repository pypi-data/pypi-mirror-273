from fastapi import APIRouter, Response

base_router = APIRouter()


@base_router.get('/health', summary='Health check')
async def healthcheck():
    return Response(status_code=200, content='OK')
