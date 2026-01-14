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
# CONFIGURAÇÕES DE PÁGINA
# =========================
st.set_page_config(
    page_title="FitMentor",
    page_icon="💪",
    layout="centered"
)

# =========================
# ESTILO GLOBAL (CSS)
# =========================
st.markdown("""
<style>
/* BACKGROUND */
body {
  background-color: #F8F9FA;
}

/* CARD / FORM */
section[data-testid="stForm"] {
  background-color: #FFFFFF;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #E0E0E0;
  box-shadow: 0px 0px 6px rgba(0,0,0,0.06);
}

/* INPUTS */
.stTextInput>div>div>input,
.stNumberInput>div>div>input,
.stSelectbox>div>div>div,
.stTextArea>div>div>textarea {
  border-radius: 8px;
  border: 1px solid #D1D5DB;
  padding: 10px;
  background-color: white;
}

/* BOTÕES */
.stButton>button {
    background-color: #1E7F6C;
    color: white;
    border-radius: 8px;
    padding: 12px 18px;
    font-size: 15px;
}

/* ESTILIZAÇÃO DE RESULTADO */
.result-box {
  background-color: #FFFFFF;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #D1D5DB;
  margin-top: 10px;
}

h1, h2, h3, .css-1d391kg {
    color: #2C3E50;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGO
# =========================
st.image("logo.png", width=200)

st.title("FitMentor")
st.caption("Treinos personalizados com Inteligência Artificial")

# =========================
# BACKEND
# =========================
API_URL = "https://fitmentor-backend-0kfp.onrender.com/gerar-treino"

# =========================
# FORMULÁRIO
with st.form("form_aluno"):
    st.subheader("📋 Dados do Aluno")

    nome = st.text_input("Nome do aluno")
    whatsapp = st.text_input("📱 WhatsApp (com DDD)", placeholder="21999999999")

    idade = st.number_input("Idade", min_value=0, max_value=100)
    altura = st.number_input("Altura (m)", min_value=0.0, max_value=2.5)
    peso = st.number_input("Peso (kg)", min_value=0.0, max_value=250.0)

    nivel = st.selectbox("Nível", ["Iniciante", "Intermediário", "Avançado"])

    objetivos = st.multiselect(
        "🎯 Objetivos (selecione um ou mais)",
        [
            "Emagrecimento",
            "Hipertrofia",
            "Condicionamento físico",
            "Reabilitação",
            "Qualidade de vida",
            "Performance esportiva"
        ]
    )

    st.subheader("🧠 Estilo de Vida")

    bebe = st.selectbox("Consome álcool?", ["Não", "Raramente", "Frequentemente"])
    fuma = st.selectbox("Fuma?", ["Não", "Raramente", "Frequentemente"])
    alimentacao = st.selectbox("Alimentação", ["Ruim", "Regular", "Boa"])
    sono = st.selectbox("Horas de sono", ["Menos de 5h", "5–6h", "6–7h", "7–8h", "8h+"])

    st.subheader("❤️ Saúde do Aluno")

    cirurgia = st.selectbox(
        "Já fez alguma cirurgia que impacta o treino?",
        ["Não", "Sim"]
    )

    cirurgia_local = ""
    cirurgia_tempo = 0

    if cirurgia == "Sim":
        cirurgia_local = st.text_input("📍 Onde foi a cirurgia?")
        cirurgia_tempo = st.number_input(
            "⏱️ Há quantos anos foi a cirurgia?",
            min_value=0,
            max_value=50,
            step=1
        )

    coracao = st.selectbox("Possui problema cardíaco?", ["Não", "Sim"])
    tontura = st.selectbox("Sente tontura ou desmaios?", ["Não", "Sim"])
    dor_peito = st.selectbox("Sente dores no peito durante esforço?", ["Não", "Sim"])
    liberacao = st.selectbox("Possui liberação médica?", ["Sim", "Não"])

    observacoes_saude = st.text_area("Observações de saúde (opcional)")

    submit = st.form_submit_button("🚀 Gerar Plano de Treino")

# =========================
# RESULTADO
if submit:

    if not nome or not objetivos:
        st.warning("Preencha o nome e selecione objetivos.")
        st.stop()

    imc = calcular_imc(peso, altura)
    classificacao, cor = classificar_imc(imc)

    with st.spinner("Gerando plano…"):
        response = requests.post(API_URL, json={
            "nome": nome,
            "idade": idade,
            "altura": altura,
            "peso": peso,
            "nivel": nivel,
            "objetivo": objetivos
        })

    if response.status_code == 200:
        st.markdown(f"<div class='result-box'><strong>IMC:</strong> {imc} ({classificacao})</div>", unsafe_allow_html=True)

        plano = response.json().get("plano", "")
        st.markdown(f"<div class='result-box'>{plano}</div>", unsafe_allow_html=True)
    else:
        st.error("Erro ao gerar plano.")
