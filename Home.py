import streamlit as st
import os

# Configuração do layout
st.set_page_config(layout="wide")

st.title("Home Dashboards")

# Listar arquivos na pasta 'pages'
pages_dir = 'pages'
pages = [f for f in os.listdir(pages_dir) if f.endswith('.py')]

# Exibir os nomes das páginas
st.write("Dashboards disponíveis:")
for page in pages:
    st.write(" - ", page[:-3])  # Remove a extensão '.py' ao exibir
