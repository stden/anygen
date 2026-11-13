# Environment Manager Agent: .env Security

## Назначение

Специализированный агент для безопасного управления конфиденциальными данными через файлы `.env`. Обеспечивает, что **логины, пароли, API-ключи, токены и локальные пути** НИКОГДА не попадают в git-репозиторий.

## Когда использовать

Вызывайте этого агента когда:
- Нужно добавить API-ключ или секрет в проект
- Настраиваете подключение к базе данных
- Требуется сохранить локальные пути
- Работаете с OAuth токенами, паролями
- Конфигурируете внешние сервисы

**Команда для вызова**:
```
"Добавь [секрет] в .env безопасно"
или
"ENV: Настрой переменные окружения для [сервис]"
```

## Что делает агент

### 1. Создание и настройка .env
- Создаёт `.env` файл если его нет
- Добавляет `.env` в `.gitignore`
- Создаёт `.env.example` как шаблон

### 2. Безопасное хранение секретов
- API ключи
- Пароли баз данных
- OAuth токены
- Приватные ключи
- Локальные пути пользователя

### 3. Документация
- Создаёт `.env.example` с описаниями
- Обновляет README с инструкциями
- Добавляет комментарии в .env

### 4. Валидация
- Проверяет, что .env в .gitignore
- Убеждается, что секреты не в коде
- Валидирует формат переменных

## Структура файлов

### `.env` (НЕ коммитится в git)
```bash
# Database Configuration
DATABASE_URL=postgresql://user:SecretP@ssw0rd@localhost:5432/mydb
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=admin
DATABASE_PASSWORD=SuperSecret123!

# API Keys (НИКОГДА не коммитить!)
OPENAI_API_KEY=sk-proj-AbC123XyZ...
STRIPE_SECRET_KEY=sk_live_51ABC...
GOOGLE_MAPS_API_KEY=AIza...

# OAuth
GITHUB_CLIENT_ID=Iv1.a629...
GITHUB_CLIENT_SECRET=1234567890abcdef...

# JWT Secrets
JWT_SECRET=your-256-bit-secret-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Local Paths (специфичны для пользователя)
PROJECT_ROOT=/path/to/your-project
UPLOAD_DIR=/var/data/uploads
LOG_PATH=/var/log/myapp

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=redis-secret

# Application Settings
DEBUG=True
LOG_LEVEL=DEBUG
SECRET_KEY=django-insecure-abc123...
```

### `.env.example` (КОММИТИТСЯ в git)
```bash
# Database Configuration
# Используйте PostgreSQL для production, SQLite для разработки
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password

# API Keys
# Получите ключи на https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-your-key-here

# Получите на https://stripe.com/docs/keys
STRIPE_SECRET_KEY=sk_test_your-key-here

# OAuth Settings
# Создайте OAuth App на https://github.com/settings/developers
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# JWT Configuration
# Сгенерируйте случайную строку: openssl rand -base64 32
JWT_SECRET=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Local Paths
# Укажите абсолютные пути к директориям
PROJECT_ROOT=/path/to/your/project
UPLOAD_DIR=/path/to/uploads
LOG_PATH=/path/to/logs

# Email (для Gmail используйте App Password)
# https://support.google.com/accounts/answer/185833
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-email-password

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=optional-redis-password

# Application
DEBUG=False
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key-here
```

### `.gitignore` (ОБЯЗАТЕЛЬНО!)
```gitignore
# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
ENV/

# Secrets and keys
*.pem
*.key
*.p12
secrets/
credentials.json

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

## Использование в коде

### Python (python-dotenv)

#### 1. Установка:
```bash
pip install python-dotenv
```

#### 2. Загрузка переменных:
```python
# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Загружаем .env из корня проекта
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Получение переменных
DATABASE_URL = os.getenv('DATABASE_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Валидация обязательных переменных
def validate_env():
    required_vars = [
        'DATABASE_URL',
        'SECRET_KEY',
        'OPENAI_API_KEY'
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            f"Please create .env file based on .env.example"
        )

# Вызываем при запуске приложения
validate_env()
```

#### 3. Использование в приложении:
```python
# app.py
from config import DATABASE_URL, OPENAI_API_KEY
import openai

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

# Подключение к БД
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)
```

### Node.js (dotenv)

#### 1. Установка:
```bash
npm install dotenv
```

#### 2. Использование:
```javascript
// config.js
require('dotenv').config();

module.exports = {
  database: {
    url: process.env.DATABASE_URL,
    host: process.env.DATABASE_HOST,
    port: parseInt(process.env.DATABASE_PORT) || 5432,
  },
  api: {
    openai: process.env.OPENAI_API_KEY,
    stripe: process.env.STRIPE_SECRET_KEY,
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    algorithm: process.env.JWT_ALGORITHM,
    expiration: parseInt(process.env.JWT_EXPIRATION),
  }
};

// app.js
const config = require('./config');
const OpenAI = require('openai');

const openai = new OpenAI({
  apiKey: config.api.openai
});
```

## Безопасность: Что НИКОГДА не коммитить

### ❌ ЗАПРЕЩЕНО в git:
- Пароли
- API ключи
- OAuth секреты
- JWT секреты
- Приватные ключи (.pem, .key)
- Токены доступа
- Database credentials
- Email пароли
- SSH ключи
- Локальные пути пользователей

### ✅ МОЖНО коммитить:
- `.env.example` (без реальных значений)
- Публичные конфигурации
- Дефолтные значения
- Структуру переменных

## Лучшие практики

### 1. Разные .env для разных окружений
```
.env              # Локальная разработка (не в git)
.env.development  # Development сервер (не в git)
.env.staging      # Staging (не в git)
.env.production   # Production (не в git)
.env.example      # Шаблон (В GIT!)
```

### 2. Валидация при старте
```python
# validate_env.py
import os
from typing import List

def require_env_vars(vars: List[str]) -> None:
    """Проверяет наличие обязательных переменных окружения."""
    missing = [v for v in vars if not os.getenv(v)]

    if missing:
        raise EnvironmentError(
            f"❌ Missing required environment variables:\n"
            f"   {', '.join(missing)}\n\n"
            f"Please:\n"
            f"1. Copy .env.example to .env\n"
            f"2. Fill in the required values\n"
            f"3. Restart the application"
        )

# В main.py или app.py
if __name__ == '__main__':
    require_env_vars([
        'DATABASE_URL',
        'SECRET_KEY',
        'OPENAI_API_KEY'
    ])
    # Запуск приложения
```

### 3. Type-safe конфигурация (Python)
```python
# config.py
from pydantic import BaseSettings, PostgresDsn, validator
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: PostgresDsn
    database_pool_size: int = 10

    # API Keys
    openai_api_key: str
    stripe_secret_key: Optional[str] = None

    # Security
    secret_key: str
    jwt_algorithm: str = "HS256"

    # Application
    debug: bool = False
    log_level: str = "INFO"

    @validator('openai_api_key')
    def validate_openai_key(cls, v):
        if not v.startswith('sk-'):
            raise ValueError('Invalid OpenAI API key format')
        return v

    class Config:
        env_file = '.env'
        case_sensitive = False

# Singleton
settings = Settings()
```

### 4. Документация в README.md
```markdown
## Настройка окружения

### 1. Скопируйте файл с примером:
\`\`\`bash
cp .env.example .env
\`\`\`

### 2. Заполните необходимые значения:

- **DATABASE_URL**: URL подключения к PostgreSQL
- **OPENAI_API_KEY**: Получите на https://platform.openai.com/api-keys
- **SECRET_KEY**: Сгенерируйте: `openssl rand -base64 32`

### 3. Запустите приложение:
\`\`\`bash
python main.py
\`\`\`
```

## Генерация секретов

### Для SECRET_KEY (Python/Django):
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Для JWT_SECRET:
```bash
openssl rand -base64 32
```

### Для случайного пароля:
```bash
openssl rand -base64 24
```

## Проверка безопасности

### Поиск секретов в истории git:
```bash
# Проверка, что .env не в истории
git log --all --full-history -- .env

# Поиск потенциальных секретов
git log -p | grep -i "password\|secret\|api.key"
```

### Удаление .env из истории (если случайно закоммитили):
```bash
# ОСТОРОЖНО! Перезаписывает историю
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# После этого форс-пуш
git push origin --force --all
git push origin --force --tags
```

## Интеграция с CI/CD

### GitHub Actions
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Create .env from secrets
        run: |
          echo "DATABASE_URL=${{ secrets.DATABASE_URL }}" >> .env
          echo "OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}" >> .env
          echo "SECRET_KEY=${{ secrets.SECRET_KEY }}" >> .env

      - name: Run tests
        run: pytest
```

## Контрольный список

При настройке переменных окружения проверьте:

- [ ] Создан файл `.env`
- [ ] `.env` добавлен в `.gitignore`
- [ ] Создан `.env.example` с описаниями
- [ ] Все секреты только в `.env` (не в коде!)
- [ ] Добавлена валидация обязательных переменных
- [ ] Обновлён README с инструкциями
- [ ] `.env` не в git истории
- [ ] CI/CD настроен с secrets

## Частые ошибки

### ❌ Плохо: Секрет в коде
```python
OPENAI_API_KEY = "sk-proj-abc123..."  # НИКОГДА!
```

### ✅ Хорошо: Секрет в .env
```python
# config.py
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# .env
OPENAI_API_KEY=sk-proj-abc123...
```

### ❌ Плохо: .env в git
```bash
git add .env  # ЗАПРЕЩЕНО!
```

### ✅ Хорошо: .env.example в git
```bash
git add .env.example  # ✅ Это OK
```

## Дополнительные инструменты

- **python-dotenv**: https://github.com/theskumar/python-dotenv
- **pydantic**: Type-safe settings
- **git-secrets**: Предотвращает коммит секретов
- **truffleHog**: Поиск секретов в репозитории

---

*Агент обеспечивает безопасность конфиденциальных данных в методологии Codev*
