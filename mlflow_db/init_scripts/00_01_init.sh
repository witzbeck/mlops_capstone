#!/bin/bash
# Connect to the default database 'postgres' and execute the commands
psql -U $POSTGRES_USER -d postgres -c "DROP DATABASE IF EXISTS $POSTGRES_DB;"
psql -U $POSTGRES_USER -d postgres -c "CREATE DATABASE $POSTGRES_DB;"
psql -U $POSTGRES_USER -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;"

# Applying database migrations for MLflow
echo "Applying database migrations for MLflow"
mlflow db upgrade postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$MLFLOW_TRACKING_HOST:$MLFLOW_TRACKING_PORT/$MLFLOW_TRACKING_NAME
