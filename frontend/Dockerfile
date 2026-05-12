FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
		&& groupadd -r streamgroup || true \
		&& useradd -r -g streamgroup -m streamuser || true

COPY app.py ./
RUN chown -R streamuser:streamgroup /app || true

USER streamuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
	CMD curl -f http://localhost:8501/ || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
