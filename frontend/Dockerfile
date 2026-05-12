FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y curl build-essential libpq-dev \
	&& pip install --no-cache-dir -r requirements.txt \
	&& groupadd -r streamgroup || true \
	&& useradd -r -g streamgroup -m streamuser || true \
	&& apt-get remove -y build-essential \
	&& apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY app.py ./
COPY proxy.py ./
RUN chown -R streamuser:streamgroup /app || true

USER streamuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
	CMD curl -f http://localhost:8501/ || exit 1

CMD ["/bin/sh", "-c", "streamlit run app.py --server.port=8502 --server.address=0.0.0.0 --server.headless=true & uvicorn proxy:app --host 0.0.0.0 --port=8501 --proxy-headers"]
