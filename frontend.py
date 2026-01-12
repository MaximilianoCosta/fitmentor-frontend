import streamlit as st
import requests

# =========================
# CONFIGURAÇÕES GERAIS
# =========================
st.set_page_config(
    page_title="FitMentor",
    page_icon="💪",
    layout="centered"
)

# ====== PERSONALIZAÇÃO FÁCIL ======
PRIMARY_COLOR = "#2ECC71"      # Verde principal
SECONDARY_COLOR = "#1F2937"    # Cinza escuro
BACKGROUND_COLOR = "#F9FAFB"   # Fundo claro

# =========================
# ESTILO GLOBAL
# =========================
st.markdown(
    f"""
    <style>
    body {{
        background-color: {BACKGROUND_COLOR};
    }}
    .stButton>button {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border-radius: 12px;
        height: 52px;
        font-size: 16px;
        font-weight: bold;
    }}
    h1, h2, h3 {{
        color: {SECONDARY_COLOR};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# LOGO E BANNER
# =========================
st.image("logo.png", width=180)
st.image("banner.png", use_container_width=True)

st.title("FitMentor")
st.caption("Plataforma inteligente para Professores de Educação Física e Personal Trainers")

st.title("💪 FitMentor")
st.subheader("Plano de treino inteligente para seus alunos")

# =========================
# URL DO BACKEND
# =========================
API_URL = "https://fitmentor-backend-0kfp.onrender.com/gerar-treino"

# =========================
# FORMULÁRIO DO ALUNO
# =========================
with st.form("form_aluno"):
    st.subheader("📋 Dados do Aluno")

    nome = st.text_input("Nome do aluno")
    idade = st.number_input("Idade", min_value=0, max_value=100)
    altura = st.number_input("Altura (m)", min_value=0.0, max_value=2.5)
    peso = st.number_input("Peso (kg)", min_value=0.0, max_value=250.0)

    nivel = st.selectbox("Nível", ["Iniciante", "Intermediário", "Avançado"])
    objetivo = st.text_area("Objetivo do treino")

    st.subheader("🧠 Estilo de Vida")

    bebe = st.selectbox("Consome álcool?", ["Não", "Raramente", "Frequentemente"])
    fuma = st.selectbox("Fuma?", ["Não", "Raramente", "Frequentemente"])
    anabol = st.selectbox("Usa anabolizantes?", ["Não", "Já usou", "Usa atualmente"])
    alimentacao = st.selectbox("Alimentação", ["Ruim", "Regular", "Boa"])
    sono = st.selectbox("Horas de sono", ["Menos de 5h", "5–6h", "6–7h", "7–8h", "8h+"])

    detalhes = ""
    if bebe != "Não" or fuma != "Não" or anabol != "Não":
        detalhes = st.text_input("Detalhe (qual, frequência, histórico)")

    submit = st.form_submit_button("🚀 Gerar Plano de Treino")

# =========================
# ENVIO PARA BACKEND
# =========================
if submit:
    if not nome or not objetivo:
        st.warning("Preencha o nome e o objetivo do aluno.")
    else:
        payload = {
            "nome": nome,
            "idade": idade,
            "altura": altura,
            "peso": peso,
            "nivel": nivel,
            "objetivo": objetivo,
            "estilo_vida": {
                "bebe": bebe,
                "fuma": fuma,
                "anabolizante": anabol,
                "alimentacao": alimentacao,
                "sono": sono,
                "detalhes": detalhes
            }
        }

        with st.spinner("Gerando plano com IA..."):
            response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            plano = response.json()["plano"]
