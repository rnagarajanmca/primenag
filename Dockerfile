# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
ARG NODE_VERSION=22.12.0

FROM node:${NODE_VERSION}-slim AS frontend
WORKDIR /app

COPY webapp/package*.json ./webapp/
RUN cd webapp && npm install

COPY webapp ./webapp
RUN cd webapp && npm run build

FROM python:${PYTHON_VERSION}-slim AS backend
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/src

FROM backend AS dev
COPY --from=frontend /app/webapp/dist ./webapp/dist

CMD ["bash"]
