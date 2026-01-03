from fastapi import APIRouter

router = APIRouter(prefix="/app")


@router.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}
