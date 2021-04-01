FROM python:3.7

COPY . /app

WORKDIR /app

RUN pip install pipenv
RUN pip install gunicorn
RUN pipenv install --system --deploy


EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "--workers=2", "--threads=2", "--timeout=1800", "--log-level=debug", "--pythonpath", "/", "application:app"]