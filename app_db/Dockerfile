FROM postgres:16.2

# Copy config to the container
COPY ./postgresql.conf /etc/postgresql/postgresql.conf

# Copy the initialization scripts to the container
COPY ./init_scripts/*.sql /docker-entrypoint-initdb.d/
COPY ./init_scripts/*.sh /docker-entrypoint-initdb.d/
COPY ./init_scripts/00_01_init.sh /app/prestart.sh

RUN pip install sqlalchemy psycopg2-binary --no-cache-dir
