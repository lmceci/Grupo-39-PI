import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Dashboard SAMU 192", layout="wide")

st.title("🚑 Painel de Indicadores SAMU 192")
st.markdown("---")

# Mensagem de introdução para o professor
st.sidebar.header("Menu de Navegação")
st.sidebar.info("Projeto Integrador - ADS Senac")

# Simulando o que teremos na Etapa 3
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cobertura por Região")
    st.info("Aqui será exibido um gráfico de barras comparando as regiões.")

with col2:
    st.subheader("Eficiência por Município")
    st.info("Aqui teremos um mapa interativo com os indicadores locais.")

st.success("Estrutura da Etapa 1 concluída com sucesso!")
