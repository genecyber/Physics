# Build stage for React app
FROM node:14-buster-slim as node-base
WORKDIR /node_app
COPY react_app/package*.json ./
RUN npm install
COPY react_app/ ./
RUN npm run build

# Final stage
FROM python:3.8-slim
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install flask flask-cors

# Copy application code
COPY app/ /app/app/
COPY --from=node-base /node_app/build/ /app/static/

ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

CMD ["python3", "-c", "from app import create_app; app = create_app(); app.run(host='0.0.0.0', port=5001)"]
