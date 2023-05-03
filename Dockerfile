FROM python:3.9-slim-buster

# Install required packages
RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy the application files into the container
COPY . /app
WORKDIR /app

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default port
EXPOSE 8501

# Start the Streamlit application
CMD ["streamlit", "run", "--server.port=8501", "--server.enableCORS=false", "app.py"]
