
import streamlit as st
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

st.set_page_config(page_title="Relatório de Mercado - Vorätte", layout="wide")
st.title("Executar Agente de IA da Vorätte (Notebook Original)")
st.markdown("Este app executa exatamente o notebook enviado, sem alterações de conteúdo ou lógica.")

if st.button("Executar Notebook"):
    with st.spinner("Executando notebook... isso pode levar alguns minutos."):
        try:
            notebook_path = "AnaliseMercado.ipynb"
            with open(notebook_path) as f:
                nb = nbformat.read(f, as_version=4)

            ep = ExecutePreprocessor(timeout=900, kernel_name="python3")
            ep.preprocess(nb, {'metadata': {'path': '.'}})

            with open("AnaliseMercado_executado.ipynb", "w", encoding="utf-8") as f:
                nbformat.write(nb, f)

            st.success("Notebook executado com sucesso!")
            with open("AnaliseMercado_executado.ipynb", "rb") as f:
                st.download_button("Baixar notebook executado", f, file_name="AnaliseMercado_executado.ipynb")
        except Exception as e:
            st.error(f"Erro durante a execução: {e}")
