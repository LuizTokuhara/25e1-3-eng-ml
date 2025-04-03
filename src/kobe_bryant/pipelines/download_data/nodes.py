"""
This is a boilerplate pipeline 'download_data'
generated using Kedro 0.19.11
"""
import requests
import pandas as pd
import io

def download_data_dev():
  resp = requests.get("https://github.com/tciodaro/eng_ml/raw/refs/heads/main/data/dataset_kobe_dev.parquet")
  if resp.status_code == 200:
    buffer = io.BytesIO(resp.content)
    df = pd.read_parquet(buffer, engine='pyarrow')
    return df
  else:
      print(f"Erro ao baixar o arquivo: {resp.status_code}")

def download_data_prod():
  resp = requests.get("https://github.com/tciodaro/eng_ml/raw/refs/heads/main/data/dataset_kobe_prod.parquet")
  if resp.status_code == 200:
    buffer = io.BytesIO(resp.content)
    df = pd.read_parquet(buffer, engine='pyarrow')
    return df
  else:
      print(f"Erro ao baixar o arquivo: {resp.status_code}")