FROM python:3.9.6-alpine as builder
ENV PYTHONFONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/web

RUN apk update && apk add postgresql-dev gcc libc-dev libffi-dev
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/web/wheels -r requirements.txt


FROM python:3.9.6-alpine

RUN mkdir -p /home/street_food

RUN addgroup -S street_food && adduser -S street_food -G street_food

ENV HOME=/home/street_food
ENV APP_HOME=/home/street_food/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

RUN apk update
COPY --from=builder /usr/src/web/wheels /wheels
COPY --from=builder /usr/src/web/requirements.txt .
RUN pip install -U pip && pip install --no-cache /wheels/*

COPY ./entrypoint.dev.sh .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.dev.sh
RUN chmod +x $APP_HOME/entrypoint.dev.sh

COPY . $APP_HOME

RUN chown -R street_food:street_food $APP_HOME

USER street_food

ENTRYPOINT ["sh", "/home/street_food/web/entrypoint.dev.sh"]
