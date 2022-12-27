FROM python:3.7-alpine
WORKDIR /source
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY source/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY source/ .
CMD ["ls"]
CMD ["flask", "run"]
