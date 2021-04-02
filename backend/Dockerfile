FROM python:3.7-alpine

# Minizinc version to use
ENV asset_version=2.5.5

# Install Minizinc
ENV asset_filename "MiniZincIDE-$asset_version-bundle-linux-x86_64.tgz"
ENV asset_url "https://github.com/MiniZinc/MiniZincIDE/releases/download/$asset_version/MiniZincIDE-$asset_version-bundle-linux-x86_64.tgz"
RUN apk add --no-cache wget \
    && cd /usr/local \
    && wget -O $asset_filename $asset_url \
    && mkdir minizinc \
    && tar xfz $asset_filename  --directory minizinc --strip-components=1 \
    && cp minizinc/bin/* bin/ \
    && cp -ra minizinc/share/* share/ \
    && rm -rf minizinc \
    && rm -rf /var/cache/apk/*

# Copy source files
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN apk add gcc g++ make libffi-dev openssl-dev
RUN pip install pipenv
RUN pip install gunicorn
RUN pipenv install --system --deploy

# Expose web server port & execute
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--workers=2", "--threads=2", "--timeout=1800", "--log-level=debug", "--pythonpath", "/", "application:app"]