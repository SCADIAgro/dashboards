# Dashboards

Projeto onde são hospedados os Dashboards criados com o Streamlit.

## Tecnologias Utilizadas
- [Python](https://www.python.org/) - Versão 3.11.4
- [Streamlit](https://streamlit.io/) - Versão 1.38.0
- [Pandas](https://pandas.pydata.org/) - Versão 2.2.3
- [Requests](https://docs.python-requests.org/en/latest/) - Versão 2.32.3
- [Plotly](https://plotly.com/python/) - Versão 5.24.1

## Instalação

Para rodar o projeto localmente, siga os passos abaixo:

1. Clone o repositório:

   ```bash
   git clone https://github.com/aloiziojr-scadi/dashboards.git 
   cd dashboards

2. Crie um ambiente virtual (opcional, mas recomendado):

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate  # No Linux use`source venv/bin/activate`

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt

## Executando o Aplicativo

Para iniciar o aplicativo Streamlit, execute o seguinte comando:

```bash
streamlit run Home.py
```
Os Dashboards estão armazenados na pasta pages, com suas respectivas documentações na pasta docs e acessíveis através do endereço http://localhost:8501/{nome-do-dashboard}/ recebendo os parâmetros 'url'  e 'token'. 

Exemplo: http://localhost:8501/Demonstrativo?url=endereco-servidor&token=valor-do-token


## Executando o Aplicativo via Docker Compose 
```bash
docker compose up
```

Obs: Caso seja executado via docker, a aplicação estará disponível na porta 7700, conforme especificado no arquivo docker-compose.yaml.

Exemplo: http://localhost:7700/{nome-do-dashboard}/