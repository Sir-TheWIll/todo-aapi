FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY todos.json .
# Instead of COPY templates/ templates/, copy the file directly:
COPY templates/index.html templates/index.html

# Copy the styles too 
COPY static/app.js static/app.js 
COPY static/styles.css static/styles.css


EXPOSE 5000
ENV PORT=5000

CMD ["python", "app.py"]