FROM python:3.12-alpine3.18

RUN apk update \
    && apk add --no-cache postgresql-dev gcc musl-dev

ENV FLASK_DEBUG=True
ENV FLASK_APP=inf349
ENV REDIS_URL=redis://redis-container
ENV DB_HOST=postgres-container
ENV DB_USER=user
ENV DB_PASSWORD=pass
ENV DB_PORT=5432
ENV DB_NAME=api8inf349
ENV NO_PROXY=*
ENV OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# WORKDIR /inf349

COPY instance /instance
COPY orders_products /orders_products
COPY static /static
COPY templates /templates
COPY inf349.py inf349.py
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# RUN flask init-db

EXPOSE 5000

CMD [ "flask", "run" ]