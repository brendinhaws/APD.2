import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configurações da página
st.set_page_config(page_title="Relatório do Autoforno", layout="wide")

# Título e descrição
st.title("Relatório do Autoforno")
st.write("Bem-vindo ao painel de controle do Autoforno. Aqui você pode visualizar os dados de funcionamento.")

# Menu lateral
st.sidebar.title("Menu")
page = st.sidebar.radio("Navegação", ["Página Inicial", "Dados", "Gráfico"])

# Logo da empresa
st.sidebar.image("logo_empresa.png", use_column_width=True)

# Função para gerar dados fictícios
def gerar_dados():
    np.random.seed(0)
    horas = np.arange(1, 11)
    temperatura = np.random.randint(1500, 1650, size=10)
    pressao = np.random.randint(95, 105, size=10)
    producao = np.random.randint(200, 250, size=10)
    return pd.DataFrame({
        "Horas": horas,
        "Temperatura": temperatura,
        "Pressão": pressao,
        "Produção": producao
    })

# Página inicial
if page == "Página Inicial":
    st.header("Página Inicial")
    st.write("Esta é a página inicial do sistema de controle do autoforno.")
    if st.button("Clique para atualizar"):
        st.experimental_rerun()

# Página de dados
elif page == "Dados":
    st.header("Dados do Autoforno")
    df = gerar_dados()

    # Filtragem de dados
    temp_min = st.sidebar.slider("Temperatura mínima", int(df.Temperatura.min()), int(df.Temperatura.max()), int(df.Temperatura.min()))
    temp_max = st.sidebar.slider("Temperatura máxima", int(df.Temperatura.min()), int(df.Temperatura.max()), int(df.Temperatura.max()))

    df_filtrado = df[(df.Temperatura >= temp_min) & (df.Temperatura <= temp_max)]
    st.write(f"Exibindo dados para temperaturas entre {temp_min} e {temp_max}")
    st.table(df_filtrado)

    # Exportação de dados
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(label="Baixar CSV", data=csv, file_name='dados_autoforno.csv', mime='text/csv')

# Página de gráfico
elif page == "Gráfico":
    st.header("Gráfico de Funcionamento")
    df = gerar_dados()
    
    tipo_grafico = st.sidebar.selectbox("Tipo de gráfico", ["Linha", "Barra"])

    if tipo_grafico == "Linha":
        fig, ax = plt.subplots()
        ax.plot(df["Horas"], df["Temperatura"], marker='o', linestyle='-', color='b', label='Temperatura')
        ax.set_xlabel("Horas")
        ax.set_ylabel("Temperatura")
        ax.set_title("Temperatura ao Longo do Tempo")
        ax.legend()
        st.pyplot(fig)
    elif tipo_grafico == "Barra":
        fig, ax = plt.subplots()
        ax.bar(df["Horas"], df["Temperatura"], color='b', label='Temperatura')
        ax.set_xlabel("Horas")
        ax.set_ylabel("Temperatura")
        ax.set_title("Temperatura ao Longo do Tempo")
        ax.legend()
        st.pyplot(fig)

    # Estatísticas adicionais
    st.subheader("Estatísticas")
    st.write(df.describe())

    # Exportação de gráfico
    st.download_button(
        label="Baixar Gráfico",
        data=fig_to_image(fig),
        file_name='grafico_autoforno.png',
        mime='image/png'
    )

# Função auxiliar para converter gráfico em imagem
def fig_to_image(fig):
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf
