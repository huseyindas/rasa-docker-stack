FROM rasa/rasa-sdk:2.8.11

WORKDIR /app

USER root

RUN pip install redis aiohttp

COPY ./actions /app/actions

USER 1001