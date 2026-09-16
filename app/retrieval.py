"""Small deterministic hybrid retrieval implementation for local demonstration."""

from collections import Counter
from math import sqrt
import re

from .chunking import Chunk


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _cosine(left: Counter[str], right: Counter[str]) -> float:
    dot = sum(value * right[token] for token, value in left.items())
    left_norm = sqrt(sum(value * value for value in left.values()))
    right_norm = sqrt(sum(value * value for value in right.values()))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


class HybridIndex:
    def __init__(self) -> None:
        self._chunks: list[Chunk] = []

    def add(self, chunks: list[Chunk]) -> None:
        self._chunks.extend(chunks)

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        query_tokens = _tokens(query)
        query_counter = Counter(query_tokens)
        query_set = set(query_tokens)
        scored: list[tuple[float, Chunk]] = []

        for chunk in self._chunks:
            chunk_tokens = _tokens(f"{chunk.section} {chunk.text}")
            keyword_score = len(query_set.intersection(chunk_tokens)) / max(len(query_set), 1)
            semantic_score = _cosine(query_counter, Counter(chunk_tokens))
            score = 0.55 * semantic_score + 0.45 * keyword_score
            scored.append((score, chunk))

        scored.sort(key=lambda item: (-item[0], item[1].position))
        return [
            {
                "score": round(score, 4),
                "text": chunk.text,
                "source": chunk.source,
                "section": chunk.section,
                "position": chunk.position,
            }
            for score, chunk in scored[:top_k]
            if score > 0
        ]
