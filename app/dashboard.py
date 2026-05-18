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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* MUDANÇA DE BACKGROUND PARA CINZA ESCURO */
    .stApp { 
        background-color: #1e222b !important; 
    }

    /* Títulos Principais e de Seção em BRANCO */
    h1 { 
        color: #ffffff !important; 
    }
    h3 { 
        color: #ffffff !important; 
        border-bottom: 2px solid #e63946; 
        padding-bottom: 6px; 
    }

    /* Cartões de KPI com textos escuros para contraste no bloco claro */
    [data-testid="metric-container"] {
        background: #ffffff !important;
        border: 1px solid #e0e7ef;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    [data-testid="metric-container"] label { 
        color: #003366 !important; 
        font-size: 13px; 
        font-weight: 600; 
    }
    [data-testid="metric-container"] [data-testid="metric-value"] { 
        color: #111111 !important; 
        font-size: 28px; 
        font-weight: 700; 
    }

    /* Sidebar */
    section[data-testid="stSidebar"] { background: #003366; }
    section[data-testid="stSidebar"] * { color: #e8f0fe !important; }
    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] { background: #1a4d99; }

    /* Divisor */
    hr { border-top: 1px solid #3d4455 !important; }

    /* Alertbox informativo adaptada para o tema escuro */
    .info-box {
        background: #282e3d;
        border-left: 6px solid #e63946;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 22px;
    }
    .info-box h4 { margin: 0 0 6px 0; color: #ffffff; }
    .info-box p  { margin: 0; color: #cbd5e1; font-size: 15px; line-height: 1.5; }
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
