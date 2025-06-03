import streamlit as st
import os
from langchain import LLMChain, PromptTemplate
from groq import Groq

# Configuração do Groq
groq_api_key = "Sgsk_GPuSNm0yRQv1dzjlJcYfWGdyb3FYZtCTsV3abupar33JbTmeZrKO"
groq_model_id = "org_01jpjrqzxrfda849mgxnxn41j5"

# Configuração do LangChain
llm_chain = LLMChain(
    llm=Groq(groq_api_key, groq_model_id),
    
    prompt_template=PromptTemplate(
        input_variables=["user_input"],
        template="Respond como um assistente: {user_input}",
    ),
)

# Função para gerar resposta
def generate_response(user_input):
    output = llm_chain({"user_input": user_input})
    return output

