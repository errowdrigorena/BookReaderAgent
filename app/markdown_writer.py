from __future__ import annotations

from pathlib import Path

from models import FinalReport


def render_markdown(report: FinalReport) -> str:
    lines: list[str] = [
        "## Resumen ejecutivo",
        report.resumen_ejecutivo,
        "",
        "## Ideas clave",
        *[f"- {item}" for item in report.ideas_clave],
        "",
        "## Cosas accionables",
        *[f"- {item}" for item in report.cosas_accionables],
        "",
        "## Humo / debilidades / relleno",
        *[f"- {item}" for item in report.humo_debilidades_relleno],
        "",
        "## Conceptos a revisar",
        *[f"- {item}" for item in report.conceptos_a_revisar],
        "",
        "## Veredicto final",
        report.veredicto_final,
        "",
    ]
    return "\n".join(lines)


def write_markdown(path: str | Path, report: FinalReport) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown(report), encoding="utf-8")
