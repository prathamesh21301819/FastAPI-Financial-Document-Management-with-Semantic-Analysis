from reranker import rerank

results = [
    "Infosys revenue increased by 15%",
    "Infosys employee count increased",
    "Operating margin improved"
]

ranked = rerank(
    "What was Infosys revenue growth?",
    results
)

print(ranked[0])