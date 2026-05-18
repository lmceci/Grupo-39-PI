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

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], p, span, div, label, td, th {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Fundo principal */
    .stApp { background-color: #f4f6fb; }

    /* Sidebar escura e elegante */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001f4d 0%, #003380 100%);
        border-right: 1px solid #1a4d99;
    }
    section[data-testid="stSidebar"] * { color: #ddeeff !important; font-family: 'Montserrat', sans-serif !important; }
    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
        background: #e63946 !important;
        border-radius: 20px;
    }
    section[data-testid="stSidebar"] h1 {
        font-size: 22px !important;
        font-weight: 800 !important;
        letter-spacing: 1px;
        color: #ffffff !important;
    }

    /* KPI cards */
    [data-testid="metric-container"] {
        background: #ffffff;
        border: none;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 4px 20px rgba(0, 51, 128, 0.08);
        border-top: 4px solid #003366;
    }
    [data-testid="metric-container"] label {
        color: #7a8fa6 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        font-family: 'Montserrat', sans-serif !important;
    }
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #001f4d !important;
        font-size: 32px !important;
        font-weight: 800 !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Títulos h3 */
    h3 {
        color: #001f4d !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        letter-spacing: 0.5px;
        padding-bottom: 8px;
        border-bottom: 3px solid #e63946;
        display: inline-block;
    }

    /* Título principal */
    h1 {
        font-weight: 800 !important;
        color: #001f4d !important;
        letter-spacing: -0.5px;
    }

    /* Divisor */
    hr { border-top: 1px solid #dce3ef; margin: 10px 0; }

    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #001f4d 0%, #003380 100%);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(0, 31, 77, 0.18);
    }
    .info-box h4 {
        margin: 0 0 8px 0;
        color: #ffffff !important;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    .info-box p {
        margin: 0;
        color: #b0c8f0 !important;
        font-size: 14px;
        line-height: 1.7;
    }
    .info-box b { color: #ffffff !important; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f0f4fa; }
    ::-webkit-scrollbar-thumb { background: #003366; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 2. CARREGAMENTO DOS DADOS
# ─────────────────────────────────────────────
@st.cache_data
def carregar_dados() -> pd.DataFrame:
    pasta_script = os.path.dirname(os.path.abspath(__file__))
    pasta_raiz   = os.path.dirname(pasta_script)
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
    df["dt_competencia"]             = pd.to_datetime(df["dt_competencia"], errors="coerce")
    df["vl_indicador_calculado_mun"] = pd.to_numeric(df["vl_indicador_calculado_mun"], errors="coerce").fillna(0)
    df["ano"] = df["dt_competencia"].dt.year
    return df


df_total = carregar_dados()

FONT          = "Montserrat"
COR_PRINCIPAL = "#001f4d"
COR_ACENTO    = "#e63946"
COR_GRADE     = "#e8eef7"


# ─────────────────────────────────────────────
# 3. BARRA LATERAL – FILTROS
# ─────────────────────────────────────────────
st.sidebar.markdown("<h1>🚑 SAMU 192</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")

anos_disponiveis = sorted(df_total["ano"].dropna().unique(), reverse=True)
ano_sel = st.sidebar.multiselect(
    "📅 Ano(s) de competência:",
    anos_disponiveis,
    default=[anos_disponiveis[0]]
)
if not ano_sel:
    ano_sel = list(anos_disponiveis)

df_ano = df_total[df_total["ano"].isin(ano_sel)]

regioes = ["Todas"] + sorted(df_ano["no_regiao_brasil"].dropna().unique())
regiao_sel = st.sidebar.multiselect("🗺️ Região:", regioes, default=["Todas"])
if "Todas" in regiao_sel or not regiao_sel:
    df_reg = df_ano.copy()
else:
    df_reg = df_ano[df_ano["no_regiao_brasil"].isin(regiao_sel)]

estados = ["Todos"] + sorted(df_reg["sg_uf"].dropna().unique())
estado_sel = st.sidebar.multiselect("📍 Estado (UF):", estados, default=["Todos"])
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

anos_texto = ", ".join(str(a) for a in sorted(ano_sel))
st.markdown(f"""
<div class="info-box">
  <h4>Índice de Conformidade Municipal — {anos_texto}</h4>
  <p>
    Painel com a cobertura operacional do <b>SAMU 192</b> por município.
    O indicador mede se a cidade atende às exigências federais de cobertura
    (≥ 100% = <b>possui cobertura</b>). A base contempla apenas os municípios
    habilitados ou em qualificação junto ao Ministério da Saúde.
  </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 5. KPIs
# ─────────────────────────────────────────────
media_nac = df_ano["vl_indicador_calculado_mun"].mean()
media_sel = df_f["vl_indicador_calculado_mun"].mean()
mun_total = df_f[["no_municipio", "sg_uf"]].drop_duplicates().shape[0]
mun_conf  = df_f[df_f["vl_indicador_calculado_mun"] >= 100][["no_municipio", "sg_uf"]].drop_duplicates().shape[0]
pct_conf  = (mun_conf / mun_total * 100) if mun_total else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("🌎 Média Nacional",        f"{media_nac:.1f}%")
k2.metric("📍 Média na Seleção",      f"{media_sel:.1f}%", delta=f"{media_sel - media_nac:.1f}%")
k3.metric("🏙️ Cidades Analisadas",   f"{mun_total:,}".replace(",", "."))
k4.metric("✅ Cidades com Cobertura", f"{mun_conf:,}".replace(",", "."), delta=f"{pct_conf:.1f}% do total")

st.divider()


# ─────────────────────────────────────────────
# 6. GRÁFICOS – UF + REGIÃO + PIZZA
# ─────────────────────────────────────────────
col_uf, col_reg = st.columns([1.4, 0.6])

with col_uf:
    st.markdown("### 📊 Média de Cobertura por Estado (UF)")
    ranking_uf = (
        df_f.groupby("sg_uf")["vl_indicador_calculado_mun"]
        .mean().reset_index()
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
        marker_line_width=0,
        text=ranking_uf["vl_indicador_calculado_mun"].map(lambda v: f"{v:.1f}%"),
        textposition="outside",
        textfont=dict(family=FONT, size=11, color=COR_PRINCIPAL),
        hovertemplate="<b>%{y}</b><br>Cobertura média: %{x:.1f}%<extra></extra>",
    ))
    fig_uf.add_vline(x=100, line_dash="dot", line_color=COR_PRINCIPAL, line_width=2,
                     annotation_text="Meta 100%", annotation_position="top right",
                     annotation_font=dict(family=FONT, color=COR_PRINCIPAL, size=11))
    fig_uf.update_layout(
        height=max(440, len(ranking_uf) * 28),
        margin=dict(l=0, r=70, t=10, b=0),
        xaxis_title="Cobertura (%)",
        yaxis_title="",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor=COR_GRADE, tickfont=dict(family=FONT)),
        yaxis=dict(tickfont=dict(family=FONT, size=12)),
        font=dict(family=FONT),
        bargap=0.3,
    )
    st.plotly_chart(fig_uf, use_container_width=True)

with col_reg:
    st.markdown("### 🗺️ Cobertura por Região")
    ranking_reg = (
        df_f.groupby("no_regiao_brasil")["vl_indicador_calculado_mun"]
        .mean().reset_index()
        .rename(columns={"no_regiao_brasil": "Região", "vl_indicador_calculado_mun": "Cobertura"})
        .sort_values("Cobertura", ascending=False)
    )
    cores_reg = ["#001f4d", "#003380", "#1a5cb3", "#4a8fd9", "#85b8f0"]
    fig_reg = go.Figure(go.Bar(
        x=ranking_reg["Cobertura"],
        y=ranking_reg["Região"],
        orientation="h",
        marker_color=cores_reg[:len(ranking_reg)],
        marker_line_width=0,
        text=ranking_reg["Cobertura"].map(lambda v: f"{v:.1f}%"),
        textposition="outside",
        textfont=dict(family=FONT, size=11),
        hovertemplate="<b>%{y}</b><br>%{x:.1f}%<extra></extra>",
    ))
    fig_reg.update_layout(
        height=280,
        margin=dict(l=0, r=70, t=10, b=0),
        xaxis_title="Cobertura (%)",
        yaxis_title="",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor=COR_GRADE, tickfont=dict(family=FONT)),
        yaxis=dict(tickfont=dict(family=FONT, size=11)),
        font=dict(family=FONT),
        bargap=0.35,
    )
    st.plotly_chart(fig_reg, use_container_width=True)

    st.markdown("### ✅ Conformidade Municipal")
    conf_counts = df_f["vl_indicador_calculado_mun"].apply(
        lambda x: "Possui Cobertura" if x >= 100 else "Não possui Cobertura"
    ).value_counts().reset_index()
    conf_counts.columns = ["Status", "Qtd"]
    fig_pizza = px.pie(
        conf_counts, names="Status", values="Qtd",
        color="Status",
        color_discrete_map={"Possui Cobertura": "#2a9d8f", "Não possui Cobertura": "#e63946"},
        hole=0.5,
    )
    fig_pizza.update_traces(
        textfont=dict(family=FONT, size=12),
        marker=dict(line=dict(color="#ffffff", width=3)),
    )
    fig_pizza.update_layout(
        height=260,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=True,
        legend=dict(orientation="h", y=-0.15, font=dict(family=FONT, size=11)),
        font=dict(family=FONT),
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

st.divider()


# ─────────────────────────────────────────────
# 7. GRÁFICO DE LINHA – EVOLUÇÃO ANUAL
# ─────────────────────────────────────────────
st.markdown("### 📈 Evolução Anual da Cobertura")

evolucao = (
    df_f.groupby("ano")["vl_indicador_calculado_mun"]
    .mean().reset_index()
    .rename(columns={"ano": "Ano", "vl_indicador_calculado_mun": "Cobertura Média (%)"})
    .sort_values("Ano")
)

fig_evo = go.Figure()
fig_evo.add_trace(go.Scatter(
    x=evolucao["Ano"].astype(str),
    y=evolucao["Cobertura Média (%)"],
    mode="lines+markers+text",
    text=evolucao["Cobertura Média (%)"].map(lambda v: f"{v:.1f}%"),
    textposition="top center",
    textfont=dict(family=FONT, size=12, color=COR_PRINCIPAL),
    line=dict(color=COR_PRINCIPAL, width=3, shape="spline"),
    marker=dict(size=11, color=COR_ACENTO, line=dict(color="#ffffff", width=2)),
    fill="tozeroy",
    fillcolor="rgba(0,31,77,0.07)",
    hovertemplate="<b>%{x}</b><br>Cobertura: %{y:.1f}%<extra></extra>",
))
fig_evo.add_hline(
    y=100, line_dash="dot", line_color=COR_ACENTO, line_width=2,
    annotation_text="Meta 100%", annotation_position="top right",
    annotation_font=dict(family=FONT, color=COR_ACENTO, size=12),
)
fig_evo.update_layout(
    height=360,
    margin=dict(l=0, r=20, t=20, b=0),
    yaxis_title="Cobertura Média (%)",
    xaxis_title="Ano",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(gridcolor=COR_GRADE, tickfont=dict(family=FONT)),
    xaxis=dict(gridcolor=COR_GRADE, tickfont=dict(family=FONT, size=12)),
    font=dict(family=FONT),
)
st.plotly_chart(fig_evo, use_container_width=True)

st.divider()


# ─────────────────────────────────────────────
# 8. TABELA DE MUNICÍPIOS
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
st.caption("Dados: Ministério da Saúde – SAMU 192 · Desenvolvido com Streamlit + Plotly")
