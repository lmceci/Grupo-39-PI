import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import os

# ─────────────────────────────────────────────
# 1. CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SAMU 192 – Cobertura Brasil",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado
st.markdown("""
<style>
    /* Fonte e fundo geral */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Cartões de KPI */
    [data-testid="metric-container"] {
        background: #f8fafd;
        border: 1px solid #e0e7ef;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 2px 8px rgba(0,51,102,0.06);
    }
    [data-testid="metric-container"] label { color: #5a6a7e; font-size: 13px; font-weight: 600; }
    [data-testid="metric-container"] [data-testid="metric-value"] { color: #003366; font-size: 28px; font-weight: 700; }

    /* Sidebar */
    section[data-testid="stSidebar"] { background: #003366; }
    section[data-testid="stSidebar"] * { color: #e8f0fe !important; }
    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] { background: #1a4d99; }

    /* Títulos de seção */
    h3 { color: #003366 !important; border-bottom: 2px solid #e63946; padding-bottom: 6px; }

    /* Divisor */
    hr { border-top: 1px solid #dde5ef; }

    /* Alertbox informativo */
    .info-box {
        background: #eaf1fb;
        border-left: 6px solid #003366;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 22px;
    }
    .info-box h4 { margin: 0 0 6px 0; color: #003366; }
    .info-box p  { margin: 0; color: #31333F; font-size: 15px; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 2. CARREGAMENTO DOS DADOS  (path robusto)
# ─────────────────────────────────────────────
@st.cache_data
def carregar_dados() -> pd.DataFrame:
    """
    Localiza o CSV relativo a este script, independente de onde
    o terminal foi aberto. Estrutura esperada:
        Grupo-39-Pi-main/
            app/dashboard.py   ← este arquivo
            data/samuppc.csv
    """
    pasta_script = os.path.dirname(os.path.abspath(__file__))   # .../app
    pasta_raiz   = os.path.dirname(pasta_script)                 # .../Grupo-39-Pi-main
    caminho_csv  = os.path.join(pasta_raiz, "data", "samuppc.csv")

    if not os.path.exists(caminho_csv):
        st.error(
            f"❌ Arquivo não encontrado em:\n\n`{caminho_csv}`\n\n"
            "Verifique se a pasta `data/` e o arquivo `samuppc.csv` "
            "estão ao lado da pasta `app/`."
        )
        st.stop()

    with open(caminho_csv, "r", encoding="latin1") as f:
        conteudo = f.read().replace('"', "")

    df = pd.read_csv(io.StringIO(conteudo), sep=",", on_bad_lines="skip", engine="python")
    df.columns = df.columns.str.strip().str.lower()

    df["dt_competencia"]            = pd.to_datetime(df["dt_competencia"], errors="coerce")
    df["vl_indicador_calculado_mun"] = pd.to_numeric(df["vl_indicador_calculado_mun"], errors="coerce").fillna(0)
    df["ano"] = df["dt_competencia"].dt.year

    return df


df_total = carregar_dados()


# ─────────────────────────────────────────────
# 3. BARRA LATERAL – FILTROS
# ─────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/SAMU_logo.svg/320px-SAMU_logo.svg.png",
    width=100,
)
st.sidebar.title("🚑 SAMU 192")
st.sidebar.markdown("---")

# Ano
anos_disponiveis = sorted(df_total["ano"].dropna().unique(), reverse=True)
ano_sel = st.sidebar.selectbox("📅 Ano de competência:", anos_disponiveis, index=0)

df_ano = df_total[df_total["ano"] == ano_sel]

# Região
regioes = ["Todas"] + sorted(df_ano["no_regiao_brasil"].dropna().unique())
regiao_sel = st.sidebar.multiselect(
    "🗺️ Região:", regioes, default=["Todas"]
)
if "Todas" in regiao_sel or not regiao_sel:
    df_reg = df_ano.copy()
else:
    df_reg = df_ano[df_ano["no_regiao_brasil"].isin(regiao_sel)]

# Estado
estados = ["Todos"] + sorted(df_reg["sg_uf"].dropna().unique())
estado_sel = st.sidebar.multiselect(
    "📍 Estado (UF):", estados, default=["Todos"]
)
if "Todos" in estado_sel or not estado_sel:
    df_f = df_reg.copy()
else:
    df_f = df_reg[df_reg["sg_uf"].isin(estado_sel)]

st.sidebar.markdown("---")
st.sidebar.caption("Fonte: Ministério da Saúde / SAMU 192")


# ─────────────────────────────────────────────
# 4. CABEÇALHO
# ─────────────────────────────────────────────
st.title("🚑 Cobertura Operacional do SAMU 192 – Brasil")

st.markdown(f"""
<div class="info-box">
  <h4>Índice de Conformidade Municipal – {ano_sel}</h4>
  <p>
    Painel com a cobertura operacional do <b>SAMU 192</b> por município.
    O indicador mede se a cidade atende às exigências federais de cobertura
    (≥ 100 % = <b>conforme</b>). A base contempla apenas os municípios
    habilitados ou em qualificação junto ao Ministério da Saúde.
  </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 5. KPIs
# ─────────────────────────────────────────────
media_nac   = df_ano["vl_indicador_calculado_mun"].mean()
media_sel   = df_f["vl_indicador_calculado_mun"].mean()
mun_total   = df_f[["no_municipio", "sg_uf"]].drop_duplicates().shape[0]
mun_conf    = df_f[df_f["vl_indicador_calculado_mun"] >= 100][["no_municipio", "sg_uf"]].drop_duplicates().shape[0]
pct_conf    = (mun_conf / mun_total * 100) if mun_total else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("🌎 Média Nacional",   f"{media_nac:.1f}%")
k2.metric("📍 Média na Seleção", f"{media_sel:.1f}%",  delta=f"{media_sel - media_nac:.1f}%")
k3.metric("🏙️ Cidades Analisadas", f"{mun_total:,}".replace(",", "."))
k4.metric("✅ Cidades com Cobertura", f"{mun_conf:,}".replace(",", "."),
          delta=f"{pct_conf:.1f}% do total")

st.divider()


# ─────────────────────────────────────────────
# 6. LINHA 1 – Gráfico por UF  +  Gráfico por Região
# ─────────────────────────────────────────────
col_uf, col_reg = st.columns([1.4, 0.6])

with col_uf:
    st.markdown("### 📊 Média de Cobertura por Estado (UF)")
    ranking_uf = (
        df_f.groupby("sg_uf")["vl_indicador_calculado_mun"]
        .mean()
        .reset_index()
        .sort_values("vl_indicador_calculado_mun", ascending=True)
    )
    ranking_uf["cor"] = ranking_uf["vl_indicador_calculado_mun"].apply(
        lambda x: "#e63946" if x < 60 else ("#f4a261" if x < 100 else "#2a9d8f")
    )

    fig_uf = go.Figure(go.Bar(
        x=ranking_uf["vl_indicador_calculado_mun"],
        y=ranking_uf["sg_uf"],
        orientation="h",
        marker_color=ranking_uf["cor"],
        text=ranking_uf["vl_indicador_calculado_mun"].map(lambda v: f"{v:.1f}%"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Cobertura média: %{x:.1f}%<extra></extra>",
    ))
    fig_uf.add_vline(x=100, line_dash="dash", line_color="#003366",
                     annotation_text="Meta 100%", annotation_position="top right")
    fig_uf.update_layout(
        height=max(420, len(ranking_uf) * 28),
        margin=dict(l=0, r=60, t=10, b=0),
        xaxis_title="Cobertura (%)",
        yaxis_title="",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#eaeef4"),
    )
    st.plotly_chart(fig_uf, use_container_width=True)

with col_reg:
    st.markdown("### 🗺️ Cobertura por Região")
    ranking_reg = (
        df_f.groupby("no_regiao_brasil")["vl_indicador_calculado_mun"]
        .mean()
        .reset_index()
        .rename(columns={"no_regiao_brasil": "Região", "vl_indicador_calculado_mun": "Cobertura"})
        .sort_values("Cobertura", ascending=False)
    )
    cores_reg = ["#003366", "#1a4d99", "#2a7fbf", "#4aa3d9", "#78c4e8"]
    fig_reg = go.Figure(go.Bar(
        x=ranking_reg["Cobertura"],
        y=ranking_reg["Região"],
        orientation="h",
        marker_color=cores_reg[:len(ranking_reg)],
        text=ranking_reg["Cobertura"].map(lambda v: f"{v:.1f}%"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>%{x:.1f}%<extra></extra>",
    ))
    fig_reg.update_layout(
        height=300,
        margin=dict(l=0, r=60, t=10, b=0),
        xaxis_title="Cobertura (%)",
        yaxis_title="",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#eaeef4"),
    )
    st.plotly_chart(fig_reg, use_container_width=True)

    # Pizza: possui cobertura vs não possui cobertura
    st.markdown("### ✅ Conformidade Municipal")
    conf_counts = df_f["vl_indicador_calculado_mun"].apply(
        lambda x: "Possui Cobertura" if x >= 100 else "Não possui Cobertura"
    ).value_counts().reset_index()
    conf_counts.columns = ["Status", "Qtd"]

    fig_pizza = px.pie(
        conf_counts, names="Status", values="Qtd",
        color="Status",
        color_discrete_map={"Possui Cobertura": "#2a9d8f", "Não possui Cobertura": "#e63946"},
        hole=0.45,
    )
    fig_pizza.update_layout(
        height=260,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=True,
        legend=dict(orientation="h", y=-0.1),
    )
    st.plotly_chart(fig_pizza, use_container_width=True)


st.divider()


# ─────────────────────────────────────────────
# 7. TABELA DE MUNICÍPIOS
# ─────────────────────────────────────────────
st.markdown("### 📋 Municípios – Status de Cobertura")

busca = st.text_input("🔍 Buscar município:", placeholder="Ex: Campinas")

tabela = df_f[["no_municipio", "sg_uf", "vl_indicador_calculado_mun"]].copy()
tabela["Status"] = tabela["vl_indicador_calculado_mun"].apply(
    lambda x: "✅ Possui Cobertura" if x >= 100 else "❌ Não possui Cobertura"
)
tabela.columns = ["Município", "UF", "Cobertura (%)", "Status"]

if busca:
    tabela = tabela[tabela["Município"].str.contains(busca, case=False, na=False)]

tabela_agg = (
    tabela.groupby(["Município", "UF"])
    .agg({"Status": "last"})
    .reset_index()
    .sort_values(["UF", "Município"])
)

st.dataframe(tabela_agg, hide_index=True, height=420, use_container_width=True)
st.caption(f"{len(tabela_agg):,} municípios exibidos".replace(",", "."))

st.divider()
st.caption("Dados: Ministério da Saúde – SAMU 192 · Painel desenvolvido com Streamlit + Plotly")
