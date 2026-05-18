FROM python:3.8-slim
WORKDIR /WORKDIR
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8001
ENTRYPOINT ["python", "app/main.py"]