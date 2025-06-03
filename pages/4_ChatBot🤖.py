# Streamlit app
import streamlit as st
from chat import generate_response
st.title("Chatbot com Groq e LangChain")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

user_input = st.text_input("Digite sua mensagem:")

if st.button("Enviar"):
    response = generate_response(user_input)
    st.session_state.conversation.append((user_input, response))
    st.experimental_rerun()

conversation = st.session_state.conversation

for user_input, response in conversation:
    st.write(f"Você: {user_input}")
    st.write(f"Chatbot: {response}")