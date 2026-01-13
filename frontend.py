import streamlit as st
import requests

# =========================
# FUNÇÕES
# =========================
def calcular_imc(peso, altura):
    if altura > 0:
        return round(peso / (altura ** 2), 2)
    return 0

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso", "red"
    elif imc < 25:
        return "Peso normal", "green"
    elif imc < 30:
        return "Sobrepeso", "orange"
    else:
        return "Obesidade", "red"

# =========================
# CONFIGURAÇÕES
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
# ESTILO
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
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# LOGO
# =========================
st.image("logo.png", width=180)
st.image("banner.png", use_container_width=True)

st.title("💪 FitMentor")
st.subheader("Plano de treino inteligente")

# =========================
# BACKEND
# =========================
API_URL = "https://fitmentor-backend-0kfp.onrender.com/gerar-treino"

# =========================
# FORMULÁRIO
# =========================
with st.form("form_aluno"):
    st.subheader("📋 Dados do Aluno")

    nome = st.text_input("Nome do aluno")

    whatsapp = st.text_input(
        "📱 WhatsApp do aluno (com DDD)",
        placeholder="Ex: 21987654321"
    )

    idade = st.number_input("Idade", min_value=0, max_value=100)
    altura = st.number_input("Altura (m)", min_value=0.0, max_value=2.5)
    peso = st.number_input("Peso (kg)", min_value=0.0, max_value=250.0)

    nivel = st.selectbox("Nível", ["Iniciante", "Intermediário", "Avançado"])

    # 🎯 OBJETIVOS (MÚLTIPLA ESCOLHA)
    st.subheader("🎯 Objetivo do Treino")
    objetivos_opcoes = [
        "Emagrecimento",
        "Hipertrofia",
        "Condicionamento físico",
        "Definição muscular",
        "Saúde e qualidade de vida",
        "Reabilitação",
        "Performance esportiva"
    ]

    objetivos = st.multiselect(
        "Selecione um ou mais objetivos",
        objetivos_opcoes
    )

    # 🧠 ESTILO DE VIDA
    st.subheader("🧠 Estilo de Vida")

    bebe = st.selectbox("Consome álcool?", ["Não", "Raramente", "Frequentemente"])
    fuma = st.selectbox("Fuma?", ["Não", "Raramente", "Frequentemente"])
    alimentacao = st.selectbox("Alimentação", ["Ruim", "Regular", "Boa"])
    sono = st.selectbox("Horas de sono", ["Menos de 5h", "5–6h", "6–7h", "7–8h", "8h+"])

    # ❤️ SAÚDE (PAR-Q)
    st.subheader("❤️ Saúde do Aluno")

    cirurgia = st.selectbox("Já fez alguma cirurgia que impacta o treino?", ["Não", "Sim"])
    coracao = st.selectbox("Possui problema cardíaco?", ["Não", "Sim"])
    tontura = st.selectbox("Sente tontura ou já desmaiou?", ["Não", "Sim"])
    dor_peito = st.selectbox("Sente dor no peito ao se exercitar?", ["Não", "Sim"])
    liberacao = st.selectbox("Possui liberação médica?", ["Sim", "Não"])

    observacoes_saude = ""
    if cirurgia == "Sim" or coracao == "Sim" or tontura == "Sim" or dor_peito == "Sim":
        observacoes_saude = st.text_area(
            "Descreva detalhes importantes sobre a saúde do aluno"
        )

    submit = st.form_submit_button("🚀 Gerar Plano de Treino")

# =========================
# PROCESSAMENTO
# =========================
if submit:
    if not nome or not objetivos:
        st.warning("Preencha o nome e selecione ao menos um objetivo.")
    elif altura <= 0 or peso <= 0:
        st.error("Altura e peso inválidos.")
    else:
        # 📊 IMC
        imc = calcular_imc(peso, altura)
        classificacao, cor = classificar_imc(imc)

        st.subheader("📊 Avaliação Física")
        st.markdown(
            f"<h3 style='color:{cor}'>IMC: {imc} — {classificacao}</h3>",
            unsafe_allow_html=True
        )

        payload = {
            "nome": nome,
            "whatsapp": whatsapp,
            "idade": idade,
            "altura": altura,
            "peso": peso,
            "imc": imc,
            "classificacao_imc": classificacao,
            "nivel": nivel,
            "objetivos": objetivos,
            "estilo_vida": {
                "bebe": bebe,
                "fuma": fuma,
                "alimentacao": alimentacao,
                "sono": sono
            },
            "saude": {
                "cirurgia": cirurgia,
                "problema_cardiaco": coracao,
                "tontura": tontura,
                "dor_peito": dor_peito,
                "liberacao_medica": liberacao,
                "observacoes": observacoes_saude
            }
        }

        with st.spinner("Gerando plano com IA..."):
            response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            st.subheader("🏋️ Plano de Treino")
            st.markdown(response.json()["plano"])
        else:
            st.error("Erro ao gerar o plano.")
