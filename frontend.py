import streamlit as st
import requests

# =========================
# FUNÇÕES IMC
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
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="FitMentor",
    page_icon="💪",
    layout="centered"
)

# =========================
# ESTILO GLOBAL
# =========================
st.markdown("""
<style>
.stButton>button {
    background-color: #2ECC71;
    color: white;
    border-radius: 12px;
    height: 52px;
    font-size: 16px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGO E BANNER
# =========================
st.image("logo.png", width=180)
st.image("banner.png", use_container_width=True)

st.title("💪 FitMentor")
st.caption("Plano de treino inteligente com apoio de IA")

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
    whatsapp = st.text_input("📱 WhatsApp do aluno (com DDD)", placeholder="Ex: 21999999999")

    idade = st.number_input("Idade", min_value=0, max_value=100)
    altura = st.number_input("Altura (m)", min_value=0.0, max_value=2.5)
    peso = st.number_input("Peso (kg)", min_value=0.0, max_value=250.0)

    nivel = st.selectbox("Nível", ["Iniciante", "Intermediário", "Avançado"])

    objetivos = st.multiselect(
        "🎯 Objetivo do treino",
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
    liberacao = st.selectbox("Possui liberação médica para treino?", ["Sim", "Não"])

    observacoes_saude = st.text_area("Observações adicionais de saúde (opcional)")

    submit = st.form_submit_button("🚀 Gerar Plano de Treino")

# =========================
# RESULTADOS
# =========================
if submit:

    if not nome or not objetivos:
        st.warning("Preencha o nome e selecione ao menos um objetivo.")
        st.stop()

    imc = calcular_imc(peso, altura)
    classificacao, cor = classificar_imc(imc)

    st.subheader("📊 Avaliação Física")
    st.markdown(
        f"<h3 style='color:{cor}'>IMC: {imc} — {classificacao}</h3>",
        unsafe_allow_html=True
    )

    payload = {
        "nome": nome,
        "idade": idade,
        "altura": altura,
        "peso": peso,
        "nivel": nivel,
        "objetivo": objetivos,
        "contato": {
            "whatsapp": whatsapp
        },
        "estilo_vida": {
            "bebe": bebe,
            "fuma": fuma,
            "alimentacao": alimentacao,
            "sono": sono
        },
        "saude": {
            "cirurgia": cirurgia,
            "local_cirurgia": cirurgia_local,
            "anos_cirurgia": cirurgia_tempo,
            "problema_cardiaco": coracao,
            "tontura": tontura,
            "dor_peito": dor_peito,
            "liberacao_medica": liberacao,
            "observacoes": observacoes_saude
        }
    }

    with st.spinner("Gerando plano de treino com IA..."):
        response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        plano = response.json().get("plano", "")
        st.subheader("📄 Plano de Treino Gerado")
        st.write(plano)
    else:
        st.error("Erro ao gerar plano. Verifique o backend.")
