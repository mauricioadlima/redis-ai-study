from sentence_transformers import SentenceTransformer

from faq_index import get_faq_index

from redisvl.query import VectorQuery

import ollama

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

def pretty_print_results(results):
    print("\nTop matches:")
    for i, doc in enumerate(results, start=1):
        print(f"\n[{i}] Question: {doc['question']}")
        print(f"    Category: {doc.get('category', 'n/a')}")
        print(f"    Answer:   {doc['answer']}")
        print(f"    Distance:   {doc.get('vector_distance')}")


def main():
    index = get_faq_index("redis://localhost:6379")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    #model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    while True:
        raw_input = input("\nAsk RediCorp DoRQ a question (or type 'quit'): ").strip()
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


if __name__ == "__main__":
    main()