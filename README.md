# Secunda API

REST API для справочника Организаций, Зданий, Деятельности.
## Что можно улучшить:
1) добавить тесты
2) доменный слой 
3) четче разделить границы слоев
4) работу с сессиями вынести в интеракторы или использовать UOW
5) Кастомная обработка ошибок при IntegrityError например

## Стек технологий

- FastAPI — веб-фреймворк
- **Pydantic** — валидация данных
- **SQLAlchemy** — ORM
- **Alembic** — миграции БД
- **Dishka** — Dependency Injection
- **PostgreSQL** — база данных
- **Docker** — контейнеризация

## Docker

```bash
# Клонировать репозиторий и перейти в директорию
cd secunda

# Запустить через Docker Compose
docker-compose up -d --build

# Применить миграции и заполнить тестовыми данными
docker-compose exec api alembic upgrade head
docker-compose exec api python -m scripts.seed
```

API доступен по адресу: http://localhost:8000

Swagger UI: http://localhost:8000/docs

## Локальная разработка

```bash
# Установить зависимости (требуется uv)
uv sync

# Создать .env файл
cp .env.example .env

# Запустить PostgreSQL (например, через Docker)
docker run -d --name postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=secunda \
  -p 5432:5432 \
  postgres:16-alpine

# Применить миграции
uv run alembic upgrade head

# Заполнить тестовыми данными
uv run python -m scripts.seed

# Запустить сервер
uv run python -m secunda.main
```

## API Endpoints

### Здания

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/buildings` | Список всех зданий |
| GET | `/buildings/{id}` | Здание по ID |
| POST | `/buildings` | Создать здание |

### Деятельности

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/activities` | Список всех деятельностей (дерево) |
| GET | `/activities/{id}` | Деятельность по ID |
| POST | `/activities` | Создать деятельность (макс. 3 уровня) |

### Организации

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/organizations/{id}` | Организация по ID |
| GET | `/organizations/building/{building_id}` | Организации в здании |
| GET | `/organizations/activity/{activity_id}` | Организации по виду деятельности (включая вложенные) |
| GET | `/organizations/search/name?name=...` | Поиск по названию |
| POST | `/organizations/search/radius` | Поиск в радиусе от точки |
| POST | `/organizations/search/rectangle` | Поиск в прямоугольной области |
| POST | `/organizations` | Создать организацию |

## Структура проекта

```
secunda/
├── scripts/
│   └── seed.py                 # Тестовые данные
├── src/secunda/
│   ├── application/            # Бизнес-логика
│   │   ├── dto.py
│   │   ├── entities.py
│   │   ├── interfaces.py       # 
│   │   └── interactors/        # Use cases
│   ├── infra/                  # Инфраструктура
│   │   ├── config.py
│   │   ├── di.py               # Dishka провайдеры
│   │   ├── migrations/          # Миграции БД (Alembic)
│   │   │   ├── alembic.ini
│   │   │   └── alembic/
│   │   │       ├── env.py
│   │   │       └── versions/
│   │   ├── database/
│   │   │   ├── models.py       # SQLAlchemy модели
│   │   │   └── session.py
│   │   └── repositories/       # Реализации репозиториев
│   ├── presentation/           # API слой
│   │   ├── dependencies.py
│   │   ├── schemas.py          # Pydantic схемы
│   │   └── routers/
│   └── main.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```
