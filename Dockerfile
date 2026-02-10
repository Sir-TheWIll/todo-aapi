# BUG #2: Wrong Python version - Python 2.7 is deprecated!
FROM python:3.13.5-slim

# Set working directory
# BUG #3: Typo in WORKDIR path - should be /app not /ap
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY todos.json .

# BUG #4: Wrong port exposed - app runs on 5000 but we expose 8000!
EXPOSE 5000

# Set environment variable
ENV PORT=5000

# BUG #5: Wrong CMD format - should use JSON array format
CMD ["python", "app.py"]