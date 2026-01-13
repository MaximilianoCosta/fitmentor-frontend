import streamlit as st
import requests

# =========================
# FUNÇÕES (TOPO DO ARQUIVO)
# =========================
def calcular_imc(peso, altura):
    if altura > 0:
        return round(peso / (altura ** 2), 2)
    return 0

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidade"

# =========================
# CONFIGURAÇÕES GERAIS
# =========================
st.set_page_config(
    page_title="FitMentor",
    page_icon="💪",
    layout="centered"
)

PRIMARY_COLOR = "#2ECC71"
SECONDARY_COLOR = "#1F2937"
BACKGROUND_COLOR = "#F9FAFB"

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
# LOGO E TÍTULO
# =========================
st.image("logo.png", width=180)
st.image("banner.png", use_container_width=True)

st.title("💪 FitMentor")
st.subheader("Plano de treino inteligente para seus alunos")

# =========================
# BACKEND
# =========================
API_URL = "https://fitmentor-backend-0kfp.onrender.com/gerar-treino"

# =========================
# FORMULÁRIO (SÓ INPUTS)
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
# PROCESSAMENTO (FORA DO FORM)
# =========================
if submit:
    if altura <= 0 or peso <= 0:
        st.error("Altura e peso devem ser maiores que zero.")
    elif not nome or not objetivo:
        st.warning("Preencha o nome e o objetivo do aluno.")
    else:
        # 👉 CÁLCULO DO IMC (AQUI É O LUGAR CERTO)
        imc = calcular_imc(peso, altura)
        classificacao = classificar_imc(imc)

        st.subheader("📊 Avaliação Física")
        st.success(f"IMC do aluno: **{imc}** ({classificacao})")

        # 👉 ENVIO PARA BACKEND
        payload = {
            "nome": nome,
            "idade": idade,
            "altura": altura,
            "peso": peso,
            "imc": imc,
            "classificacao_imc": classificacao,
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
            st.subheader("🏋️ Plano de Treino")
            st.markdown(plano)
        else:
            st.error("Erro ao gerar plano. Tente novamente.")
