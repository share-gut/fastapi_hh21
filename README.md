# Sharegut API

## Preparation

Python - requirements:

```bash
> apt install python3-pip python3-virtualenv
> virtualenv venv
> . ./venv/bin/activate
> pip3 install -r requirements.txt
```

Create the database tables:

```bash
> alembic upgrade head
```

(to regenerate the alembic migrations, delete `database.db` and `db/versions/*`, do `alembic revision --autogenerate -m "Init tables"`)

Start the server:
```bash
> uvicorn main:app --reload --root-path /api
```
