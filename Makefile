.PHONY: install run test ui fmt lint

install:
	pip install -U pip
	pip install -r backend/requirements.txt

run:
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

ui:
	streamlit run ui/streamlit_app.py --server.port 8501

test:
	pytest -q

fmt:
	ruff check --fix || true
	black . || true

lint:
	ruff check . || true
