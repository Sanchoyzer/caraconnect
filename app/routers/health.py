from datetime import UTC, datetime
from typing import Final

from fastapi import APIRouter

from app import __VERSION__


health_router: APIRouter = APIRouter()
started: Final[str] = datetime.now(tz=UTC).isoformat()


@health_router.get('')
async def ready() -> dict[str, str]:
    return {'up_since': started, 'version': __VERSION__}
