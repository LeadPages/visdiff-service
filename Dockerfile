FROM python:2.7

# Copy files to src folder
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app

# Expose port 5000
EXPOSE 5000

# Add environment file
ENV CONFIG 'production'

# Install Pip requirements
RUN pip install -r requirements/common.txt

ENTRYPOINT ["/usr/local/bin/gunicorn"]

CMD ["-w", "2", "-b",":5000","app"]
