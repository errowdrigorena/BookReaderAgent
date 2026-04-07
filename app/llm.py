from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class LLMConfig:
    base_url: str
    api_key: str
    model: str
    timeout: float = 60.0
    verify_ssl: bool = True


class ChatCompletionsClient:
    def __init__(self, config: LLMConfig) -> None:
        self._config = config

    def chat_json(self, messages: list[dict[str, str]], temperature: float = 0.2) -> dict[str, Any]:
        payload = {
            "model": self._config.model,
            "messages": messages,
            "temperature": temperature,
        }

        response = requests.post(
            self._endpoint_url(),
            headers=self._headers(),
            json=payload,
            verify=self._config.verify_ssl,
            timeout=self._config.timeout,
        )
        
        if not response.ok:
            try:
                error_detail = response.json()
            except:
                error_detail = response.text
            raise ValueError(f"Error {response.status_code} desde {self._config.base_url}: {error_detail}")

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return self._load_json(content)

    def _endpoint_url(self) -> str:
        return self._config.base_url.rstrip("/") + "/chat/completions"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }

    def _load_json(self, content: str) -> dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}")
            if start == -1 or end == -1 or end <= start:
                return self._fallback_dict()

            extracted = content[start : end + 1]
            try:
                return json.loads(extracted)
            except json.JSONDecodeError:
                extracted = extracted.replace("\n", " ").replace("'", '"')
                try:
                    return json.loads(extracted)
                except json.JSONDecodeError:
                    return self._extract_with_regex(extracted)

    def _extract_with_regex(self, text: str) -> dict[str, Any]:
        result = {
            "resumen_ejecutivo": self._extract_field(text, "resumen_ejecutivo"),
            "ideas_clave": self._extract_list_field(text, "ideas_clave"),
            "cosas_accionables": self._extract_list_field(text, "cosas_accionables"),
            "humo_debilidades_relleno": self._extract_list_field(text, "humo_debilidades_relleno"),
            "conceptos_a_revisar": self._extract_list_field(text, "conceptos_a_revisar"),
            "veredicto_final": self._extract_field(text, "veredicto_final") or "poco basado",
        }
        if not result["resumen_ejecutivo"]:
            return self._fallback_dict()
        return result

    def _extract_field(self, text: str, field: str) -> str:
        pattern = rf'"{field}"\s*:\s*"([^"]*)"'
        match = re.search(pattern, text)
        return match.group(1) if match else ""

    def _extract_list_field(self, text: str, field: str) -> list[str]:
        pattern = rf'"{field}"\s*:\s*\[(.*?)\]'
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            return []
        items_text = match.group(1)
        items = re.findall(r'"([^"]*)"', items_text)
        return [item.strip() for item in items if item.strip()]

    def _fallback_dict(self) -> dict[str, Any]:
        return {
            "resumen_ejecutivo": "Resumen no disponible (error en respuesta del LLM)",
            "ideas_clave": [],
            "cosas_accionables": [],
            "humo_debilidades_relleno": [],
            "conceptos_a_revisar": [],
            "veredicto_final": "poco basado",
        }
