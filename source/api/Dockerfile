FROM python:3.12.0a5-alpine
WORKDIR /api
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY api/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY .env .env
COPY ./api .
CMD ["flask", "run"]
