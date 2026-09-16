"""Structure-aware chunking utilities."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Chunk:
    text: str
    source: str
    section: str
    position: int


def chunk_markdown(content: str, source: str, max_words: int = 120) -> list[Chunk]:
    """Split Markdown by headings, then by word count while retaining metadata."""
    if max_words < 10:
        raise ValueError("max_words must be at least 10")

    chunks: list[Chunk] = []
    section = "Document"
    buffer: list[str] = []
    position = 0

    def flush() -> None:
        nonlocal buffer, position
        words = " ".join(buffer).split()
        for start in range(0, len(words), max_words):
            text = " ".join(words[start : start + max_words]).strip()
            if text:
                chunks.append(Chunk(text=text, source=source, section=section, position=position))
                position += 1
        buffer = []

    for raw_line in content.splitlines():
        line = raw_line.strip()
        heading = re.match(r"^#{1,6}\s+(.+)$", line)
        if heading:
            flush()
            section = heading.group(1).strip()
        elif line:
            buffer.append(line)
    flush()
    return chunks
