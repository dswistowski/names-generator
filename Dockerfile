FROM python:3.10-slim
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app

WORKDIR $APP_HOME
COPY . ./
RUN pip install -r requirements.txt

CMD exec uvicorn names_generator.app:app --port $PORT --host 0.0.0.0