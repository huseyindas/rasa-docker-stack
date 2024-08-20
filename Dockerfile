ARG RASA_SDK_VERSION
FROM rasa/rasa-sdk:${RASA_SDK_VERSION}

WORKDIR /app

USER root

COPY ./actions/requirements.txt .
RUN pip install -r requirements.txt

COPY ./actions /app/actions

USER 1001