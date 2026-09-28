FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
ENV TOPOLOGY_PATH=/app/configs/topology.json
ENV LAYOUT_PATH=/app/configs/layout.json
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
