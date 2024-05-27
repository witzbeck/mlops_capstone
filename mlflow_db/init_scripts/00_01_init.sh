#!/bin/bash
# Connect to the default database 'postgres' and execute the commands
psql -U postgres -d postgres -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"
psql -U postgres -d postgres -c "DROP DATABASE IF EXISTS $POSTGRES_DB;"
psql -U postgres -d postgres -c "CREATE DATABASE $POSTGRES_DB;"
psql -U postgres -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;"

# Applying database migrations for MLflow
echo "Applying database migrations for MLflow"
mlflow db upgrade postgresql+psycopg2://$MLFLOW_TRACKING_USER:$MLFLOW_TRACKING_PASSWORD@$MLFLOW_TRACKING_HOST:$MLFLOW_TRACKING_PORT/$MLFLOW_TRACKING_NAME
