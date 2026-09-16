from app.chunking import chunk_markdown


def test_headings_are_preserved_as_metadata() -> None:
    chunks = chunk_markdown("# Policy\nUse approved tools.\n## Security\nNever share secrets.", "guide.md")
    assert [chunk.section for chunk in chunks] == ["Policy", "Security"]
    assert all(chunk.source == "guide.md" for chunk in chunks)
