from app.chunking import Chunk
from app.retrieval import HybridIndex


def test_hybrid_search_prioritizes_relevant_chunk() -> None:
    index = HybridIndex()
    index.add([
        Chunk("Employees receive 20 paid leave days.", "policy.md", "Leave", 0),
        Chunk("Expense claims require receipts.", "finance.md", "Expenses", 1),
    ])
    results = index.search("paid leave days", top_k=1)
    assert results[0]["source"] == "policy.md"
