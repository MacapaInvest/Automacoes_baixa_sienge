import streamlit as st
import pandas as pd
import numpy as np
from login import fazerLogin
from baixas import efetuar_baixas
from data import definir_data_baixa
from consulta_conta import consultar_contas_correntes
import io
from lista_spe import spe_subdominio

def obter_subdominio(cod_spe):
    return spe_subdominio.get(int(cod_spe), 'Subdomínio não encontrado')

def ler_base(uploaded_file):
    baixas = pd.read_excel(uploaded_file)
    baixas = baixas[['Cód SPE', 'Título', 'Parcela']]
    baixas['subdominio'] = baixas['Cód SPE'].apply(lambda x: obter_subdominio(str(x)))
    baixas['company_id'] = baixas['Cód SPE'].astype(int)
    return baixas

def gerar_download(df, nome_arquivo):
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    st.download_button(label=f"Baixar {nome_arquivo}", data=output, file_name=nome_arquivo, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def app():
    st.set_page_config(page_title="Efetuar Baixas", page_icon=":guardsman:", layout="wide", initial_sidebar_state="expanded")

    st.markdown("""
        <style>
        .main { background-color: #E1E1E2; }
        h1 { color: #1B2D4E; text-align: left; }
        h3 { color: #3BABD4; text-align: left; }
        .stButton>button { background-color: #1B2D4E; color: white; }
        .stButton>button:hover { background-color: #3BABD4; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>Carregar Base de Dados e Efetuar Baixas</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Escolha o arquivo Excel", type="xlsx")

    if uploaded_file is not None:
        baixas = ler_base(uploaded_file)

        st.subheader('Base Completa')
        st.write(baixas)

        data_baixa = definir_data_baixa()
        st.write('Data de Baixa Definida:', data_baixa)

        for index, row in baixas.iterrows():
            subdominio = row['subdominio']
            cod_spe = int(row['Cód SPE'])
            contas_bancarias = consultar_contas_correntes(subdominio, cod_spe)

            if contas_bancarias:
                contas_bancarias.insert(0, np.nan)
                conta_selecionada = st.selectbox(
                    f"Selecione uma conta para Título {row['Título']} - Parcela {row['Parcela']}",
                    contas_bancarias, key=f"conta_{subdominio}_{index}")
                baixas.at[index, 'CASO_DIF_CONTA'] = conta_selecionada

        if st.button('Rodar Baixas', key="rodar_baixas"):
            with st.spinner('Processando as baixas...'):
                resumo = {"sucesso": 0, "falha": 0}
                for subdominio in baixas['subdominio'].unique():
                    navegador = fazerLogin(subdominio)
                    if navegador is None:
                        st.warning(f"Falha no login para {subdominio}")
                        continue

                    for index, row in baixas[baixas['subdominio'] == subdominio].iterrows():
                        status = efetuar_baixas(
                            navegador, data_baixa, row['Cód SPE'], row['Título'], row['Parcela'],
                            row.get('CASO_DIF_CONTA', np.nan), f"https://{subdominio}.sienge.com.br/sienge/CPG/filterBaixa.do"
                        )
                        baixas.at[index, 'status'] = status
                        resumo["sucesso" if status == "Baixa realizada" else "falha"] += 1

                        # 🖨️ Imprime Título, Parcela e Status
                        st.write(f"🎯 Título: {row['Título']} | Parcela: {row['Parcela']} | Status: {status}")

                st.success(f"Execução Finalizada: {resumo['sucesso']} baixas com sucesso, {resumo['falha']} falhas.")

                gerar_download(baixas, 'Baixas_com_status.xlsx')

if __name__ == "__main__":
    app()
