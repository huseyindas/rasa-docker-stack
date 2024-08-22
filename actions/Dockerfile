ARG RASA_SDK_VERSION
FROM rasa/rasa-sdk:${RASA_SDK_VERSION}

WORKDIR /app

USER root

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/actions

USER 1001