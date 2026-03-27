FAQ_DOCS = [
    {
        "key": "faq:1",
        "question": "Is Redis just a cache or can it be a primary database?",
        "answer": (
            "Redis is commonly used as a cache, but it can also serve as a primary "
            "database for many workloads. It supports persistence, replication, and "
            "high availability in Redis Enterprise and Redis Cloud."
        ),
        "category": "concepts",
        "technology": "redis"
    },
    {
        "key": "faq:2",
        "question": "How do I connect to Redis from Python?",
        "answer": (
            "Use the redis-py client. For example: "
            "import redis; r = redis.Redis(host='localhost', port=6379, decode_responses=True); "
            "r.set('key', 'value')."
        ),
        "category": "client",
        "technology": "redis"
    },
    {
        "key": "faq:3",
        "question": "How does Redis store data in memory and still persist it?",
        "answer": (
            "Redis stores data in memory for speed, and uses persistence mechanisms "
            "like RDB snapshots and AOF logs to persist data to disk."
        ),
        "category": "persistence",
        "technology": "redis"
    },
    {
        "key": "faq:4",
        "question": "What are some common use cases for Redis?",
        "answer": (
            "Common use cases include caching, session storage, real-time analytics, "
            "leaderboards, queues, and as a vector database for AI applications."
        ),
        "category": "use-cases",
        "technology": "redis"
    },
    {
        "key": "faq:5",
        "question": "Can Redis store vectors for semantic search?",
        "answer": (
            "Yes. Modern Redis supports vector fields and vector indices so you can "
            "store embeddings and run similarity search directly in Redis."
        ),
        "category": "vectors",
        "technology": "redis"
    },
    {
        "key": "faq:6",
        "question": "What is the difference between a Clustered and a Non-Clustered index in SQL Server?",
        "answer": (
            "A Clustered index determines the physical order of data in a table (one per table), "
            "while a Non-Clustered index is a separate structure from the data rows that contains "
            "pointers to the actual data, similar to an index in a book."
        ),
        "category": "indexing",
        "technology": "sql-server"
    },
    {
        "key": "faq:7",
        "question": "How can I improve query performance using Execution Plans?",
        "answer": (
            "Execution Plans show how the SQL Server query optimizer executes a query. By analyzing "
            "them, you can identify bottlenecks like Table Scans, missing indexes, or expensive "
            "joins, allowing you to refactor the T-SQL or add necessary indexes."
        ),
        "category": "performance",
        "technology": "sql-server"
    },
    {
        "key": "faq:8",
        "question": "What is the purpose of Always On Availability Groups?",
        "answer": (
            "Always On Availability Groups is a high-availability and disaster-recovery solution "
            "that provides an enterprise-level alternative to database mirroring. It allows for "
            "multiple readable secondary replicas and automatic failover."
        ),
        "category": "high-availability",
        "technology": "sql-server"
    }
]
