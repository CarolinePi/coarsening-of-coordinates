FROM python:3.9-slim

WORKDIR /app


ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV MYPYPATH "${MYPYPATH}:/app"
ENV CONFIG_PATH "config/pytest.yaml"


COPY requirements/requirements.txt .
COPY requirements/requirements-tests.txt .
COPY api api
COPY bl bl
COPY dl dl
COPY tests tests
COPY config.py .
COPY config/config.yaml .
COPY main.py .
COPY .flake8 .
COPY mypy.ini .
EXPOSE 8080

RUN pip install -r requirements.txt
RUN pip install -r requirements-tests.txt
