import streamlit as st
import requests

API_URL = "http://localhost:8000/summarize"

st.title("Desafio Dynadok 🚀")

input_type = st.radio(
    "Escolha como deseja fornecer o texto",
    options=["Inserir manualmente", "Carregar arquivo de texto"],
)

text_input = ""

if input_type == "Inserir manualmente":
    text_input = st.text_area("Digite o texto para resumir", placeholder="Digite aqui seu texto...")
elif input_type == "Carregar arquivo de texto":
    uploaded_file = st.file_uploader("Faça o upload de um arquivo de texto (.txt)", type=["txt"])
    if uploaded_file is not None:
        try:
            text_input = uploaded_file.read().decode("utf-8")
            st.success("Arquivo carregado com sucesso!")
            st.write("### Conteúdo do arquivo:")
            st.write(text_input)
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {str(e)}")

language = st.selectbox(
    "Selecione o idioma do resumo",
    options=["Português", "Inglês", "Espanhol"],
    format_func=lambda x: {"Português": "pt", "Inglês": "en", "Espanhol": "es"}[x],
)

lang_code = {"Português": "pt", "Inglês": "en", "Espanhol": "es"}[language]

if st.button("Gerar Resumo"):
    if not text_input.strip():
        st.error("O campo de texto ou arquivo não pode estar vazio!")
    else:
        try:
            with st.spinner("Gerando resumo..."):
                response = requests.post(API_URL, json={"text": text_input, "lang": lang_code})
                response_data = response.json()
                
                if response.status_code == 200:
                    summary = response_data.get("summary", "Nenhum resumo retornado.")
                    st.success("Resumo gerado com sucesso!")
                    st.write("### Resumo")
                    st.write(summary)
                else:
                    st.error(f"Erro na API: {response_data.get('detail', 'Erro desconhecido')}")
        except Exception as e:
            st.error(f"Ocorreu um erro ao conectar com a API: {str(e)}")
