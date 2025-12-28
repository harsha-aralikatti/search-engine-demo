# src/services/learning_service.py

def compute_behavior_score(product):
    """
    Convert product behavioral signals into a normalized score.
    Weighted scoring based on business logic.
    """

    return (
        product.click_count * 0.5 +
        product.cart_count * 1.2 +
        product.purchase_count * 3.0 +
        product.total_dwell_time * 0.02 -
        product.bounce_count * 0.5
    )


def apply_behavioral_ranking(products, similarity_map):
    """
    Combine vector similarity + behavior score
    Return sorted products with explanation
    """

    ranked_results = []

    for p in products:
        sim = similarity_map.get(str(p.id), 0)

        behavior = compute_behavior_score(p)

        # Final ranking (simple weighted sum)
        final = sim * 0.7 + behavior * 0.3

        ranked_results.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "category": p.category,
            "price": p.price,
            "rating": p.rating,
            "attributes": p.attributes,

            # raw behavior signals
            "click_count": p.click_count,
            "cart_count": p.cart_count,
            "purchase_count": p.purchase_count,
            "total_dwell_time": p.total_dwell_time,
            "bounce_count": p.bounce_count,

            # ranking signals
            "similarity_score": sim,
            "behavior_score": behavior,
            "final_score": final,

            # human-readable explanation
            "explanation": f"Similarity: {round(sim,3)}, BehaviorScore: {round(behavior,3)}"
        })

    # Sort by final score descending
    ranked_results.sort(key=lambda x: x["final_score"], reverse=True)

    return ranked_results
