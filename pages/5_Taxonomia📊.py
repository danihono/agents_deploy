import streamlit as st
import pandas as pd
import io
import agente_taxonomia_corrigido as agente_taxonomia  # Importar o módulo do agente corrigido

st.set_page_config(layout="wide", page_title="Classificador de Empresas para Construtoras")

st.title("Agente de IA para Classificação de Empresas")
st.subheader("Taxonomia para Área de Compras (Strategic Sourcing) com Busca de CNPJ")

st.markdown("""
Esta aplicação permite que você carregue uma planilha com informações de empresas (Razão Social e, opcionalmente, CNPJ)
para classificá-las automaticamente em uma taxonomia de 4 níveis: Família, Categoria, Subcategoria e Subsubcategoria.
Se o CNPJ não for fornecido, o sistema tentará buscá-lo automaticamente usando a API CNPJá (sujeito aos limites da chave configurada).
""")

# --- Upload do Arquivo ---
st.sidebar.header("1. Carregar Planilha de Empresas")
uploaded_file = st.sidebar.file_uploader(
    "Selecione um arquivo Excel (.xlsx, .xls) ou CSV (.csv)", 
    type=["xlsx", "xls", "csv"]
)

# Inicializar session state para df_classificado se não existir
if 'df_classificado' not in st.session_state:
    st.session_state.df_classificado = None
if 'df_original' not in st.session_state:
    st.session_state.df_original = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.df_original = pd.read_csv(uploaded_file)
        else:
            st.session_state.df_original = pd.read_excel(uploaded_file)
        
        st.sidebar.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")
        st.subheader("Dados Originais Carregados (Primeiras 5 linhas):")
        st.dataframe(st.session_state.df_original.head())

        st.info("Colunas carregadas. A normalização será feita automaticamente.")
        
        # Normalizando colunas usando a função do agente_taxonomia
        st.session_state.df_original = agente_taxonomia.normalizar_colunas(st.session_state.df_original)

        # Verificar e renomear CNPJ se necessário
        if "CNPJ" not in st.session_state.df_original.columns:
            st.session_state.df_original["CNPJ"] = ""  # Adiciona coluna CNPJ vazia se não existir

        st.info("Coluna 'Razão Social' encontrada. Coluna 'CNPJ' verificada/adicionada. Pronto para processar.")
        st.session_state.df_classificado = None  # Reseta classificado se novo arquivo é carregado

    except Exception as e:
        st.sidebar.error(f"Erro ao ler o arquivo: {e}")
        st.session_state.df_original = None
        st.session_state.df_classificado = None

# --- Processamento e Classificação ---
st.sidebar.header("2. Processar e Classificar")
if st.session_state.df_original is not None and "Razão Social" in st.session_state.df_original.columns and st.sidebar.button("Classificar Empresas"):
    with st.spinner("Processando, buscando CNPJs (se necessário) e classificando as empresas..."):
        try:
            # Chamar a função de processamento do agente_taxonomia
            st.session_state.df_classificado = agente_taxonomia.processar_empresas(
                st.session_state.df_original.copy(),
                agente_taxonomia.REGRAS_TAXONOMIA,
                agente_taxonomia.CNPJA_API_KEY
            )
            
            # Mostrar todas as linhas classificadas por padrão
            st.subheader("Dados Classificados (Tabela Completa):")
            st.dataframe(st.session_state.df_classificado)
            st.success(f"Empresas classificadas com sucesso! Total de {len(st.session_state.df_classificado)} registros processados.")
        except ValueError as ve:
            st.error(f"Erro durante a classificação: {ve}")
            st.session_state.df_classificado = None
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado durante a classificação: {e}")
            st.session_state.df_classificado = None

# --- Download do Arquivo Classificado ---
st.sidebar.header("3. Baixar Resultado")
if st.session_state.df_classificado is not None:
    output = io.BytesIO()
    
    # Usando openpyxl como engine em vez de xlsxwriter
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        st.session_state.df_classificado.to_excel(writer, index=False, sheet_name='Taxonomia_Empresas')
    
    excel_data = output.getvalue()
    
    st.sidebar.download_button(
        label="Baixar Planilha Classificada (.xlsx)",
        data=excel_data,
        file_name="empresas_classificadas_taxonomia.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.sidebar.success("Clique no botão acima para baixar a planilha com a taxonomia completa.")
else:
    st.sidebar.info("Aguardando o carregamento e classificação dos dados para habilitar o download.")
