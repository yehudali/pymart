FROM python:3.8-slim
WORKDIR /WORKDIR
COPY ./services/catalog_management/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "./app/main.py"]