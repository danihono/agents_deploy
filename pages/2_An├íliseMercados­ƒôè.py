import streamlit as st 
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from analisemercado import gerar_relatorio

st.set_page_config(page_title="Relatório de Mercado - Vorätte", layout="wide")
st.title("Executar Agente de IA da Vorätte (Com Setor Dinâmico)")
st.markdown("Este app executa o agente de IA adaptado para o setor que você escolher, baseado no notebook original.")

setor = st.text_input("Informe a Categoria que você deseja analisar:", placeholder="Ex: Tratores, Papelão, Computadores...")
empresa = st.text_input("Informe o setor que sua empresa atuar:",placeholder="Ex: Farmaceutica, Construção Civil, Industria etc")
regiao = st.text_input("Informe sua região de atuação:",placeholder="Ex: Brasil, Sudeste, São Paulo, Campinas etc")

if st.button("Executar Análise de Mercado"):
    if not setor.strip():
        st.error("Por favor, informe uma CATEGORIA para gerar o relatório.")
    else:
        # Valores padrão
        empresa_final = empresa.strip() if empresa.strip() else "Todos os setores"
        regiao_final = regiao.strip() if regiao.strip() else "Brasil"

        with st.spinner(f"Gerando relatório para {setor} ({empresa_final}) na região {regiao_final}..."):
            try:
                arquivo_word = gerar_relatorio(setor, empresa_final, regiao_final)
                st.success("Relatório gerado com sucesso!")

                with open(arquivo_word, "rb") as file:
                    st.download_button(
                        label="📥 Baixar Relatório Word",
                        data=file,
                        file_name=arquivo_word,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

            except Exception as e:
                st.error(f"Erro durante a geração: {e}")
