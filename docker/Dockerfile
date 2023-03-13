ARG     PYTHON_VER=3.11

FROM    python:${PYTHON_VER} AS fast-api-back

WORKDIR /app

COPY    backend /app

RUN     pip install -r requirements.txt

EXPOSE  8000

CMD     ["bash", "-c", "wait-for-it --service db:5432 --timeout 60 && alembic upgrade head && python run_prod.py"]