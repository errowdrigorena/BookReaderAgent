from __future__ import annotations

import argparse
import os
from pathlib import Path

from chunking import split_text
from document_reader import read_document
from llm import ChatCompletionsClient, LLMConfig
from markdown_writer import write_markdown
from models import FinalReport, FragmentSummary, final_report_from_dict, fragment_summary_from_dict
from prompts import final_messages, fragment_messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agente local para resumir capítulos de libros técnicos")
    parser.add_argument("--input", required=True, help="Archivo .txt, .md, .pdf o .epub de entrada")
    parser.add_argument("--output", required=True, help="Archivo Markdown de salida")
    parser.add_argument("--model", required=True, help="Nombre del modelo compatible con OpenAI")
    parser.add_argument("--chunk-size", type=int, default=6000, help="Tamaño máximo de cada fragmento en caracteres")
    parser.add_argument("--overlap", type=int, default=400, help="Solapamiento entre fragmentos en caracteres")
    parser.add_argument("--temperature", type=float, default=0.2, help="Temperatura del modelo")
    return parser.parse_args()


def load_env_file(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.is_file():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or key in os.environ:
            continue

        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]

        os.environ[key] = value


def build_llm(model: str) -> ChatCompletionsClient:
    base_url = os.environ.get("LLM_BASE_URL")
    api_key = os.environ.get("LLM_API_KEY")
    if not base_url:
        raise EnvironmentError("Falta la variable de entorno LLM_BASE_URL")
    if not api_key:
        raise EnvironmentError("Falta la variable de entorno LLM_API_KEY")

    verify_ssl = os.environ.get("VERIFY_SSL", "true").lower() != "false"
    return ChatCompletionsClient(LLMConfig(
        base_url=base_url,
        api_key=api_key,
        model=model,
        verify_ssl=verify_ssl
    ))


def summarize_fragments(llm: ChatCompletionsClient, chunks: list[str], temperature: float) -> list[FragmentSummary]:
    fragment_summaries: list[FragmentSummary] = []
    total_chunks = len(chunks)

    for index, chunk in enumerate(chunks, start=1):
        print(f"Procesando fragmento {index}/{total_chunks}...")
        result = llm.chat_json(fragment_messages(chunk, index, total_chunks), temperature=temperature)
        fragment_summaries.append(fragment_summary_from_dict(result))

    return fragment_summaries


def consolidate_report(llm: ChatCompletionsClient, fragment_summaries: list[FragmentSummary], temperature: float) -> FinalReport:
    fragment_reports = [summary.__dict__ for summary in fragment_summaries]
    result = llm.chat_json(final_messages(fragment_reports), temperature=temperature)
    return final_report_from_dict(result)


def main() -> None:
    load_env_file()
    args = parse_args()
    text = read_document(args.input)
    chunks = split_text(text, args.chunk_size, args.overlap)

    if not chunks:
        raise ValueError("El archivo de entrada está vacío")

    llm = build_llm(args.model)
    fragment_summaries = summarize_fragments(llm, chunks, args.temperature)
    final_report = consolidate_report(llm, fragment_summaries, args.temperature)
    write_markdown(args.output, final_report)
    print(f"Resumen guardado en {args.output}")


if __name__ == "__main__":
    main()
