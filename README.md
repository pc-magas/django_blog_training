# A simple Blog in Django

## About

This is a personal training project on Django. It is a simple blog where 2 user groups:

1. `Authors`: A user group that allows you to add and modify articles
2. `Editors`: A user group that edits, deleted and undeleted articles

## Local dev Setup:

Run:

```shell
docker compose up -d
```

## Managing Dependencies

We are using `uv` for dependency management. You can add a dependency as:

```shell
uv add <dependency-name>
```

Where `<dependency-name>` is the name from a dependency.

Tools using for development you can use the `--dev` option for example:

```shell
uv add --dev pytest
```

## Development shell

App runs inside a docker container in order to access the shell you need top run:

```shell
docker compose exec -ti django /bin/bash
```

## Production rehersal

Upon `docker-compose.testprod.yml` a production-ready image is being built and emulates a production environment.
In order to test build the image you need to run:

```shell
docker compose -f ./docker-compose.testprod.yml build django-testprod
```

Then run:

```shell
docker compose -f ./docker-compose.testprod.yml up -d
```

This is used in order to ensure that production image works as supposed to before deployment.
