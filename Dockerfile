# Use stable Python version (3.13 may not be final yet)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app.py .
COPY todos.json .
# If you have a templates/ folder for index.html, copy it too:
# COPY templates/ templates/

# Expose the default port
EXPOSE 5000

# Set environment variable
ENV PORT=5000

# Run the app
CMD ["python", "app.py"]