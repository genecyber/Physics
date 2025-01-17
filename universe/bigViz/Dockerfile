# Use a base image with Python
FROM python:3.8-slim

# Install curl and Node.js
RUN apt-get update && \
    apt-get install -y curl npm && \
    npm install -g n && \
    n stable && \
    npm install -g npm@latest

# Set working directory for the Python app
WORKDIR /app

# Copy Python requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python application into the container
COPY ./python_app ./python_app

# Set working directory for the Node.js app
WORKDIR /app/node_app

# Copy Node.js package files and install dependencies
COPY ./node_app/package.json .
RUN npm install

# Copy the Node.js application into the container
COPY ./node_app ./node_app

# Expose ports for both applications
EXPOSE 5010 
# Python app port
EXPOSE 3010       
# Node.js app port

# Command to run both applications
CMD ["sh", "-c", "python3 /app/python_app/racl.py & node /app/node_app/server.js"]