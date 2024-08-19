ARG RASA_SDK_VERSION
FROM rasa/rasa-sdk:${RASA_SDK_VERSION}

WORKDIR /app

USER root

RUN pip install redis aiohttp

COPY ./actions /app/actions

USER 1001