import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard SAMU 192", page_icon="🚑", layout="wide")

# 2. Função inteligente para encontrar o arquivo CSV
@st.cache_data
def carregar_dados():
    # Este comando descobre o caminho da pasta onde este script (dashboard.py) está
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Ele sobe um nível e entra na pasta 'data' para buscar o arquivo
    caminho_csv = os.path.join(diretorio_atual, '..', 'data', 'samuppc.csv')
    
    # Carrega o arquivo
    df = pd.read_csv(caminho_csv)
    
    # Converte a coluna de data para o formato correto
    df['dt_competencia'] = pd.to_datetime(df['dt_competencia'])
    return df

# Tentativa de carregar os dados com tratamento de erro amigável
try:
    df = carregar_dados()
except Exception as e:
    st.error(f"Erro ao encontrar a base de dados: {e}")
    st.info("Certifique-se de que o arquivo 'samuppc.csv' está dentro da pasta 'data'.")
    st.stop()

# 3. Menu Lateral
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Samu_logo.svg/1200px-Samu_logo.svg.png", width=150)
st.sidebar.title("Filtros de Análise")

# Filtros dinâmicos
regioes = df['no_regiao_brasil'].unique().tolist()
regiao_selecionada = st.sidebar.multiselect("Selecione a Região:", regioes, default=regioes)

ufs_filtradas = df[df['no_regiao_brasil'].isin(regiao_selecionada)]['sg_uf'].unique().tolist()
uf_selecionada = st.sidebar.multiselect("Selecione o Estado (UF):", ufs_filtradas, default=ufs_filtradas)

# Aplicar Filtros
df_filtrado = df[(df['no_regiao_brasil'].isin(regiao_selecionada)) & (df['sg_uf'].isin(uf_selecionada))]

# 4. Cabeçalho
st.title("🚑 Painel de Monitoramento: Eficiência do SAMU 192")
st.markdown(f"**Análise de Cobertura e Desempenho** | Dados atualizados até {df['dt_competencia'].max().strftime('%m/%Y')}")
st.divider()

# 5. Cartões de Indicadores (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    media_br = df_filtrado['vl_indicador_calculado_br'].mean()
    st.metric(label="Média Nacional", value=f"{media_br:.1f}%")
with col2:
    media_loc = df_filtrado['vl_indicador_calculado_mun'].mean()
    st.metric(label="Média Local (Filtro)", value=f"{media_loc:.1f}%", delta=f"{media_loc - media_br:.1f}%")
with col3:
    total_mun = df_filtrado['no_municipio'].nunique()
    st.metric(label="Municípios na Seleção", value=total_mun)

st.markdown("---")

# 6. Gráficos Interativos
col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("📈 Tendência de Desempenho")
    evolucao = df_filtrado.groupby('dt_competencia')['vl_indicador_calculado_mun'].mean().reset_index()
    fig_line = px.line(evolucao, x='dt_competencia', y='vl_indicador_calculado_mun', 
                        title="Média de Indicadores por Mês",
                        labels={'dt_competencia': 'Mês/Ano', 'vl_indicador_calculado_mun': 'Indicador (%)'})
    st.plotly_chart(fig_line, use_container_width=True)

with col_dir:
    st.subheader("📊 Ranking por Estado")
    ranking_uf = df_filtrado.groupby('sg_uf')['vl_indicador_calculado_mun'].mean().reset_index().sort_values('vl_indicador_calculado_mun')
    fig_bar = px.bar(ranking_uf, x='vl_indicador_calculado_mun', y='sg_uf', orientation='h',
                      title="Desempenho Médio por UF",
                      labels={'vl_indicador_calculado_mun': 'Eficiência (%)', 'sg_uf': 'Estado'},
                      color='vl_indicador_calculado_mun', color_continuous_scale='Reds')
    st.plotly_chart(fig_bar, use_container_width=True)

# 7. Tabela de Detalhes
st.divider()
st.subheader("📋 Detalhamento dos Municípios")
st.dataframe(df_filtrado[['no_municipio', 'sg_uf', 'vl_indicador_calculado_mun', 'vl_indicador_calculado_br']].sort_values('vl_indicador_calculado_mun'), 
             use_container_width=True)
