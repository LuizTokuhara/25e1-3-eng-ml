"""
This is a boilerplate pipeline 'pipeline_aplicacao'
generated using Kedro 0.19.12
"""
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, log_loss
from sklearn.preprocessing import RobustScaler
import numpy as np
import pandas as pd
import mlflow

mlflow.set_tracking_uri('http://127.0.0.1:5500')
mlflow.set_experiment('kobe')
artifact_path = "data/processed/kobe_predictions.parquet"
model = mlflow.sklearn.load_model("models:/log_reg_model/2")

def application_pipeline(df):
  with mlflow.start_run(run_name="pipeline_aplicacao"):
    features = df[['lat', 'lon', 'minutes_remaining', 'period', 'playoffs', 'shot_distance', 'shot_made_flag']]
    features_clean = features.dropna(subset=['shot_made_flag'])
    req_rows = features_clean.drop(columns=['shot_made_flag'])

    # Aplicar RobustScaler
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(req_rows)

    y_pred = model.predict(X_scaled)
    y_pred_proba = model.predict_proba(X_scaled)[:, 1]

    y_true = features_clean["shot_made_flag"]

    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred),
        'log_loss': log_loss(y_true, y_pred_proba)
    }

    mlflow.log_metrics(metrics)

    # Criar DataFrame de resultados
    df_result = pd.DataFrame({
        'predictions': y_pred.tolist(),
        'real_values': y_true.tolist()
    })

    # Logar como artefato no MLflow
    mlflow.log_artifact(artifact_path)

    return df_result