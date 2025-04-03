import streamlit as st
import requests
import numpy as np
from sklearn.preprocessing import RobustScaler

# Criar e carregar o RobustScaler
scaler = RobustScaler()

def call_inference(data):
    """Faz a requisição ao endpoint de inferência do modelo após aplicar o RobustScaler"""
    
    column_names = ['lat', 'lon', 'minutes_remaining', 'period', 'playoffs', 'shot_distance']
    
    # Converter lat/lon de string para float
    try:
        data['lat'] = float(data['lat']) if data['lat'] else 0.0
        data['lon'] = float(data['lon']) if data['lon'] else 0.0
    except ValueError:
        st.error("Erro: Latitude e Longitude precisam ser valores numéricos.")
        return None
    
    st.json(data)

    # Criar array com os dados inseridos pelo usuário
    input_array = np.array([[data[col] for col in column_names]])

    # Aplicar RobustScaler
    scaled_input = scaler.fit_transform(input_array)  # ⚠️ Se já tem um scaler salvo, use scaler.transform()
    
    # Criar estrutura para enviar à API
    rows = scaled_input.tolist()

    try:
        resp = requests.post(
            'http://localhost:5600/invocations',
            json={
                'dataframe_split': {
                    'columns': column_names,
                    'data': rows
                }
            }
        )
        response_json = resp.json()
        st.json(response_json)  # Mostra o JSON de resposta no Streamlit
        return response_json['predictions'][0]

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao chamar a API: {e}")
        return None

st.markdown("""
# Engenharia de Machine Learning  
### Predição de cestas do jogador Kobe Bryant 🏀
""")

# Criando os inputs do usuário
lat = st.text_input('Latitude')  # Agora recebe como texto
lon = st.text_input('Longitude')  # Agora recebe como texto
minutes_remaining = st.number_input('Minutes Remaining')
period = st.number_input('Period')
playoffs = st.number_input('Playoffs')
shot_distance = st.number_input('Shot Distance')

# Criando o dicionário de entrada
input_data = {
    'lat': lat,
    'lon': lon,
    'minutes_remaining': minutes_remaining,
    'period': period,
    'playoffs': playoffs,
    'shot_distance': shot_distance
}

# Chamando a inferência
shot_made_flag = call_inference(input_data)

# Exibir resultado da predição
if shot_made_flag is not None:
    st.write(f"**Fez a cesta?** {'✅ Sim' if shot_made_flag else '❌ Não'}")