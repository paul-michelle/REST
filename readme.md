### RUNNING WITH DOCKER

Since there is a bunch of services (App  with Databases, Nginx with Certbot, Celery and Celery-Beat with Redis) 
it makes sense to run them in containers via a composition.
So, make sure you have [docker](https://www.docker.com/) and docker-compose installed on the machine.

With docker istalled, cd to the working directory and - for development purposes - run:
```
$ docker-compose -f docker-compose.dev.yaml up -d
```
This way, you will pull the already built image of the django-based project - as well as all the
other necessary images - and run them in daemon mode. Visit the localhost at port 8000.

Alternatively, you can make an image by yourself - especially when further changes to the program
made and need to be fixed as an image - staying in the working directory and running:
```
$ docker build -t <image name> .
```
If you preferred to change the image name or version, you will need to amend the docker-compose
file, substituting the image's default name with the one you gave it in the "docker build" command.

### DEPLOYING WITH DOCKER

Running yours services in production will not differ a lot what has been
done in development. You will have to add to the working directory two 
environment variables files: `.web_prod.env` and `.db_prod.env`. If you prefer to
give other names to those files, amend the docker-compose.prod.yaml file, 
providing new files' names in the `env_file:` sections. If stick to the default names, let 
us immediately move further.

Those `rename_web_prod_env.py` and `rename_db_prod_env.py` files are here for
your convenience. Fill in the variables listed in them, remove whitespaces before
and after assignment `=`, and rename the files to `.web_prod.env` and `.db_prod.env`.
Make sure the databases' variables in .db_prod.env match those in .web_prod.env.

On your production server run:
```
$ docker-compose -f docker-compose.prod.yaml up -d

