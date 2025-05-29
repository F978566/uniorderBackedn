FROM python:3.11-bookworm

WORKDIR /app

RUN pip install --upgrade pip wheel

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]