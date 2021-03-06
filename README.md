# Visdiff as a service #

Vaas is a visual comparison tool that compares two existing screenshots and reports the percent difference and raw pixel difference count. Additionally, it merges both images and overlays a color mask that makes it easy for a human to see where the differences are.  The base images are darkened and the differences are highlighted in yellow.

## Running Vaas ##

There are a number of different ways to run vaas:

### cli ###

With the pre-reqs in requirements install via pip run:

`python cli.py "IMAGE_ONE_LOCATION" "IMAGE_TWO_LOCATION" "DIFF_IMAGE_NAME"`

The comparison will be made between the two images, and a diff image will be output in the current working directory

### api ###

Swagger docs incoming

To start the server:

`gunicorn app -b :5000`

### Docker ###

With [docker](https://get.docker.com/) installed run:

`docker build -t "YOUR_IMAGE_NAME" .`

`docker run -p 5000:5000 YOUR_IMAGE_NAME`

### Docker Compose ###

With [Docker-Compose](https://docs.docker.com/compose/install/) installed run:

`docker-compose up -d`

To scale we instances run:

`docker-compose scale web=<n>`

### Testing ###

`pytest --cov=app -nauto tests/ --cov-report html:coverage/cov_html --cov-report xml:coverage/cov.xml --cov-report term`

`pytest --cov=app -nauto tests/`
