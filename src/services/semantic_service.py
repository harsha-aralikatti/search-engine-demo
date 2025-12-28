# src/services/semantic_service.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.product import Product

from src.core.embeddings import generate_local_embedding
from src.services.vector_service import vector_search


class SemanticService:

    @staticmethod
    async def search(query: str, limit: int, db: AsyncSession):
        # 1️⃣ Generate query embedding
        query_vector = generate_local_embedding(query)

        # 2️⃣ Vector search from Qdrant
        vector_results = await vector_search(query_vector, limit=limit)

        # Take top vector results product_ids
        vector_product_ids = [p.payload["product_id"] for p in vector_results]

        # 3️⃣ Keyword search (Postgres)
        stmt = select(Product).where(
            (Product.title.ilike(f"%{query}%")) |
            (Product.description.ilike(f"%{query}%"))
        ).limit(limit)

        keyword_products = (await db.execute(stmt)).scalars().all()

        # Convert to uniform format
        keyword_results = [
            {
                "product_id": p.id,
                "title": p.title,
                "description": p.description,
                "category": p.category,
                "price": p.price,
                "score": 0.5   # base keyword score
            }
            for p in keyword_products
        ]

        # Convert vector results
        vector_results_formatted = [
            {
                "product_id": r.payload["product_id"],
                "title": r.payload["title"],
                "description": r.payload["description"],
                "category": r.payload["category"],
                "price": r.payload["price"],
                "score": float(r.score)  # cosine similarity
            }
            for r in vector_results
        ]

        # 4️⃣ Combine + re-rank
        combined = {item["product_id"]: item for item in keyword_results}

        for v in vector_results_formatted:
            if v["product_id"] in combined:
                combined[v["product_id"]]["score"] += v["score"]  # boost
            else:
                combined[v["product_id"]] = v

        # Sort by score desc
        final_results = sorted(
            combined.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        return final_results[:limit]
