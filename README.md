# Sharegut API

## Preparation

Create the database tables:

```bash
> alembic upgrade head
```

(to regenerate the alembic migrations, delete `database.db` and `db/versions/*`, do `alembic revision --autogenerate -m "Init tables"`)

Start the server:
```bash
> uvicorn main:app --reload --root-path /api
```
