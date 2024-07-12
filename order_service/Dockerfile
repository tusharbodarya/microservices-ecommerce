FROM python:3.9

WORKDIR /order_service

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install pytest

COPY . .

CMD ["pytest", "tests"]
