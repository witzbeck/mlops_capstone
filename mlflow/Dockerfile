FROM ghcr.io/mlflow/mlflow:v2.13.0

RUN pip3 install --user --no-cache-dir psycopg2 sqlalchemy

RUN python3 -c "import site; print(site.getusersitepackages())"
RUN python3 -c "import sys; print(sys.path)"

RUN python3 -c "import psycopg2; print('psycopg2 import successful')"

# Set the working directory
RUN ls -la

RUN echo "POSTGRES_USER: $POSTGRES_USER"

ENV POSTGRES_USER=mlflow

RUN echo "POSTGRES_USER: $POSTGRES_USER"
