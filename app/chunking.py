from __future__ import annotations


def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size debe ser mayor que 0")
    if overlap < 0:
        raise ValueError("overlap no puede ser negativo")
    if overlap >= chunk_size:
        raise ValueError("overlap debe ser menor que chunk_size")

    cleaned = text.strip()
    if not cleaned:
        return []

    chunks: list[str] = []
    start = 0
    text_length = len(cleaned)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        if end < text_length:
            break_at = cleaned.rfind(" ", start, end)
            if break_at > start + chunk_size // 2:
                end = break_at

        chunk = cleaned[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = max(0, end - overlap)
        while start < text_length and cleaned[start].isspace():
            start += 1

    return chunks
