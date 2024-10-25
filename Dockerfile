# app/Dockerfile

FROM python:3.11.4

WORKDIR /app

COPY ./.streamlit ./.streamlit
COPY ./fonts ./fonts
COPY ./css ./css
COPY ./pages ./pages
COPY ./requirements.txt .
COPY ./Home.py .

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y --no-install-recommends locales; rm -rf /var/lib/apt/lists/*; sed -i '/^#.* pt_BR.UTF-8 /s/^#//' /etc/locale.gen; locale-gen
RUN locale -a

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]