# dbasik

## Revising the application in 2022

The objective here is to deploy the application using Docker in 2022. Because I don't know Docker, this is a learning experience and the K.I.S.S principle applies in handfuls.

## Objectives

* Get the application running locally using a Python virtualenv but Postgres and Celery running in a Docker container.
  * Use basic Dockerfiles for each of these (no `docker-compose.yml` files)
    * Create a new branch for the work (DONE)
    * Create Dockerfile to get Postgres running. Check it you can log into it with credentials, create a database, create tables and output queries.
    * Create a Dockerfile for Celery. No idea at this point what that requires.
    * Get the application running locally.
    * Handle pinning of dependencies.
* Run the application with an added Python Docker container. All running locally.