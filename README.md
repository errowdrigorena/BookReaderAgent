# book_agent

MVP en Python para resumir capítulos de libros técnicos o de software desde línea de comandos.

## Qué hace

Envía cada fragmento a un LLM compatible con OpenAI, como OpenRouter.
- Genera resúmenes parciales y un resumen final consolidado.
- Guarda el resultado en Markdown.

## Estructura

```text
book_agent/
├── app/
│   ├── main.py
│   ├── llm.py
│   ├── models.py
│   └── markdown_writer.py
├── input/
├── output/
├── .env.example
├── requirements.txt
└── README.md
```

## Instalación

```bash
cd book_agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuración

Define estas variables de entorno:

- `LLM_BASE_URL`
- `LLM_API_KEY`
- `VERIFY_SSL` opcional, por defecto `true`

Puedes copiarlas desde el ejemplo incluido:

```bash
cp .env.example .env
```

Contenido de ejemplo:

```bash
LLM_BASE_URL="https://openrouter.ai/api/v1"
LLM_API_KEY="tu-api-key"
VERIFY_SSL="true"
```

`app/main.py` carga automáticamente el archivo `.env` si existe en la raíz del proyecto.

## Ejecución

```bash
python3 app/main.py \
  --input input/capitulo_01.md \
  --output output/capitulo_01_resumen.md \
  --model qwen2.5:7b
```

Opciones útiles:

- `--chunk-size`: tamaño máximo de cada fragmento en caracteres. Valor por defecto: `6000`.
- `--overlap`: solapamiento entre fragmentos. Valor por defecto: `400`.
- `--temperature`: temperatura del modelo. Valor por defecto: `0.2`.

## Formato de salida

El Markdown final contiene exactamente estas secciones:

1. Resumen ejecutivo
2. Ideas clave
3. Cosas accionables
4. Humo / debilidades / relleno
5. Conceptos a revisar
6. Veredicto final

El veredicto final solo puede ser uno de estos valores:

- fundamentado
- poco basado
- ingenuo
- acertado
- extraordinario

## Decisiones de diseño

- Sin frameworks: el flujo es directo y fácil de leer.
- Sin Pydantic: la validación manual alcanza para este MVP y evita otra dependencia.
- JSON en las respuestas: reduce fragilidad y hace más simple la consolidación.
- Cliente genérico de chat completions: facilita cambiar de proveedor sin tocar el resto del proyecto.

## Mejoras futuras posibles

1. Añadir reintentos con backoff para errores de red.
2. Permitir ajustar el prompt desde archivos externos.
3. Guardar también el JSON intermedio de cada fragmento para depuración.
4. Añadir un modo `--dry-run` que solo trocee y muestre fragmentos.
5. Incorporar soporte opcional para streaming si el proveedor lo permite.
