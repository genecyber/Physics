# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install any needed packages
RUN pip install numpy pillow nltk

# Download necessary NLTK data
RUN python -m nltk.downloader punkt words averaged_perceptron_tagger

# Copy the source code and data into the container
COPY src/ ./src
COPY data/ ./data

# Set the command to run the script
CMD ["python", "src/process_data.py"]
