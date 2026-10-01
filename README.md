# Product Prep OS

A personal, local-first Django web application for an 8-week product-company interview sprint.

## What it includes
- Dashboard with overall weighted completion percentage.
- Roadmap showing phase → chapter → problem progress.
- Difficulty points: Easy 10, Medium 20, Hard 30.
- Persistent completion, notes, confidence and spaced-review schedule.
- Daily study-session log.
- Automatic phase completion state and congratulations screen.
- Personal-only local design: no registration, no cloud account, no multi-user model.
- Django admin for editing the roadmap/problems.
- SQLite zero-setup mode and PostgreSQL support via `.env`.

## Run locally (fastest)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_roadmap
python manage.py runserver
```
Open http://127.0.0.1:8000/

## PostgreSQL
Copy `.env.example` to `.env`, create the `product_prep` database, update credentials, then run:
```bash
python manage.py migrate
python manage.py seed_roadmap
python manage.py runserver
```

## Useful commands
```bash
python manage.py createsuperuser
python manage.py runserver
```
Admin: http://127.0.0.1:8000/admin/

## Reset progress
Use the dashboard's **Reset personal progress** button. It clears completion/review/session data but preserves the roadmap.
