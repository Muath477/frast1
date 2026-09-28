# All-in-one image: nginx (UI) + uvicorn (API/WS) on port 8080
FROM node:22-alpine AS febuild
WORKDIR /fe
COPY frontend/package*.json ./
RUN npm ci
COPY frontend ./
COPY configs /configs
RUN npm run build

FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends nginx \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
COPY configs ./configs
COPY --from=febuild /fe/dist /usr/share/nginx/html
COPY deploy/nginx-allinone.conf /etc/nginx/sites-available/default
RUN rm -f /etc/nginx/sites-enabled/default \
  && ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default \
  && mkdir -p /app/data
ENV TOPOLOGY_PATH=/app/configs/topology.json
ENV LAYOUT_PATH=/app/configs/layout.json
ENV ROOTIQ_MODE=sim
EXPOSE 8080
COPY deploy/start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
