import streamlit as st
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

st.set_page_config(page_title="Análise de Contrato", layout="wide")
st.title("Agente de IA - Análise de Contrato")

st.markdown("""
Este app executa o agente de análise de contrato com base no notebook original.
Certifique-se de preencher os campos necessários abaixo para rodar o agente.
""")

if st.button("Executar Notebook"):
    with st.spinner("Executando notebook... isso pode levar alguns minutos."):
        try:
            notebook_path = "AnaliseContrato.ipynb"
            
            with open(notebook_path, encoding="utf-8") as f:
                nb = nbformat.read(f, as_version=4)

            ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
            ep.preprocess(nb, {'metadata': {'path': '.'}})
            
            with open("AnaliseContrato_executado.ipynb", "w", encoding="utf-8") as f:
                nbformat.write(nb, f)

            st.success("Notebook executado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao executar o notebook: {e}")