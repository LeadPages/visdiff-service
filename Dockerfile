FROM python:2.7

# Copy files to src folder
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app

# Expose port 5000
EXPOSE 5000

# Add environment file
ENV CONFIG 'production'
RUN echo "FLASK_CONFIG=$CONFIG" > .env

# Install Pip requirements
RUN pip install -r requirements/production.txt

ENTRYPOINT ["python", "./manage.py"]
