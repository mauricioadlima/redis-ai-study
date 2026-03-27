from sentence_transformers import SentenceTransformer

from faq_index import get_faq_index, get_semantic_index

from redisvl.query import VectorQuery

import numpy as np
import uuid
import ollama
import time

def ask_ollama(user_query, results):
    context = "\n".join([f"FAQ: {r['question']} - Ans: {r['answer']}" for r in results])
    
    prompt = f"""
    Use the context below to answer the user question in a friendly way.
    If the context doesn't have the answer, say you don't know.
    
    Context: {context}
    User Question: {user_query}
    
    Answer (in Portuguese):"""

    response = ollama.generate(model='tinyllama', prompt=prompt)
    return response['response']

def add_to_semantic_cache(index, model, user_query_vec, ai_answer):
    q_vec_bytes = np.array(user_query_vec, dtype=np.float32).tobytes()

    cache_id = f"cache:{uuid.uuid4().hex}"

    cache_doc = {
        "key": cache_id,
        "answer": ai_answer,
        "embedding": q_vec_bytes
    }

    index.load([cache_doc])

def check_semantic_cache(index, q_vec, threshold=0.1):
    query = VectorQuery(
        vector=q_vec,
        vector_field_name="embedding",
        return_fields=["question", "answer"],
        num_results=1
    )
    
    results = index.query(query)
    
    if results and float(results[0]['vector_distance']) <= threshold:
        return results[0]
    
    return None

def pretty_print_results(results):
    print("\nTop matches:")
    for i, doc in enumerate(results, start=1):
        print(f"\n[{i}] Question: {doc['question']}")
        print(f"    Category: {doc.get('category', 'n/a')}")
        print(f"    Answer:   {doc['answer']}")
        print(f"    Distance:   {doc.get('vector_distance')}")


def main():
    index = get_faq_index()
    index_semantic = get_semantic_index()

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    #model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    while True:
        raw_input = input("\nAsk RediCorp DoRQ a question (or type 'quit'): ").strip()
        start_time = time.time()
        if raw_input.lower() in ("quit", "exit"):
            break

        if ":" in raw_input:
            tech, user_query = raw_input.split(":", 1)
            tech = tech.strip().lower()
        else:
            tech = "redis"
            user_query = raw_input

        # 1) Embed the query locally (no LLM, just a sentence-transformer)
        q_vec = model.encode([user_query]).tolist()[0]


        # 1) Try semantic cache first
        cached_res = check_semantic_cache(index_semantic, q_vec)

        if cached_res:
            print(f"\n🚀 [CACHE HIT] Distância: {cached_res['vector_distance']}")
            print(f"✨ AI ANSWER (Cached): {cached_res['answer']}")
            end_time = time.time()
            duration = end_time - start_time
            print(f"⏱️ Response time: {duration:.4f} seconds")
            continue

        query = VectorQuery(
            vector=q_vec,
            vector_field_name="embedding", 
            return_fields=["question", "answer", "category"],
            num_results=3,
            filter_expression=f"@technology:{{\"{tech}\"}}",
            ef_runtime=10
        )

        # 2) Vector search against Redis
        results = index.query(query)

        # 3) Display results
        pretty_print_results(results)

        ai_answer = ask_ollama(user_query, results)
        print(f"\n✨ AI ANSWER: {ai_answer}")

        end_time = time.time()
        duration = end_time - start_time
        print(f"⏱️ Response time: {duration:.4f} seconds")

        add_to_semantic_cache(index_semantic, model, q_vec, ai_answer)


if __name__ == "__main__":
    main()