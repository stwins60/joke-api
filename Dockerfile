FROM python:3.12-slim AS build

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --target=/app/dependencies

COPY . .

FROM python:3.12-slim

WORKDIR /app

COPY --from=build /app .
COPY --from=build /app/dependencies /usr/local/lib/python3.12/site-packages
EXPOSE 5055

CMD ["python", "app.py"]