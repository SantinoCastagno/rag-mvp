# RAG Lab

Este proyecto es un sistema modular de Generación Aumentada por Recuperación (RAG), que demuestra:
- **LLM / Embeddings:** Agnóstico al proveedor mediante patrón factory — soporta **Google Gemini** (por defecto) y **Ollama**. Se cambia con la variable de entorno `LLM_PROVIDER`.
- **Vector Store:** ChromaDB (persistencia local)
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Trazabilidad/Evaluación:** Arize Phoenix
- **Característica clave:** Historial de chat persistente entre sesiones usando SQLite.

## Configuración

1. **Instalar dependencias:**
   ```bash
   poetry install
   ```

2. **Variables de entorno:**
   Crear un archivo `.env` copiando `.env.example` y configurar el proveedor. `GOOGLE_API_KEY` solo es necesaria cuando `LLM_PROVIDER=gemini`.
   ```bash
   cp .env.example .env
   # Editar .env: definir LLM_PROVIDER y las credenciales/URLs correspondientes
   ```

## Ejecutar la aplicación

Este proyecto usa un `Makefile` para simplificar la ejecución de los distintos servicios. Es necesario iniciar el servidor Phoenix, el backend FastAPI y el frontend Streamlit.

### 1. Iniciar Arize Phoenix (opcional pero recomendado para trazabilidad)
```bash
make phoenix
```
*Interfaz de Phoenix en http://localhost:6006*

### 2. Iniciar el Backend (FastAPI)
```bash
make api
```
*Documentación de la API en http://localhost:8000/docs*

### 3. Iniciar el Frontend (Streamlit)
```bash
make ui
```
*Chatbot disponible en http://localhost:8501*

## Uso

1. Abrí la app de Streamlit en el navegador (luego de ejecutar `make ui`).
2. Subí un archivo PDF o Markdown desde el panel lateral.
3. Hacé clic en "Ingest File".
4. Hacé preguntas en el chat. El historial de conversación se guardará para tu sesión.

## Documentación

La documentación técnica detallada está disponible en el directorio [`docs/`](docs/):

- [Arquitectura](docs/ARCHITECTURE.md)
- [Flujos del sistema](docs/SYSTEM_FLOWS.md)
- [Modelos de datos](docs/DATA_MODELS.md)
- [Protocolo API](docs/PROTOCOL_API.md)

## Notas de desarrollo

- **Tests:** Los tests unitarios e de integración están fuera del alcance de este POC. El proyecto está pensado como demostración de un sistema RAG funcional, no como código de producción.
- **Trazabilidad:** Phoenix es opcional. Si no está corriendo, la API levanta igualmente con un warning en consola.
