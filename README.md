# Ajaia Docs

Editor local-first para el assignment.

## Run

    cd ajaia-docs-assignment
    python3 app.py

Abre http://127.0.0.1:8000.

## Cuentas demo

Ivan (ivan) es propietario y puede crear, editar, guardar, importar y compartir. Grace (grace) solo ve documentos compartidos explícitamente y los viewer son de solo lectura. El selector simula el login. La persistencia está en data.json.

## Incluye

Creación, renombrado, rich text, guardado, persistencia, importación TXT/MD, ownership/shared badges, enforcement viewer en backend, comentarios visibles, historial, exportación Markdown, presencia por heartbeat/polling y layout responsive.

## Verificación

    python3 -m py_compile app.py
    python3 -m unittest -v test_app.py

## Arquitectura y límites

Servidor HTTP Python sin dependencias + cliente HTML estático + data.json. Se priorizó reproducibilidad y profundidad del flujo principal. No incluye autenticación real, SQLite, WebSockets/Yjs, resolución de conflictos ni parser DOCX completo. Siguientes pasos: sesiones reales, sanitización server-side, SQLite y colaboración realtime.
