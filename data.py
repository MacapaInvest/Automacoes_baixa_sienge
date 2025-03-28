import threading
from datetime import datetime, timedelta
import streamlit as st

def obter_ultimo_dia_util():
    """Calcula o último dia útil (desconsiderando sábados e domingos)."""
    hoje = datetime.today() - timedelta(days=1)  # Um dia anterior
    if hoje.weekday() == 5:  # Se for sábado, volta para sexta
        hoje -= timedelta(days=1)
    elif hoje.weekday() == 6:  # Se for domingo, volta para sexta
        hoje -= timedelta(days=2)
    return hoje.strftime('%d/%m/%Y')

def solicitar_data_baixa():
    """Solicita que o usuário insira a data manualmente ou aguarde 5 segundos."""
    global data_baixa
    data_baixa = st.text_input("Digite a data de baixa (DD/MM/AAAA):", "")

def definir_data_baixa():
    """Define a data de baixa com um timeout de 5 segundos."""
    global data_baixa
    data_baixa = None

    # Chama a função para solicitar a data com Streamlit
    solicitar_data_baixa()

    # Espera até 5 segundos pela entrada do usuário
    if not data_baixa:
        data_baixa = obter_ultimo_dia_util()
        st.write(f"Nenhuma data inserida. Usando o dia anterior: {data_baixa}")

    return data_baixa
