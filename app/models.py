from __future__ import annotations

from dataclasses import dataclass


ALLOWED_VERDICTS = {
    "fundamentado",
    "poco basado",
    "ingenuo",
    "acertado",
    "extraordinario",
}


@dataclass(frozen=True)
class FragmentSummary:
    resumen_ejecutivo: str
    ideas_clave: list[str]
    cosas_accionables: list[str]
    humo_debilidades_relleno: list[str]
    conceptos_a_revisar: list[str]
    veredicto_final: str


@dataclass(frozen=True)
class FinalReport:
    resumen_ejecutivo: str
    ideas_clave: list[str]
    cosas_accionables: list[str]
    humo_debilidades_relleno: list[str]
    conceptos_a_revisar: list[str]
    veredicto_final: str


def normalize_verdict(value: str) -> str:
    verdict = value.strip().lower()
    if verdict not in ALLOWED_VERDICTS:
        raise ValueError(f"Veredicto no válido: {value}")
    return verdict


def ensure_string(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"El campo {field_name} debe ser un texto no vacío")
    return value.strip()


def ensure_string_list(value: object, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"El campo {field_name} debe ser una lista")

    items: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"El campo {field_name} solo puede contener textos no vacíos")
        items.append(item.strip())
    return items


def fragment_summary_from_dict(data: dict) -> FragmentSummary:
    return FragmentSummary(
        resumen_ejecutivo=ensure_string(data["resumen_ejecutivo"], "resumen_ejecutivo"),
        ideas_clave=ensure_string_list(data["ideas_clave"], "ideas_clave"),
        cosas_accionables=ensure_string_list(data["cosas_accionables"], "cosas_accionables"),
        humo_debilidades_relleno=ensure_string_list(data["humo_debilidades_relleno"], "humo_debilidades_relleno"),
        conceptos_a_revisar=ensure_string_list(data["conceptos_a_revisar"], "conceptos_a_revisar"),
        veredicto_final=normalize_verdict(ensure_string(data["veredicto_final"], "veredicto_final")),
    )


def final_report_from_dict(data: dict) -> FinalReport:
    return FinalReport(
        resumen_ejecutivo=ensure_string(data["resumen_ejecutivo"], "resumen_ejecutivo"),
        ideas_clave=ensure_string_list(data["ideas_clave"], "ideas_clave"),
        cosas_accionables=ensure_string_list(data["cosas_accionables"], "cosas_accionables"),
        humo_debilidades_relleno=ensure_string_list(data["humo_debilidades_relleno"], "humo_debilidades_relleno"),
        conceptos_a_revisar=ensure_string_list(data["conceptos_a_revisar"], "conceptos_a_revisar"),
        veredicto_final=normalize_verdict(ensure_string(data["veredicto_final"], "veredicto_final")),
    )
