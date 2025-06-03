
import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Análise de Contrato", layout="wide")
st.title("Agente de IA - Análise de Contrato")

st.markdown("""
Este app executa o agente de análise de contrato com base no script Python gerado do notebook.
Faça o upload do contrato em PDF abaixo antes de executar.
""")

# Upload do PDF
uploaded_file = st.file_uploader("Selecione o contrato em PDF", type="pdf")

if uploaded_file is not None:
    pdf_path = "contrato.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")

if st.button("Executar Análise"):
    if uploaded_file is None:
        st.warning("Por favor, envie um arquivo PDF antes de executar o script.")
    else:
        with st.spinner("Executando análise... isso pode levar alguns minutos."):
            try:
                result = subprocess.run(["python", "AnaliseContratoComTabelasAuto.py"], capture_output=True, text=True)
                if result.returncode == 0:
                    st.success("Análise concluída com sucesso!")
                    st.text(result.stdout)
                else:
                    st.error("Erro durante a execução do script:")
                    st.text(result.stderr)
            except Exception as e:
                st.error(f"Erro ao executar o script: {e}")
