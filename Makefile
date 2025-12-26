.PHONY: install api ui phoenix clean test lint

# Variables
PYTHON_EXEC = poetry run python
UVICORN_EXEC = poetry run uvicorn
STREAMLIT_EXEC = poetry run streamlit

# Instalación de dependencias
install:
	poetry install

# Ejecutar el servidor de trazas (Phoenix)
phoenix:
	$(PYTHON_EXEC) -m phoenix.server.main serve

# Ejecutar el Backend (FastAPI)
api:
	$(UVICORN_EXEC) app.api.main:app --reload --port 8000

# Ejecutar el Frontend (Streamlit)
ui:
	$(STREAMLIT_EXEC) run app/ui/app.py

# Limpiar archivos temporales y cache
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Ejecutar chequeos (ejemplo futuro)
lint:
	poetry run ruff check .
