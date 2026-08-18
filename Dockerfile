FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FEIDE_USERNAME=""
ENV FEIDE_PASSWORD=""

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN playwright install chromium

COPY . .

CMD ["python3", "src/cmd.py"]
