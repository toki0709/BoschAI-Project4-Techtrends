# Set the base image
FROM python:3.8-slim-buster

LABEL mainitainer="Babatunde Adeyemi"

COPY ./techtrends /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN python init_db.py

EXPOSE 3111

ENTRYPOINT ["python", "app.py"]