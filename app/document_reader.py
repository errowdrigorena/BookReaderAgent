from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub
from pypdf import PdfReader


SUPPORTED_INPUT_SUFFIXES = {".txt", ".md", ".pdf", ".epub"}


def read_document(path: str) -> str:
    input_path = Path(path)
    suffix = input_path.suffix.lower()

    if suffix not in SUPPORTED_INPUT_SUFFIXES:
        allowed = ", ".join(sorted(SUPPORTED_INPUT_SUFFIXES))
        raise ValueError(f"La entrada debe ser uno de estos formatos: {allowed}")

    if suffix in {".txt", ".md"}:
        return input_path.read_text(encoding="utf-8")
    if suffix == ".pdf":
        return _read_pdf(input_path)
    return _read_epub(input_path)


def _read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages.append(text.strip())
    return "\n\n".join(pages)


def _read_epub(path: Path) -> str:
    book = epub.read_epub(str(path))
    documents: list[str] = []

    for item in book.get_items_of_type(ITEM_DOCUMENT):
        html = item.get_content().decode("utf-8", errors="ignore")
        text = BeautifulSoup(html, "html.parser").get_text(separator=" ", strip=True)
        if text:
            documents.append(text)

    return "\n\n".join(documents)
