"""
This is a boilerplate pipeline 'preparacao_dados'
generated using Kedro 0.19.11
"""
from sklearn.model_selection import train_test_split
import mlflow

mlflow.set_tracking_uri('http://127.0.0.1:5500')
mlflow.set_experiment('kobe')

def preparacao_dados_dev(df):
  df = df.dropna()
  features = df[['lat', 'lon', 'minutes_remaining', 'period', 'playoffs', 'shot_distance', 'shot_made_flag']]
  # features.loc[:, 'playoffs'] = features['playoffs'].map({0: False, 1: True})
  # features.loc[:, 'shot_made_flag'] = features['shot_made_flag'].map({0: False, 1: True})
  return features

def treino_teste(df):
  with mlflow.start_run(run_name='train_test'):
        train, test = train_test_split(
            df, test_size=0.2, stratify=df['shot_made_flag'], random_state=42
        )

        # Log parâmetros
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)

        # Log métricas (quantidade de amostras)
        mlflow.log_metric("train_size", len(train))
        mlflow.log_metric("test_size", len(test))

        # Log distribuição da variável alvo
        mlflow.log_metric("train_shot_made_1", train["shot_made_flag"].sum())
        mlflow.log_metric("test_shot_made_1", test["shot_made_flag"].sum())

        return train, test