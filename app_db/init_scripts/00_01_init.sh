#!/bin/bash
# Connect to the default database 'postgres' and execute the commands
psql -U postgres -d postgres -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"
psql -U postgres -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $MLFLOW_TRACKING_NAME TO $MLFLOW_TRACKING_USER;"

# Applying database migrations for MLflow
mlflow db upgrade postgresql://$MLFLOW_TRACKING_USER:$MLFLOW_TRACKING_PASSWORD@$MLFLOW_TRACKING_HOST:$MLFLOW_TRACKING_PORT/$MLFLOW_TRACKING_NAME
