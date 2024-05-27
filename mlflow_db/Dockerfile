FROM postgres:16.2
RUN echo "ENVIRONMENT: $ENVIRONMENT"

# Copy the initialization scripts to the container
COPY ./init_scripts/*.sql /docker-entrypoint-initdb.d/
COPY ./init_scripts/*.sh /docker-entrypoint-initdb.d/
COPY ./init_scripts/00_01_init.sh /app/prestart.sh

RUN pip3 install sqlalchemy psycopg[binary] --no-cache-dir
