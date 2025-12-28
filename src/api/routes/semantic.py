# src/api/routes/semantic.py

from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.semantic_service import SemanticService
from src.core.database import get_db

router = APIRouter()   # ✅ You forgot this earlier

@router.get("/semantic")
async def semantic_search(
    q: str = Query(..., description="Search query"),
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    return await SemanticService.search(q, limit, db)
