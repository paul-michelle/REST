FROM python:3.9.6-alpine as builder
ENV PYTHONFONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/web

RUN apk update --no-cache && apk add postgresql-dev gcc libc-dev libffi-dev jpeg-dev zlib-dev linux-headers make
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/web/wheels -r requirements.txt

FROM python:3.9.6-alpine
ENV PYTHONFONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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

COPY . $APP_HOME

RUN chown -R street_food:street_food $APP_HOME

RUN for entrypoint in $APP_HOME/*.sh ; do sed -i "s/\r$//g" "$entrypoint" && chmod +x "$entrypoint" ; done

USER street_food