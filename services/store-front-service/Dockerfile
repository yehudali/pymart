FROM python:3.8-slim
WORKDIR /WORKDIR
COPY ./services/store-front-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app/catalog.py", "--server.port=8501", "--server.address=0.0.0.0"]