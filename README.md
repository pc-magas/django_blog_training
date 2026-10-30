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

