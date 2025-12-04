# Power Plant coding challenge

## Quickstart

Steps:

- Create a python virtual environemnt and activate it (tested with python version `3.13.9`).
- Install [uv](https://docs.astral.sh/uv/) and then install the dependencies as follows:

```bash
uv pip install -r requierements/requirements.txt
```

- Apply the migrations

```bash
src/manage.py migrate
```

- Run the development server with:

```bash
src/manage.py runserver localhost:8888
```