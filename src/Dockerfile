FROM python:3.9-slim-bullseye

ARG BUILD_DATE
ARG VCS_REF

LABEL maintainer="devon.warren@gmail.com"
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="devonwarren/pod-labeler-webhook"
LABEL org.label-schema.url="https://github.com/devonwarren/pod-labeler-webhook"
LABEL org.label-schema.vcs-url="https://github.com/devonwarren/pod-labeler-webhook"
LABEL org.label-schema.vcs-ref=$VCS_REF

# port for webhook api
EXPOSE 8443/tcp

# allow verbose logging if set to true
ENV DEBUG="false"

# list of labels to copy from namespace into pods. separate by commas or wildcard to copy all
ENV LABELS="*"

# setup app directory with code/user
WORKDIR /app
RUN adduser -u 1001 webapp -q && chown webapp:webapp /app
COPY --chown=webapp:webapp . /app

# get required dependencies
RUN pip3 install -r /app/requirements.txt && chown webapp:webapp `which uvicorn`

# run as non-root user
USER webapp

# uvicorn will run the fastapi app using mounted tls files
ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "--port", "8443", "--ssl-keyfile", "/app/ssl/tls.key", "--ssl-certfile", "/app/ssl/tls.crt", "main:app" ]
