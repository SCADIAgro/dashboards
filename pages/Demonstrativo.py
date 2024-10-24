import streamlit as st
import pandas as pd
import requests
import json as j
import plotly.express as px
import locale

st.set_page_config(layout= 'wide')

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html= True)

# Define o locale para formato monetário brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

## Funções
# Função para obter as safras
def obter_safras(url, header):
    try:
        resposta = requests.get(url, headers = header)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a API: {e}")
    except ValueError as e:
        st.error(f"Erro ao carregar os dados: {e}")

# Função para obter o token
def obter_token():
    return st.query_params["token"]

# Função para obter a URL do servidor
def obter_url_servidor():
    return st.query_params["url"]

# Função para obter a URL das safras
def obter_url_safras(url_base):
    return f"http://{url_base}/api/safras"

# Função para obter a URL do demonstrativo
def obter_url_demonstrativo(url_base):
    return f"http://{url_base}/api/resultados/demonstrativo"

# Obtém o token
token = obter_token()

# Obtém a url do servidor
url_servidor = obter_url_servidor()

### Criação do Sidebar e dos Filtros
st.sidebar.title('Filtros')

## Criação da lista do Filtro de Safras
url_safras = obter_url_safras(url_servidor)
param_token = {
    "x-access-token": token
}
safras = obter_safras(url_safras, param_token)

df_safras = pd.DataFrame(safras, columns = ["safra"])

# Adicionando uma nova coluna formatada
df_safras['safra_formatada'] = df_safras['safra'].astype(str).str[:2] + '/' + df_safras['safra'].astype(str).str[2:]

with st.sidebar.expander('Safras'):
    filtro_safras = st.selectbox('Selecione', options = df_safras["safra_formatada"], placeholder = 'Opções')
    safra_selecionada = filtro_safras.replace("/", "")

if filtro_safras:
    safra_selecionada = filtro_safras.replace("/", "")

# URL Demonstrativo
url_demonstrativo = obter_url_demonstrativo(url_servidor)
param_safra = {
  "safra": safra_selecionada
}

header_demonstrativo = {
    "x-access-token": token,
    "params": j.dumps(param_safra)
}

with st.spinner("Carregando dados... "):
    try:
        # Fazendo a requisição GET para consumir os dados
        respostaDados = requests.get(url_demonstrativo, headers = header_demonstrativo)
        respostaDados.raise_for_status()
        jsonDados = respostaDados.json()

        # Pegando a Safra 
        safra = jsonDados['safra']
        subtitulo_safra = f"Safra: {safra[:2]}/{safra[2:]}"

        ### Exibindo o título
        st.title("Demonstrativo")

        # Extração e Tratamento dos dados
        atividades = jsonDados['atividades']
        lista_atividades = []
        lista_itens = []
        for dado in atividades:
            cod_atividade = dado["codAtividade"]
            desc_atividade = dado["atividade"]
            receita = dado["demonstrativo"]["receita"]
            despesa = dado["demonstrativo"]["despesa"]["total"]
            resultado = dado["demonstrativo"]["resultado"]

            for i in dado["demonstrativo"]["despesa"]["itens"]:
                item = {
                    "atividade": dado["atividade"],
                    "descricao": i["descConta"],
                    "valor": i ["valor"]
                }
                lista_itens.append(item)

            desc_resultado = ""
            if resultado < 0:
                desc_resultado = "(Prejuízo)"
            if resultado > 0:
                desc_resultado = "(Lucro)"

            lucratividade = 0
            if receita != 0:
                lucratividade = resultado / receita * 100

            rentabilidade = 0
            if despesa != 0:
                rentabilidade = (receita - despesa) / despesa * 100
            
            nova_atividade = {
                "codigo_atividade" : cod_atividade,
                "descricao_atividade" : desc_atividade,
                "receita" : receita,
                "despesa" : despesa,
                "resultado" : resultado,
                "descricao_resultado": desc_resultado,
                "lucratividade" : round(lucratividade, 2),
                "rentabilidade" : round(rentabilidade, 2)
            }
            lista_atividades.append(nova_atividade)

        # Carregando os dados em um DataFrame
        df_item = pd.DataFrame(lista_itens)

        df = pd.DataFrame(lista_atividades)

        ## Criação da lista do Filtro de Atividade
        df_atividade = pd.DataFrame(df, columns = ["codigo_atividade", "descricao_atividade"])
        with st.sidebar.expander('Atividade'):
            filtro_atividade = st.selectbox('Selecione', options = df_atividade['descricao_atividade'], placeholder = 'Opções')

        if filtro_atividade:
            df = df[df["descricao_atividade"] == filtro_atividade]
            df_item = df_item[df_item["atividade"] == filtro_atividade]
        else:
            primeira_atividade = df_atividade["descricao_atividade"].iloc[0]
            df = df[df["descricao_atividade"] == primeira_atividade]
            df_item = df_item[df_item["descricao_atividade"] == primeira_atividade]

        ### Exibindo Subtítulo
        colunasubtitulo1, colunasubtitulo2 = st.columns(2)
        with colunasubtitulo1:
            st.subheader(filtro_atividade)
        with colunasubtitulo2:
            st.subheader(subtitulo_safra)

        # Tabela de Despesa dos Itens
        despesa_itens = df_item[["descricao", "valor"]].copy()
        despesa_itens["valor_formatado"] = despesa_itens["valor"].apply(lambda x: locale.currency(x, grouping=True))

        tb_despesa_itens = despesa_itens[["descricao", "valor_formatado"]].copy()
        tb_despesa_itens.rename(columns={"descricao": "Descrição"}, inplace=True)
        tb_despesa_itens.rename(columns={"valor_formatado": "Valor"}, inplace=True)
        
        # Tabela Receita x Despesa
        df_receita_despesa = df.melt(id_vars =  ["codigo_atividade", "descricao_atividade"], value_vars = ["receita", "despesa"], var_name= "tipo", value_name = "valor")

        receita_despesa = df_receita_despesa[["tipo", "valor"]].copy()
        receita_despesa["tipo"] = receita_despesa["tipo"].str.capitalize()
        receita_despesa["valor_formatado"] = receita_despesa["valor"].apply(lambda x: locale.currency(x, grouping=True))

        #Tabela Resultados
        df_resultados = df.melt(id_vars =  ["codigo_atividade", "descricao_atividade", "descricao_resultado"], value_vars = ["resultado"], var_name= "tipo", value_name = "valor")
        descricao_resultado_formatado = "Resultado " + df_resultados.loc[0, "descricao_resultado"]
        resultado_formatado = locale.currency(df_resultados.loc[0, "valor"], grouping = True)  
        
        #Tabela Lucratividade x Rentabilidade
        df_lucratividade_rentabilidade = df.melt(id_vars =  ["codigo_atividade", "descricao_atividade"], value_vars = ["lucratividade", "rentabilidade"], var_name= "tipo", value_name = "valor")

        lucratividade_rentabilidade = df_lucratividade_rentabilidade[["tipo", "valor"]].copy()
        lucratividade_rentabilidade["tipo"] = lucratividade_rentabilidade["tipo"].str.capitalize()

        lucratividade_formatado = f"{lucratividade_rentabilidade.loc[0, 'valor']} %"
        rentabilidade_formatado = f"{lucratividade_rentabilidade.loc[1, 'valor']} %"
        
        ## Criação dos gráficos
        fig_atividades = px.bar(receita_despesa, y = "tipo", x = "valor", category_orders = {"tipo": ["Receita", "Despesa"]}, title = 'Receita x Despesa')
        fig_atividades.update_traces(marker_color=["#75587A", "#DD482F"],
                                     customdata = receita_despesa["valor_formatado"],
                                     hovertemplate = "%{customdata}",
                                     text = receita_despesa["valor_formatado"])

        fig_atividades.update_layout(xaxis_title = "", yaxis_title = "")

        ### Exibição do Corpo do Dashboard
        coluna1, coluna2 = st.columns(2)
        with coluna1:
            st.plotly_chart(fig_atividades)
        with coluna2:
            with st.container():
                st.divider()
                st.metric(descricao_resultado_formatado, resultado_formatado)
                coluna3, coluna4 = st.columns(2)
                with coluna3:
                    st.metric("Rentabilidade ", rentabilidade_formatado)
                with coluna4:
                    st.metric("Lucratividade ", lucratividade_formatado)
                st.divider()
                with st.expander('Despesas'):
                    #st.plotly_chart(fig_despesa_itens)
                    st.dataframe(tb_despesa_itens, use_container_width = True, hide_index = True)
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a API: {e}")
    except ValueError as e:
        st.error(f"Erro ao carregar os dados: {e}")
