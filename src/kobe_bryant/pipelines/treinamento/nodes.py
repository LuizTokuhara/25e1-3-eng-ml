"""
This is a boilerplate pipeline 'treinamento'
generated using Kedro 0.19.12
"""
from pycaret.classification import ClassificationExperiment
from sklearn.metrics import log_loss, accuracy_score, recall_score, precision_score, f1_score
from mlflow.models.signature import infer_signature
import mlflow
import json

mlflow.set_tracking_uri('http://127.0.0.1:5500')

def train_reg_log(base_train, base_test):
  exp = ClassificationExperiment()

  exp.setup(
      data=base_train,
      test_data=base_test,
      target='shot_made_flag',
      session_id=42,
      normalize=True,
      normalize_method='robust',
      log_experiment=True,
      experiment_name='kobe'
  )

  # Treinar o modelo de regressão logística
  log_reg_model = exp.create_model('lr')

  # Avaliar o modelo no conjunto de teste
  predictions = exp.predict_model(log_reg_model, data=base_test)

  # Definir um exemplo de entrada para a assinatura do modelo
  input_example = base_test.drop(columns=['shot_made_flag']).head(1)
  signature = infer_signature(input_example, predictions[['prediction_label']])

  # # Calcular métricas manualmente
  y_true = base_test['shot_made_flag']
  y_pred = predictions['prediction_label']
  y_pred_proba = predictions['prediction_score']  # Probabilidades para log_loss

  metrics = {
      'accuracy': accuracy_score(y_true, y_pred),
      'precision': precision_score(y_true, y_pred),
      'recall': recall_score(y_true, y_pred),
      'f1': f1_score(y_true, y_pred),
      'log_loss': log_loss(y_true, y_pred_proba)
  }

  exp.evaluate_model(log_reg_model)

  # exp.save_model(log_reg_model, model_name="log_reg_model")

  # Logar métricas calculadas
  mlflow.sklearn.log_model(
      sk_model=log_reg_model,
      artifact_path='log_reg_model',
      signature=signature,
      input_example=input_example,
      registered_model_name='log_reg_model',
  )
  mlflow.log_metrics(metrics)
  
  return log_reg_model, metrics


def train_dec_tree(base_train, base_test):
  exp = ClassificationExperiment()

  exp.setup(
      data=base_train,
      test_data=base_test,
      target='shot_made_flag',
      session_id=42,
      normalize=True,
      normalize_method='robust',
      log_experiment=True,
      experiment_name='kobe'
  )

  # Treinar o modelo de arvore de decisao
  dt_model = exp.create_model('dt')

  # Avaliar o modelo no conjunto de teste
  predictions = exp.predict_model(dt_model, data=base_test)

  # Definir um exemplo de entrada para a assinatura do modelo
  input_example = base_test.drop(columns=['shot_made_flag']).head()
  signature = infer_signature(input_example, predictions[['prediction_label']])

  # Calcular métricas manualmente
  y_true = base_test['shot_made_flag']
  y_pred = predictions['prediction_label']
  y_pred_proba = predictions['prediction_score']  # Probabilidades para log_loss

  metrics = {
      'accuracy': accuracy_score(y_true, y_pred),
      'precision': precision_score(y_true, y_pred),
      'recall': recall_score(y_true, y_pred),
      'f1': f1_score(y_true, y_pred),
      'log_loss': log_loss(y_true, y_pred_proba)
  }

  # exp.save_model(dt_model, model_name="dt_model")

  # Logar métricas calculadas
  mlflow.sklearn.log_model(
      sk_model=dt_model,
      artifact_path='dt_model',
      signature=signature,
      input_example=input_example,
      registered_model_name='dt_model'
  )
  mlflow.log_metrics(metrics)

  return dt_model, json.dumps(metrics)