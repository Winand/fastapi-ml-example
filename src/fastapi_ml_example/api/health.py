from fastapi import APIRouter

# note: `tags` is used in Swagger documentation for endpoint grouping
router = APIRouter(tags=["health"])

@router.get("/health")
async def health() -> dict[str, str]:
    "Check if app is alive."
    return {"status": "ok"}
