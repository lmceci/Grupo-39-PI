import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página (Deve ser a primeira linha do Streamlit)
st.set_page_config(page_title="Dashboard SAMU 192", page_icon="🚑", layout="wide")

# 2. Carregando os dados com "memória" (Cache) para não travar o computador
@st.cache_data
def carregar_dados():
    # O Streamlit vai ler o arquivo na pasta data
    df = pd.read_csv('data/samuppc.csv')
    
    # Converte a coluna de data para o formato correto de tempo
    df['dt_competencia'] = pd.to_datetime(df['dt_competencia'])
    return df

df = carregar_dados()

# 3. Criando o Menu Lateral (Sidebar)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Samu_logo.svg/1200px-Samu_logo.svg.png", width=150)
st.sidebar.title("Filtros")

# Filtro de Região
regioes = df['no_regiao_brasil'].unique().tolist()
regiao_selecionada = st.sidebar.multiselect("Selecione a Região:", regioes, default=regioes)

# Filtro de Estado (UF) dinâmico com base na região
ufs_filtradas = df[df['no_regiao_brasil'].isin(regiao_selecionada)]['sg_uf'].unique().tolist()
uf_selecionada = st.sidebar.multiselect("Selecione o Estado (UF):", ufs_filtradas, default=ufs_filtradas)

# Aplicando os filtros na base de dados
df_filtrado = df[(df['no_regiao_brasil'].isin(regiao_selecionada)) & (df['sg_uf'].isin(uf_selecionada))]

# 4. Título Principal da Página
st.title("🚑 Painel de Monitoramento: Eficiência do SAMU 192")
st.markdown("Projeto Integrador - Grupo 39 | Análise de Cobertura e Desempenho")
st.divider() # Linha de separação

# 5. Indicadores Principais (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    media_nacional = df_filtrado['vl_indicador_calculado_br'].mean()
    st.metric(label="Média do Indicador Nacional", value=f"{media_nacional:.1f}%")
with col2:
    media_municipal = df_filtrado['vl_indicador_calculado_mun'].mean()
    st.metric(label="Média dos Municípios Filtrados", value=f"{media_municipal:.1f}%")
with col3:
    total_municipios = df_filtrado['no_municipio'].nunique()
    st.metric(label="Municípios Analisados", value=total_municipios)

st.markdown("---")

# 6. Gráficos
col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.subheader("📈 Evolução do Atendimento ao Longo do Tempo")
    # Agrupando os dados por data para ver a evolução da média municipal
    evolucao = df_filtrado.groupby('dt_competencia')['vl_indicador_calculado_mun'].mean().reset_index()
    fig_linha = px.line(evolucao, x='dt_competencia', y='vl_indicador_calculado_mun', 
                       labels={'dt_competencia': 'Data', 'vl_indicador_calculado_mun': 'Indicador (%)'},
                       markers=True)
    st.plotly_chart(fig_linha, use_container_width=True)

with col_grafico2:
    st.subheader("📊 Desempenho Médio por Estado")
    # Agrupando por UF para ver quem tem a melhor média
    desempenho_uf = df_filtrado.groupby('sg_uf')['vl_indicador_calculado_mun'].mean().reset_index().sort_values(by='vl_indicador_calculado_mun', ascending=False)
    fig_barra = px.bar(desempenho_uf, x='sg_uf', y='vl_indicador_calculado_mun',
                       labels={'sg_uf': 'Estado', 'vl_indicador_calculado_mun': 'Indicador Médio (%)'},
                       color='vl_indicador_calculado_mun', color_continuous_scale='Blues')
    st.plotly_chart(fig_barra, use_container_width=True)

st.markdown("---")

# 7. Tabela de Atenção (Municípios abaixo da média nacional)
st.subheader("⚠️ Municípios que requerem atenção")
st.write("Abaixo estão os municípios cujo indicador está **menor que a média nacional** no período mais recente.")

# Pegar apenas a data mais recente disponível nos dados
data_recente = df_filtrado['dt_competencia'].max()
df_recente = df_filtrado[df_filtrado['dt_competencia'] == data_recente]

# Filtrar quem está abaixo da média do BR (comparando a coluna do municipio com a do BR)
df_abaixo_media = df_recente[df_recente['vl_indicador_calculado_mun'] < df_recente['vl_indicador_calculado_br']]

# Mostrando as colunas mais importantes de forma limpa
tabela_atencao = df_abaixo_media[['sg_uf', 'no_municipio', 'vl_indicador_calculado_mun', 'vl_indicador_calculado_br']]
tabela_atencao.columns = ['Estado', 'Município', 'Indicador Local (%)', 'Média Nacional (%)']

st.dataframe(tabela_atencao, use_container_width=True)
