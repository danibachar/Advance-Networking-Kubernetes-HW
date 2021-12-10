FROM python:3.6

RUN mkdir -p /app

COPY /app.py/ /app
COPY /requirements.txt/ /app
RUN pip3 install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
# For local testing
EXPOSE 8080
CMD ["python", "app.py"]
