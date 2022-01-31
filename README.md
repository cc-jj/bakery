# TODO
1. ~~Auth~~
2. OrderBy
3. ~~Migrations~~
4. Async
5. ~~Pagination~~
6. ~~CORS~~
7. Logging (Uvicorn and Python)
8. Frontend (templates)

# Installation
```bash
python -V  # 3.9.7
pipenv install --dev
```

# Tests
```bash
pytest tests
```

# Configuration
Settings are configured through environment variables, see [settings.py](./src/settings.py).

With environment variables set, launch the app or migrate the database like so:
```bash
./run.py app launch                # launch the app
./run.py db update                 # migrate the db to the latest revision
./run.py --help                    # see all commands
```

# API Docs
```commandline
http://localhost:3000/docs/
```

# Migrations in detail
The database uri is configured in [alembic/env.py](./alembic/env.py) (see `database.engine` and `settings.SQLALCHEMY_DATABASE_URI`).  

Then, the migrations are auto generated from the SqlAlchemy models. After making a change to the models, apply the change to the database like so:
```bash
./run.py db create-migration     # create a new migration revision
./run.py db update               # migrate the database to the latest revision
```
