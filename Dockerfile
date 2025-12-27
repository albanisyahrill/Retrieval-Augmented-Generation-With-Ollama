FROM python:3.12-bookworm AS builder

WORKDIR /opt/app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim-bookworm

WORKDIR /opt/app

COPY --from=builder /opt/venv /opt/venv

COPY . .

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=.

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]