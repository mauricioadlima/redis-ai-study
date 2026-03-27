from redisvl.index import SearchIndex

FAQ_INDEX_SCHEMA = {
    "index": {
        "name": "faq_index",
        "prefix": "faq:"      # all docs will use keys starting with this
    },
    "fields": [
        {"name": "question", "type": "text"},
        {"name": "answer", "type": "text"},
        {"name": "category", "type": "tag"},
        {"name": "technology", "type": "tag"},
        {
            "name": "embedding",
            "type": "vector",
            "attrs": {
                "dims": 384, # 384, 768
                "algorithm": "hnsw", # hnsw, flat
                "distance_metric": "cosine" # cosine = text, l2 = images, ip = recommendation
            }
        }
    ]
}


def get_faq_index(redis_url: str = "redis://localhost:6379") -> SearchIndex:
    return SearchIndex.from_dict(FAQ_INDEX_SCHEMA, redis_url=redis_url)
