FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
COPY configs ./configs
RUN mkdir -p /app/data
ENV TOPOLOGY_PATH=/app/configs/topology.json
ENV LAYOUT_PATH=/app/configs/layout.json
ENV ROOTIQ_MODE=sim
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
