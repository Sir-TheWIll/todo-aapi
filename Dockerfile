FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY todos.json .
COPY templates templates/   # ✅ NO trailing slash on source

EXPOSE 5000
ENV PORT=5000

CMD ["python", "app.py"]