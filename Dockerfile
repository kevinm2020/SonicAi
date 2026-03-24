# Use Python 3.11 for Flask compatibility
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy project files
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for FastAPI/Flask
EXPOSE 8888

# Command to run FastAPI backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]