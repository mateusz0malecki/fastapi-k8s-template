ARG     PYTHON_VER=3.11

FROM    python:${PYTHON_VER} AS fast-api-back

WORKDIR /app

COPY    backend /app

RUN     pip install -r requirements.txt

EXPOSE  8000

CMD     ["bash", "-c", "python run_prod.py"]