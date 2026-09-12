#FROM python:3.13-alpine3.20
FROM python:3.14.6-slim-trixie

# Установка Allure
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless curl tar && \
    curl -o allure-2.13.8.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz && \
    tar -zxvf allure-2.13.8.tgz -C /opt/ && \
    ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure && \
    rm allure-2.13.8.tgz && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /usr/workspace
COPY ./requirements.txt /usr/workspace
RUN pip install -r requirements.txt

