FROM python:3.11.7-slim as base
RUN python -m pip install --upgrade --no-cache-dir pip wheel setuptools \
    && python -m pip install poetry \
    && poetry config virtualenvs.create false \
    && mkdir -p /srv/src

ENV PYTHONPATH=/srv/src
WORKDIR /srv/src

COPY pyproject.toml poetry.lock ./
RUN poetry install --only=main


FROM base as development
COPY app ./app
CMD uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload


FROM development as test
RUN poetry install --only=test
COPY tests ./tests
CMD python -m pytest --durations=3 .


FROM base as production
COPY app ./app
CMD gunicorn app.main:app --timeout 120 --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080
