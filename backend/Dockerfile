FROM minizinc/minizinc:2.5.5

# Install Python3.8 and some packages
RUN apt update \
    && apt install -yqq wget git gnupg curl python3.8 python3-pip libmysqlclient-dev
RUN pip3 install pipenv
RUN pip3 install gunicorn

# Copy source files
COPY . /app
WORKDIR /app
RUN pipenv install --system --deploy

# Expose web server port & execute
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers=2", "--threads=2", "--timeout=1800", "--log-level=debug", "--pythonpath", "/", "application:app"]