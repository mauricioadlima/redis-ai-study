from typing import List

from sentence_transformers import SentenceTransformer
from redisvl.index import SearchIndex

from faq_data import FAQ_DOCS
from faq_index import get_faq_index, get_semantic_index

import numpy as np


def build_embeddings(texts: List[str]) -> List[list]:
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    #model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
    vectors = model.encode(texts)
    return [vec.astype(np.float32).tobytes() for vec in vectors]


def main():
    # 1) Connect / create index
    index: SearchIndex = get_faq_index()

    # Drop index if it exists (to make reruns easy)
    if index.exists():
        index.delete()

    index.create()
    print("Created index:", index.name)

    # 2) Prepare texts to embed (question + answer)
    texts = [
        f"{doc['question']} {doc['answer']}"
        for doc in FAQ_DOCS
    ]
    vectors = build_embeddings(texts)

    # 3) Build RedisVL documents
    docs = []
    for doc, vec in zip(FAQ_DOCS, vectors):
        docs.append({
            "key": doc["key"],            
            "question": doc["question"],
            "answer": doc["answer"],
            "category": doc["category"],
            "technology": doc["technology"],
            "embedding": vec
        })

   
    semantic_index: SearchIndex = get_semantic_index()
    
    if semantic_index.exists():
        semantic_index.delete()

    semantic_index.create()


if __name__ == "__main__":
    main()