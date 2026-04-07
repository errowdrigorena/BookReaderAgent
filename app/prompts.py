from __future__ import annotations

import json


FRAGMENT_SCHEMA = """
{
  \"resumen_ejecutivo\": \"Texto breve con la idea central del fragmento.\",
  \"ideas_clave\": [\"...\"],
  \"cosas_accionables\": [\"...\"],
  \"humo_debilidades_relleno\": [\"...\"],
  \"conceptos_a_revisar\": [\"...\"],
  \"veredicto_final\": \"fundamentado|poco basado|ingenuo|acertado|extraordinario\"
}
""".strip()


FINAL_SCHEMA = """
{
  \"resumen_ejecutivo\": \"Texto breve y sintético del capítulo completo.\",
  \"ideas_clave\": [\"...\"],
  \"cosas_accionables\": [\"...\"],
  \"humo_debilidades_relleno\": [\"...\"],
  \"conceptos_a_revisar\": [\"...\"],
  \"veredicto_final\": \"fundamentado|poco basado|ingenuo|acertado|extraordinario\"
}
""".strip()


def fragment_messages(fragment_text: str, fragment_number: int, total_fragments: int) -> list[dict[str, str]]:
    system = (
        "Eres un analista de capítulos técnicos. Devuelve solo JSON válido, sin markdown ni explicaciones. "
        "Sé preciso, sobrio y conciso. No inventes contenido no presente en el fragmento."
    )
    user = f"""
Analiza el fragmento {fragment_number}/{total_fragments} de un capítulo.

Devuelve exactamente este esquema JSON:
{FRAGMENT_SCHEMA}

Instrucciones:
- Resume solo lo que aporta este fragmento.
- Usa listas cortas y concretas.
- Si algo es relleno, débil o humo, dilo sin suavizarlo.
- El veredicto_final debe ser uno de: fundamentado, poco basado, ingenuo, acertado, extraordinario.

Fragmento:
{fragment_text}
""".strip()
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def final_messages(fragment_reports: list[dict]) -> list[dict[str, str]]:
    fragment_reports_json = json.dumps(fragment_reports, ensure_ascii=False, indent=2)
    system = (
        "Eres un analista de capítulos técnicos. Devuelve solo JSON válido, sin markdown ni explicaciones. "
        "Consolida los resúmenes parciales en una versión final sin redundancias."
    )
    user = f"""
Consolida estos resúmenes parciales en un único resumen final del capítulo.

Devuelve exactamente este esquema JSON:
{FINAL_SCHEMA}

Instrucciones:
- Fusiona ideas repetidas y elimina duplicados.
- Prioriza claridad y utilidad práctica.
- La sección \"humo_debilidades_relleno\" debe señalar con honestidad las partes flojas, vagas o repetitivas.
- \"conceptos_a_revisar\" debe listar términos o ideas que conviene estudiar después.
- El veredicto_final debe ser uno de: fundamentado, poco basado, ingenuo, acertado, extraordinario.
- No menciones los fragmentos ni el proceso de consolidación.

Resúmenes parciales:
{fragment_reports_json}
""".strip()
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]
