### RUNNING WITH DOCKER-COMPOSE

Since there is a bunch of services (App itself, Postgres, Nginx with Certbot, Celery and Celery-Beat with Redis) 
it makes sense to run them in containers with docker and docker-compose.
So, make sure you have [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/install/)
installed on the machine.

With docker installed, cd to the working directory (where you have pulled the repo inti)
and - for development purposes - run:
```
$ docker-compose -f docker-compose.dev.yaml up -d
```

This way, you will pull the already built image of the django-based project - as well as all the
other necessary images - and run them in daemon mode. Visit the localhost at port 8000, with the
debug-mode on.

Stop the containers, removing all the data (i.e. returning you to the position 
before they were launched) by:
```
$ docker-compose -f docker-compose.dev.yaml down -v
```
Skip the `-v` flag to keep the data collected (database entries, static files, etc.)
while containers were active:
```
$ docker-compose -f docker-compose.dev.yaml down
```
This way, if you run the containers again with the `up` directive, you will be able to
further use all the data collected before you stopped the containers.

You are always able to check running containers with...
```
$ docker ps
```
...as well all the containers available with:
```
$ docker ps -a
```
To check which images have been built or pulled by you and are currently available, run:
```
$ docker images
```
To clear all stale images, inactive containers as well as the data associated with it, run:
```
$ docker system prune --volumes
```
### BUILDING WITH DOCKER
As for the program image itself, you can always build an image by yourself instead of pulling the pre-built
from dockerhub. This is actually unavoidable when further changes to the program
made and need to be fixed as an image. So, staying in the working directory, run this command to build an image:
```
$ docker build -t <image name> .
```
If you performed changes to the image name or version, you will need to amend the docker-compose
file, substituting the image's default name with the one you gave it in the "docker build" command.

### DEPLOYING WITH DOCKER-COMPOSE

Running yours services in production will not differ a lot what has been
done in development. You will have to add to the working directory two 
environment variables files: `.web_prod.env` and `.db_prod.env`. If you prefer to
give other names to those files, amend the docker-compose.prod.yaml file, 
providing new files' names in the `env_file:` sections. If you stick to the default names, let 
us immediately move further.

Those `rename_web_prod_env.py` and `rename_db_prod_env.py` files in misc directory are here for
your convenience. Fill in the variables listed in them, remove whitespaces before
and after assignment `=`, and rename the files to `.web_prod.env` and `.db_prod.env`.
Make sure the databases' variables in .db_prod.env match those in .web_prod.env.

In the working directory on your production server, run...
```
$ docker-compose -f docker-compose.prod.yaml up -d
```
...and visit your web-page.