# dbasik

## Revising the application in 2022

The objective here is to deploy the application using Docker in 2022. Because I don't know Docker, this is a learning experience and the K.I.S.S principle applies in handfuls.

## Objectives

* Get the application running locally using a Python virtualenv but Postgres and Celery running in a Docker container.
  * Use basic Dockerfiles for each of these (no `docker-compose.yml` files)
    * Create a new branch for the work (DONE)
    * Create Dockerfile to get Postgres running. Check it you can log into it with credentials, create a database, create tables and output queries. (DONE)
    * Get the application running locally. (DONE)
    * Handle pinning of dependencies. (TODO)
* Run the application with an added Python Docker container. All running locally. (DONE)

## Running the containers

### Install Docker and docker-compose

* Install `docker`: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository. You want to be able to run docker as non-superuser so ensure you follow the simple steps at https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user. Ensure you reboot your machine for the changes to take effect.
* Install `docker-compose`: https://docs.docker.com/compose/install/#install-compose-on-linux-systems.

### Running the development server

* To run the Django development server: `docker-compose -f docker-compose.yml up`. This will start the `app` and `db` service. The `db` service uses postgres which takes a few seconds to configure and set up - the `app` service (Django) depends on postgres so you will see messages in your terminal telling you whether the database is ready or not. Django should wait for postgres to be ready. When it is, the migrations will run etc and you should see the familiar Django development service message, advertising the application running on 127.0.0.1:8000.
* You need to create a superuser so you can access the admin. To do that, Ctrl-C the running containers - give them a moment to stop, then run `docker-compose -f docker-compose.yml run app sh -c "python manage.py createsuperuser"`. Add your details as usual. Then to get the server running again, repeat the `docker-compose -f docker-compose.yml up` command.
* To stop the server, Ctrl-C, then `docker-compose -f docker-compose.yml down`.

### Running the production server

* The production configuration is far more robust and uses nginx as a reverse proxy, with uswgi as the Django application server. This is intended to be run on a production server but can be tested locally too in the same way that the development server is run.
* You need an `.env` file in the root of the project (not included in the repo as it is intended to contain secrets). For testing, copy `.env.sample` to `.env` and provide some different settings or just use the ones provided - they're fine for testing.
* To run the production containers: `docker-compose -f docker-compose-deploy.yml up`. The site will be available at `127.0.0.1/admin` (note: `:8000` not required as this is running on default browser port 80).
* Take the same steps as above to stop the server and create a superuser: Ctrl-C the running containers, `docker-compose -f docker-compose-deploy.yml run app sh -c "python manage.py createsuperuser"`, then `docker-compose -f docker-compose-deploy.yml up` to get it running again.
* To stop the server, Ctrl-C, then `docker-compose -f docker-compose-deploy.yml down`.

### Debugging with VSCode

* Remove existing volumes - `docker images prune`.
* Run `make COMPOSEFILE=docker-compose-debug.yml clean-rebuild-and-run`.
* Run `make createsuperuser`.
* Run `make create-financial-quarters`.