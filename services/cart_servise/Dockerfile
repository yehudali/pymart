# שימוש בפייתון מתקדם משאר הסרוויסים!
FROM python:3.11-slim

WORKDIR /WORKDIR
COPY ./services/cart_servise/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./services/cart_servise .
EXPOSE 8003
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]