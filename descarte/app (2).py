
import streamlit as st
from AnaliseContrato import *

st.set_page_config(page_title="Análise de Contrato", layout="wide")
st.title("Agente de IA - Análise de Contrato")

st.markdown("""
Este app executa o agente de análise de contrato com base no notebook original.
Certifique-se de preencher os campos necessários abaixo para rodar o agente.
""")

# Cria um botão para executar o código do notebook
if st.button("Executar Agente"):
    st.markdown("### Saída do Agente")
    try:
        # Executa o código principal do notebook convertido
        main()  # Assumindo que existe uma função main(), caso contrário edita aqui
    except Exception as e:
        st.error(f"Erro ao executar o agente: {e}")
