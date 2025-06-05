import pandas as pd
import re
import requests
import json
import unicodedata

def normalizar_colunas(df):
    """
    Identifica e padroniza as colunas 'Razão Social' e 'CNPJ' mesmo que estejam com nomes alternativos.
    """
    colunas_normalizadas = {col.strip().lower().replace("ã", "a").replace("ç", "c"): col for col in df.columns}
    
    possiveis_razao_social = [
        "razao social", "razaosocial", "nome da empresa", "empresa", "nome", "razao_social"
    ]
    
    # Detectar e renomear a coluna de Razão Social
    for chave in colunas_normalizadas:
        for alias in possiveis_razao_social:
            if alias.replace(" ", "") in chave.replace(" ", "").replace("_", ""):
                df = df.rename(columns={colunas_normalizadas[chave]: "Razão Social"})
                break
        if "Razão Social" in df.columns:
            break

    # Detectar e renomear a coluna de CNPJ
    for chave in colunas_normalizadas:
        if "cnpj" in chave:
            df = df.rename(columns={colunas_normalizadas[chave]: "CNPJ"})
            break

    # Se ainda não tiver CNPJ, cria uma vazia
    if "CNPJ" not in df.columns:
        df["CNPJ"] = ""

    return df

# Chave da API CNPJá fornecida pelo usuário
CNPJA_API_KEY = "8c2289d8-d276-4cb4-b714-30af1390c221-d475e0a7-a0da-4344-becd-ec44fdb7cf95"
CNPJA_BASE_URL = "https://api.cnpja.com/office"

def remover_acentos(texto):
    """
    Remove acentos de um texto, mantendo apenas caracteres ASCII.
    """
    if not isinstance(texto, str):
        return ""
    # Normaliza para forma de decomposição e remove os caracteres não ASCII
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def limpar_texto(texto):
    """
    Limpa o texto removendo acentos, caracteres especiais e padronizando espaços.
    """
    if not isinstance(texto, str):
        return ""
    # Primeiro remove acentos
    texto = remover_acentos(texto)
    # Converte para maiúsculas
    texto = texto.upper()
    # Remove caracteres não alfanuméricos, exceto espaços
    texto = re.sub(r'[^A-Z0-9\s]', '', texto)
    # Remove espaços extras e faz trim
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def buscar_cnpj_por_razao_social(razao_social_original, api_key):
    """
    Busca o CNPJ de uma empresa pela Razão Social usando a API CNPJá.
    Retorna o CNPJ encontrado ou uma string vazia se não encontrar ou ocorrer erro.
    """
    if not razao_social_original or not isinstance(razao_social_original, str):
        return ""
    
    headers = {
        "Authorization": api_key
    }
    params = {
        "names.in": razao_social_original, 
        "limit": 5 
    }

    try:
        response = requests.get(CNPJA_BASE_URL, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get("records", [])
            if records:
                cnpj_ativo = ""
                for record in records:
                    if record.get("status", {}).get("text", "").upper() == "ATIVA":
                        cnpj_ativo = record.get("taxId", "")
                        if cnpj_ativo: 
                            return cnpj_ativo
                
                if not cnpj_ativo and records[0].get("taxId"):
                    return records[0].get("taxId")
            return "" 
        elif response.status_code == 401:
            print(f"Erro de autenticação (401) ao buscar CNPJ para '{razao_social_original}'. Verifique a chave da API.")
            return "CNPJ_API_AUTH_ERROR"
        elif response.status_code == 429:
            print(f"Limite de taxa excedido (429) ao buscar CNPJ para '{razao_social_original}'.")
            return "CNPJ_API_RATE_LIMIT"
        else:
            print(f"Erro na API CNPJá ({response.status_code}) ao buscar CNPJ para '{razao_social_original}': {response.text}")
            return "CNPJ_API_ERROR"
            
    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição ao buscar CNPJ para '{razao_social_original}': {e}")
        return "CNPJ_REQUEST_ERROR"
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON da API CNPJá para '{razao_social_original}'. Resposta: {response.text}")
        return "CNPJ_JSON_ERROR"
    return ""

def classificar_empresa(razao_social, regras_taxonomia):
    """
    Classifica uma empresa com base em sua razão social e nas regras de taxonomia.
    """
    razao_social_limpa = limpar_texto(razao_social)
    
    # Debug para verificar a razão social limpa
    print(f"DEBUG - Razão Social Limpa: '{razao_social_limpa}'")
    
    for familia, data_familia in regras_taxonomia.items():
        # Normaliza as keywords da família
        keywords_familia = [limpar_texto(kw) for kw in data_familia.get("keywords", [])]
        
        # Debug para verificar as keywords da família
        print(f"DEBUG - Família: {familia}, Keywords: {keywords_familia}")
        
        if any(keyword in razao_social_limpa for keyword in keywords_familia):
            print(f"DEBUG - Match na Família: {familia}")
            
            for categoria, data_categoria in data_familia.get("CATEGORIAS", {}).items():
                # Normaliza as keywords da categoria
                keywords_categoria = [limpar_texto(kw) for kw in data_categoria.get("keywords", [])]
                
                # Debug para verificar as keywords da categoria
                print(f"DEBUG - Categoria: {categoria}, Keywords: {keywords_categoria}")
                
                if any(keyword in razao_social_limpa for keyword in keywords_categoria):
                    print(f"DEBUG - Match na Categoria: {categoria}")
                    
                    for subcategoria, data_subcategoria in data_categoria.get("SUBCATEGORIAS", {}).items():
                        # Normaliza as keywords da subcategoria
                        keywords_subcategoria = [limpar_texto(kw) for kw in data_subcategoria.get("keywords", [])]
                        
                        # Debug para verificar as keywords da subcategoria
                        print(f"DEBUG - Subcategoria: {subcategoria}, Keywords: {keywords_subcategoria}")
                        
                        if any(keyword in razao_social_limpa for keyword in keywords_subcategoria):
                            print(f"DEBUG - Match na Subcategoria: {subcategoria}")
                            
                            for subsubcategoria, data_subsubcategoria in data_subcategoria.get("SUBSUBCATEGORIAS", {}).items():
                                # Normaliza as keywords da subsubcategoria
                                keywords_subsubcategoria = [limpar_texto(kw) for kw in data_subsubcategoria.get("keywords", [])]
                                
                                # Debug para verificar as keywords da subsubcategoria
                                print(f"DEBUG - Subsubcategoria: {subsubcategoria}, Keywords: {keywords_subsubcategoria}")
                                
                                if any(keyword in razao_social_limpa for keyword in keywords_subsubcategoria):
                                    print(f"DEBUG - Match na Subsubcategoria: {subsubcategoria}")
                                    return familia, categoria, subcategoria, subsubcategoria
                            return familia, categoria, subcategoria, "Não Classificado"
                    return familia, categoria, "Não Classificado", "Não Classificado"
            return familia, "Não Classificado", "Não Classificado", "Não Classificado"
    return "Não Classificado", "Não Classificado", "Não Classificado", "Não Classificado"

def processar_empresas(df_empresas, regras_taxonomia, api_key_cnpja):
    """
    Processa um DataFrame de empresas, buscando CNPJs quando necessário e classificando-as.
    """
    if not isinstance(df_empresas, pd.DataFrame):
        raise ValueError("Entrada deve ser um DataFrame pandas.")

    if "Razão Social" not in df_empresas.columns:
        raise ValueError("DataFrame deve conter a coluna 'Razão Social'.")

    if "CNPJ" not in df_empresas.columns:
        df_empresas["CNPJ"] = ""
    else:
        # Garantir que a coluna CNPJ seja string para evitar problemas com tipos mistos
        df_empresas["CNPJ"] = df_empresas["CNPJ"].astype(str)

    resultados = []
    for index, row in df_empresas.iterrows():
        razao_social = row["Razão Social"]
        cnpj = str(row.get("CNPJ", "")).strip()
        # Normalizar CNPJs vazios ou com valores como 'nan' para string vazia
        if cnpj.lower() == 'nan' or cnpj.lower() == 'none' or not cnpj:
            cnpj = ""

        if not cnpj and razao_social:
            print(f"CNPJ não fornecido para '{razao_social}'. Buscando via API...")
            cnpj_encontrado = buscar_cnpj_por_razao_social(razao_social, api_key_cnpja)
            if cnpj_encontrado and not any(err_code in cnpj_encontrado for err_code in ["CNPJ_API_AUTH_ERROR", "CNPJ_API_RATE_LIMIT", "CNPJ_API_ERROR", "CNPJ_REQUEST_ERROR", "CNPJ_JSON_ERROR"]):
                cnpj = cnpj_encontrado
                print(f"CNPJ encontrado para '{razao_social}': {cnpj}")
            else:
                print(f"Não foi possível obter o CNPJ para '{razao_social}'. Detalhe: {cnpj_encontrado}")
                if any(err_code in cnpj_encontrado for err_code in ["CNPJ_API_AUTH_ERROR", "CNPJ_API_RATE_LIMIT", "CNPJ_API_ERROR", "CNPJ_REQUEST_ERROR", "CNPJ_JSON_ERROR"]):
                    cnpj = cnpj_encontrado 
                else:
                    cnpj = "" 
        
        familia, categoria, subcategoria, subsubcategoria = classificar_empresa(razao_social, regras_taxonomia)
        
        resultados.append({
            "CNPJ": cnpj,
            "Razão Social": razao_social,
            "Família": familia,
            "Categoria": categoria,
            "Subcategoria": subcategoria,
            "Subsubcategoria": subsubcategoria
        })
    
    df_resultado = pd.DataFrame(resultados)
    return df_resultado

# Regras de taxonomia com keywords normalizadas (sem acentos)
REGRAS_TAXONOMIA = {
    "SERVIÇOS": {
        "keywords": ["SERVICO", "SERVICOS", "ASSESSORIA", "CONSULTORIA", "MANUTENCAO", "INSTALACAO", "TRANSPORTE", "LOGISTICA", "LIMPEZA", "CONSERVACAO"],
        "CATEGORIAS": {
            "SERVIÇOS DE ENGENHARIA E ARQUITETURA": {
                "keywords": ["ENGENHARIA", "ARQUITETURA", "PROJETO", "PROJETOS", "PLANEJAMENTO URBANO"],
                "SUBCATEGORIAS": {
                    "PROJETOS DE ARQUITETURA": {
                        "keywords": ["ARQUITETONICO", "ARQUITETURA"],
                        "SUBSUBCATEGORIAS": {}
                    },
                    "PROJETOS DE ENGENHARIA": {
                        "keywords": ["ESTRUTURAL", "ENGENHARIA CIVIL"],
                        "SUBSUBCATEGORIAS": {}
                    },
                    "CONSULTORIA EM ENGENHARIA": {
                        "keywords": ["CONSULTORIA EM GESTAO DE PROJETOS DE ENGENHARIA CIVIL"],
                        "SUBSUBCATEGORIAS": {}
                    }
                }
            },
            "SERVIÇOS DE CONSULTORIA": {
                "keywords": ["CONSULTORIA", "ASSESSORIA"],
                "SUBCATEGORIAS": {
                    "CONSULTORIA EM GESTÃO": {
                        "keywords": ["GESTAO", "EMPRESARIAL"],
                        "SUBSUBCATEGORIAS": {}
                    },
                    "CONSULTORIA EM TI": {
                        "keywords": ["TI", "TECNOLOGIA DA INFORMACAO", "SOLUCOES EM TI"],
                        "SUBSUBCATEGORIAS": {}
                    }
                }
            },
            "SERVIÇOS DE INSTALAÇÃO E MANUTENÇÃO": {
                "keywords": ["INSTALACAO", "MANUTENCAO"],
                "SUBCATEGORIAS": {
                    "INSTALAÇÕES ELÉTRICAS E HIDRÁULICAS": {
                        "keywords": ["ELETRICA", "HIDRAULICA"],
                        "SUBSUBCATEGORIAS": {}
                    },
                    "MANUTENÇÃO PREDIAL": {
                        "keywords": ["PREDIAL"],
                        "SUBSUBCATEGORIAS": {}
                    }
                }
            },
            "SERVIÇOS GERAIS": {
                "keywords": ["ALVENARIA", "PINTURAS", "EDIFICACAO", "OBRAS", "LIMPEZA", "CONSERVACAO"],
                 "SUBCATEGORIAS": {
                    "LIMPEZA E CONSERVAÇÃO": {
                        "keywords": ["LIMPEZA", "CONSERVACAO PREDIAL PROFISSIONAL"],
                        "SUBSUBCATEGORIAS": {}
                    }
                }
            },
            "SERVIÇOS DE TRANSPORTE E LOGÍSTICA": {
                "keywords": ["TRANSPORTE", "LOGISTICA"],
                "SUBCATEGORIAS": {
                    "TRANSPORTE DE CARGAS": {
                        "keywords": ["CARGAS"],
                        "SUBSUBCATEGORIAS": {}
                    }
                }
            }
        }
    },
    "MATERIAIS DIRETOS": {
        "keywords": ["MATERIAL", "MATERIAIS", "FORNECIMENTO", "INSUMO", "MADEIREIRA", "COMERCIO"],
        "CATEGORIAS": {
            "MATERIAL BÁSICO": {
                "keywords": ["BASICO", "AREIA", "BRITA", "CIMENTO", "CAL", "TIJOLO", "MADEIREIRA"],
                "SUBCATEGORIAS": {
                    "AGREGADOS": {
                        "keywords": ["AREIA", "BRITA", "PEDRA GRANDE"],
                        "SUBSUBCATEGORIAS": {}
                    },
                    "MADEIRA": {
                        "keywords": ["MADEIREIRA", "BOA VISTA"],
                        "SUBSUBCATEGORIAS": {}
                    }
                }
            },
            "MATERIAL DE ACABAMENTO": {
                "keywords": ["ACABAMENTO", "ACABAMENTOS", "REVESTIMENTO", "PISO", "AZULEJO", "TINTA", "LOUCA", "METAL SANITARIO", "PINTURAS"],
                "SUBCATEGORIAS": {
                    "PINTURAS E REVESTIMENTOS": {
                        "keywords": ["PINTURAS", "ACABAMENTOS FINOS"],
                        "SUBSUBCATEGORIAS": {}
                    }
                }
            }
        }
    },
    "EQUIPAMENTOS": {
        "keywords": ["EQUIPAMENTO", "EQUIPAMENTOS", "MAQUINA", "FERRAMENTA", "FERRAMENTAS"],
        "CATEGORIAS": {
            "LOCAÇÃO DE EQUIPAMENTOS": {
                "keywords": ["LOCACAO", "ALUGUEL", "LOCADORA"],
                "SUBCATEGORIAS": {
                    "LOCAÇÃO DE ANDAIMES E PEQUENOS EQUIPAMENTOS": {
                        "keywords": ["ANDAIMES", "EQUIPAMENTOS PARA CONSTRUCAO"],
                        "SUBSUBCATEGORIAS": {}
                    }
                }
            },
            "COMPRA DE FERRAMENTAS E MÁQUINAS": {
                "keywords": ["COMERCIO DE FERRAMENTAS", "MAQUINAS INDUSTRIAIS"],
                "SUBCATEGORIAS": {
                    "FERRAMENTAS MANUAIS E ELÉTRICAS": {
                        "keywords": ["FERRAMENTAS"],
                        "SUBSUBCATEGORIAS": {}
                    }
                }
            }
        }
    },
    "ALIMENTAÇÃO": {
        "keywords": ["PADARIA", "ALIMENTOS", "RESTAURANTE", "LANCHONETE"],
        "CATEGORIAS": {
            "PADARIAS E CONFEITARIAS": {
                "keywords": ["PADARIA", "CONFEITARIA", "DELICIA DO BAIRRO", "PAO QUENTE"],
                "SUBCATEGORIAS": {
                    "PRODUTOS DE PADARIA": {
                        "keywords": ["PAO", "BOLO"],
                        "SUBSUBCATEGORIAS": {}
                    }
                }
            }
        }
    }
}

if __name__ == "__main__":
    print("Iniciando teste do agente de taxonomia com busca de CNPJ e arquivo completo...")
    
    input_csv_file = "/home/ubuntu/empresas_teste_completo.csv"
    output_excel_file = "/home/ubuntu/empresas_classificadas_completo.xlsx"

    try:
        df_empresas_teste_completo = pd.read_csv(input_csv_file)
        print(f"\nDataFrame de Entrada (de {input_csv_file}):")
        print(df_empresas_teste_completo.head())

        df_classificado_completo = processar_empresas(df_empresas_teste_completo, REGRAS_TAXONOMIA, CNPJA_API_KEY)

        print("\nDataFrame Classificado com CNPJs Buscados (quando aplicável) - Completo:")
        print(df_classificado_completo)

        df_classificado_completo.to_excel(output_excel_file, index=False)
        print(f"\nResultado salvo em {output_excel_file}")

    except FileNotFoundError:
        print(f"Erro: Arquivo de teste '{input_csv_file}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento: {e}")
        print("Se for erro ao salvar Excel, certifique-se de que a biblioteca 'openpyxl' está instalada: pip install openpyxl")
