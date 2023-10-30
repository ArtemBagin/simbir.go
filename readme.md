# Simbir.go

**Для запуска:**
- Добавить в проект .env по примеру example.env
- `pip install -r requirements.txt`
- `cd src`
- `alembic upgrade head`
- `uvicorn main:app --reload`

**Создание суперпользователя:**
- `cd src`
- `python create_admin.py`

Документация(swagger) - http://127.0.0.1:8000/docs
