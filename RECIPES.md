# Удачные рецепты и практики разработки

## 📋 Оглавление

1. [Контрольный чек-лист перед коммитом](#контрольный-чек-лист-перед-коммитом)
2. [Порядок работы с проектом](#порядок-работы-с-проектом)
3. [Принципы качества кода](#принципы-качества-кода)
4. [Контрактное программирование](#контрактное-программирование)
5. [Рекомендации по оптимизации](#рекомендации-по-оптимизации)
6. [Conventional Commits на русском](#conventional-commits-на-русском)
7. [Установка Zen MCP для мультиагентной консультации](#установка-zen-mcp-для-мультиагентной-консультации)

---

## ✅ Контрольный чек-лист перед коммитом

Используйте этот чек-лист **перед каждым коммитом** для обеспечения качества кода:

- [ ] Все переменные имеют говорящие имена
- [ ] Функции < 50 строк (идеально < 20)
- [ ] Docstrings для всех публичных функций/классов
- [ ] Type hints везде где возможно
- [ ] Нет дублирования кода (DRY)
- [ ] Нет хардкода паролей/токенов
- [ ] Валидация входных данных
- [ ] Обработка ошибок везде где нужно

**Применение**: Добавьте этот чек-лист в ваш `CLAUDE.md` или создайте git pre-commit hook.

---

## 🔄 Порядок работы с проектом

### 7-шаговый workflow для любой задачи:

1. **Используй готовые модули**
   - Проверь существующие утилиты в `lib/` и корне проекта
   - При создании новых модулей соблюдай архитектурные принципы и типизацию

2. **Управляй зависимостями правильно**
   - Используй `uv` (или `pip-tools`, `poetry`) для управления зависимостями
   - **Не добавляй** внешние пакеты без `uv add` (или `pip install` + обновление requirements)

3. **Валидируй конфигурации перед применением**
   - Для Caddy: `caddy validate`
   - Для Docker Compose: `docker-compose config`
   - Для Kubernetes: `kubectl apply --dry-run=client`

4. **Покрывай код тестами**
   - Новый код → pytest-тесты (или unittest, vitest для JS)
   - Проверяй конфиги перед применением
   - Используй существующие мониторинговые утилиты

5. **Соблюдай требования безопасности**
   - Секреты ТОЛЬКО в `.env` (никогда в Git)
   - SSH доступ по ED25519 (не RSA)
   - Принцип наименьших привилегий

6. **Документируй изменения**
   - Обновляй `CLAUDE.md` при значительных изменениях
   - Запускай валидацию документации (если есть)
   - README должен быть актуален

7. **Коммить правильно**
   - Conventional Commits на русском: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`
   - После завершения: `git push` в origin/main

### Пример запроса к AI:

> «Разработай мониторинг использования диска в контейнерах и отправку оповещений в Telegram при превышении 85%»

**Ожидаемый результат:**
- Новый скрипт в корне проекта
- Интеграция с алертинг-системой
- systemd-таймер для периодического запуска
- pytest-тесты
- Обновление документации
- Коммит: `feat: добавлен мониторинг дискового пространства контейнеров`

---

## 🏆 Принципы качества кода

### 1. DRY (Don't Repeat Yourself)

**Правило**: Каждый фрагмент знания должен иметь **единственное, чёткое представление** в системе.

#### ❌ ПЛОХО: Дублирование конфигурации
```python
def send_telegram_host():
    bot_token = "TOKEN"
    chat_id = "ID"

def send_telegram_container():
    bot_token = "TOKEN"
    chat_id = "ID"
```

#### ✅ ХОРОШО: Единый источник конфигурации
```python
from config import TELEGRAM_CONFIG

def send_telegram(message):
    send_to_bot(
        TELEGRAM_CONFIG['token'],
        TELEGRAM_CONFIG['chat_id'],
        message
    )
```

**Практическое применение:**
- Конфигурация в одном месте (`.env`, `config.py`)
- Общие утилиты в `lib/` или `utils/`
- Документация синхронизирована с кодом

---

### 2. KISS (Keep It Simple, Stupid)

**Правило**: Простое решение всегда лучше сложного.

**Принципы:**
- Читаемый код без избыточных абстракций
- Минимум зависимостей
- Понятные имена переменных и функций

**Примеры:**
```python
# ❌ ПЛОХО: Излишняя сложность
class AbstractFactoryBuilderSingleton:
    def create_instance_with_dependency_injection(self):
        pass

# ✅ ХОРОШО: Прямолинейно и понятно
def create_user(name: str, email: str) -> User:
    return User(name=name, email=email)
```

---

### 3. SOLID

#### S - Single Responsibility
Одна функция = одна задача

```python
# ❌ ПЛОХО: функция делает слишком много
def process_user(user_data):
    validate(user_data)
    save_to_db(user_data)
    send_email(user_data)
    log_action(user_data)

# ✅ ХОРОШО: разделение ответственности
def validate_user(user_data): ...
def save_user(user_data): ...
def notify_user(user_data): ...
```

#### O - Open/Closed
Легко расширять без изменения существующего кода

```python
# ✅ ХОРОШО: расширяемая архитектура
class Notifier(ABC):
    @abstractmethod
    def send(self, message): pass

class EmailNotifier(Notifier):
    def send(self, message): ...

class TelegramNotifier(Notifier):
    def send(self, message): ...
```

#### L - Liskov Substitution
Наследники не ломают контракт родителя

#### I - Interface Segregation
Маленькие специфичные интерфейсы

#### D - Dependency Inversion
Зависимость от абстракций, не от конкретики

---

## 📝 Контрактное программирование (Design by Contract)

### Шаблон docstring с контрактом:

```python
def reset_password(username: str, min_length: int = 12) -> str:
    """
    Генерирует и устанавливает новый пароль для пользователя.

    Предусловия:
        - username существует в системе
        - min_length >= 8
        - Есть права sudo

    Постусловия:
        - Пароль изменён в системе
        - Возвращён сгенерированный пароль
        - Пароль соответствует требованиям безопасности

    Args:
        username: Имя пользователя в системе
        min_length: Минимальная длина пароля (по умолчанию 12)

    Returns:
        Сгенерированный пароль

    Raises:
        ValueError: если username не найден или min_length < 8
        PermissionError: если нет прав sudo

    Example:
        >>> new_pwd = reset_password("john", 16)
        >>> len(new_pwd) >= 16
        True
    """
    if min_length < 8:
        raise ValueError("min_length должен быть >= 8")

    if not user_exists(username):
        raise ValueError(f"Пользователь {username} не найден")

    # ... реализация
```

**Ключевые элементы:**
1. **Предусловия** (Preconditions): что должно быть выполнено ДО вызова
2. **Постусловия** (Postconditions): что гарантируется ПОСЛЕ выполнения
3. **Инварианты**: что всегда должно быть истинным
4. **Явные исключения**: какие ошибки могут быть выброшены

---

## ⚡ Рекомендации по оптимизации (научный подход)

### Правило: **Профилируй ДО оптимизации**

Результаты реальных оптимизаций из production проектов:

### 1. MySQL Оптимизация ✅
```ini
[mysqld]
# InnoDB
innodb_buffer_pool_size = 4G         # 50-80% доступной RAM
innodb_flush_log_at_trx_commit = 2   # Баланс скорость/надёжность
innodb_log_file_size = 512M
innodb_flush_method = O_DIRECT       # Избегаем двойного кеширования

# Connections
max_connections = 300
wait_timeout = 600
connect_timeout = 10

# Cache
table_open_cache = 4000
table_definition_cache = 2000

# Logging
slow_query_log = ON
long_query_time = 2
skip-log-bin                         # Если репликация не нужна
```

**Результат**: ↓15% RAM (835MB → 707MB), ↑2x connection capacity

---

### 2. Redis Caching ✅
```bash
# redis.conf
maxmemory 2GB
maxmemory-policy allkeys-lru
```

**Использование для OpenAI API:**
```python
import redis
r = redis.Redis(host='localhost', port=6379, db=2)

def get_openai_completion(prompt: str) -> str:
    cache_key = f"openai:{hashlib.sha256(prompt.encode()).hexdigest()}"

    # Проверка кеша
    if cached := r.get(cache_key):
        return cached.decode()

    # Запрос к API
    result = openai.ChatCompletion.create(...)

    # Сохранение в кеш (TTL = 1 час)
    r.setex(cache_key, 3600, result)
    return result
```

**Результат**: ↓80-95% API costs, ↓90% response time

---

### 3. Node.js Production Mode ✅
```bash
NODE_ENV=production
```

**Влияние:**
- Отключается подробное логирование
- Включается минификация
- Кеширование шаблонов
- ↓30-40% memory usage

---

### 4. Python Uvicorn Workers ✅
```bash
uvicorn app:app \
  --workers 2 \
  --limit-concurrency 100 \
  --timeout-keep-alive 5 \
  --backlog 2048
```

**Результат**: ↓12% avg response time (74ms → 65ms), ↑2x concurrent capacity

---

## 🔖 Conventional Commits на русском

### Формат:
```
<тип>: <краткое описание>

[необязательное подробное описание]

[необязательный footer]
```

### Типы коммитов:

| Тип | Описание | Пример |
|-----|----------|--------|
| `feat:` | Новая функция | `feat: добавлен мониторинг CPU` |
| `fix:` | Исправление бага | `fix: исправлена утечка памяти в парсере` |
| `docs:` | Документация | `docs: обновлён README с примерами` |
| `style:` | Форматирование (не влияет на логику) | `style: форматирование black` |
| `refactor:` | Рефакторинг | `refactor: извлечён класс DatabaseConnection` |
| `perf:` | Оптимизация производительности | `perf: добавлено кеширование запросов` |
| `test:` | Добавление тестов | `test: unit-тесты для auth модуля` |
| `chore:` | Обслуживание кода | `chore: обновление зависимостей` |
| `ci:` | CI/CD | `ci: добавлен GitHub Actions workflow` |

### Примеры качественных коммитов:

```bash
feat: добавлен мониторинг дискового пространства контейнеров

- Создан скрипт disk_monitor.py
- Интеграция с telegram_alerter
- Systemd таймер для запуска каждые 15 минут
- Pytest тесты для всех сценариев
- Документация в CLAUDE.md

Refs: #42
```

```bash
fix: исправлена race condition в cache invalidation

Проблема: при конкурентном доступе кеш мог быть повреждён.
Решение: добавлен Redis WATCH/MULTI для транзакций.

Тесты: test_cache_concurrent_access
```

```bash
perf: оптимизация MySQL запросов

- Добавлены индексы на users.email и orders.created_at
- Оптимизирован N+1 query в get_user_orders
- Результат: ↓70% время выполнения (850ms → 250ms)

Профилирование: django-debug-toolbar
```

---

## 📚 Применение рецептов в вашем проекте

### Быстрый старт (5 шагов):

1. **Добавьте чек-лист в CLAUDE.md**
   ```bash
   cat RECIPES.md >> CLAUDE.md
   ```

2. **Создайте pre-commit hook** (опционально)
   ```bash
   # .git/hooks/pre-commit
   #!/bin/bash
   echo "Проверяем код перед коммитом..."

   # Запуск линтеров
   black --check .
   mypy .

   # Запуск тестов
   pytest tests/ -v
   ```

3. **Настройте .env.example**
   ```bash
   cp .env .env.example
   # Замените все значения на placeholder'ы
   git add .env.example
   ```

4. **Добавьте conventional commits в CI**
   ```yaml
   # .github/workflows/lint-commits.yml
   - name: Check commit messages
     run: |
       pip install commitizen
       cz check --rev-range origin/main..HEAD
   ```

5. **Начните применять порядок работы**
   - При каждой задаче следуйте 7-шаговому workflow
   - Используйте контрактное программирование для критичных функций
   - Профилируйте ДО оптимизации

---

## 🎯 Метрики успеха

После применения этих практик вы должны увидеть:

- ✅ Код стал читаемее (код-ревью проходит быстрее)
- ✅ Меньше багов в production (DRY + контракты + тесты)
- ✅ Быстрее онбординг новых разработчиков (документация)
- ✅ Легче находить проблемы (логирование + мониторинг)
- ✅ Оптимизации основаны на данных (профилирование)

---

## 🤝 Установка Zen MCP для мультиагентной консультации

**Zen MCP** - это Model Context Protocol сервер, который позволяет Claude консультироваться с другими AI-моделями (Gemini 2.5 Pro, GPT-5, O3) для получения второго мнения.

### Зачем нужен Zen MCP?

**Проблема**: Один AI может пропустить баги, не увидеть оптимальных решений, или не заметить проблемы архитектуры.

**Решение**: Мультиагентная консультация - Claude автоматически запрашивает мнение других AI-экспертов:
- **Gemini 2.5 Pro**: Анализ больших кодовых баз (1M токенов контекста)
- **GPT-5 / O3**: Глубокое рассуждение и архитектурные решения
- **Claude**: Координация и интеграция всех мнений

### Практический пример

```
Claude:  "Предлагаю использовать Redis для кеширования"
   ↓ [консультация через Zen MCP]
Gemini:  "Согласен, но добавь TTL стратегию и cold start обработку"
GPT-5:   "Рассмотри также in-memory кеш для hot data"
   ↓
Claude:  [создаёт оптимальное решение учитывая оба мнения]
```

### Установка

#### Автоматическая установка (рекомендуется)

```bash
# Запустить скрипт установки
./scripts/install-zen-mcp.sh
```

Скрипт автоматически:
1. Проверит Python 3.10+ и Git
2. Склонирует Zen MCP в `~/.zen-mcp-server`
3. Создаст виртуальное окружение и установит зависимости
4. Создаст `.env` файл из шаблона
5. Настроит `~/.claude/mcp_config.json`

#### Ручная установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/BeehiveInnovations/zen-mcp-server.git ~/.zen-mcp-server
cd ~/.zen-mcp-server

# 2. Создать виртуальное окружение
python3 -m venv .zen_venv
source .zen_venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Настроить .env
cp .env.example .env
nano .env  # Добавить API-ключи

# 5. Настроить Claude MCP config
cat > ~/.claude/mcp_config.json << 'EOF'
{
  "mcpServers": {
    "zen": {
      "command": "bash",
      "args": [
        "${HOME}/.zen-mcp-server/run-server.sh"
      ],
      "env": {
        "PYTHONPATH": "${HOME}/.zen-mcp-server"
      }
    }
  }
}
EOF
```

### Настройка API-ключей

Отредактируйте `~/.zen-mcp-server/.env`:

```bash
# Обязательно хотя бы один
GEMINI_API_KEY=your_gemini_api_key_here    # https://makersuite.google.com/app/apikey
OPENAI_API_KEY=your_openai_api_key_here    # https://platform.openai.com/api-keys
XAI_API_KEY=your_xai_api_key_here          # https://console.x.ai/ (опционально)
```

### Проверка работы

```bash
# 1. Перезапустите Claude Code

# 2. Проверьте версию Zen MCP
mcp__zen__version

# 3. Используйте консультацию
"Consult Gemini Pro about this architecture"
"Ask GPT-5 to review this code"
"Get O3's opinion on this algorithm"
```

### Использование в протоколе SPIDER

После установки Zen MCP вы можете мигрировать с **SPIDER-SOLO** на полный **SPIDER** протокол с мультиагентной консультацией:

```markdown
## Фаза: Specification

1. Написать черновик спецификации
2. **Консультация с Gemini Pro и GPT-5** ← теперь доступно!
3. Обновить спецификацию на основе консультации
4. Представить пользователю для утверждения
```

### Сравнение SPIDER vs SPIDER-SOLO

| Характеристика | SPIDER (с Zen MCP) | SPIDER-SOLO |
|---|---|---|
| Консультации | ✅ GPT-5 + Gemini Pro | ❌ Самопроверка |
| Качество | ✅✅✅ Консенсус экспертов | ✅✅ Хорошее |
| Скорость | ⚠️ Медленнее | ✅ Быстрее |
| Стоимость | 💰💰 API-вызовы | 💰 Дешевле |
| Зависимости | ⚠️ Требует Zen MCP | ✅ Автономный |

### Полезные команды

```bash
# Проверить статус Zen MCP
mcp list

# Перезапустить Zen MCP (если зависло)
killall -9 python3
# Перезапустить Claude Code

# Посмотреть логи
tail -f ~/.zen-mcp-server/logs/mcp_server.log

# Обновить Zen MCP
cd ~/.zen-mcp-server
git pull origin main
source .zen_venv/bin/activate
pip install -r requirements.txt
```

### Устранение проблем

#### Zen MCP не отвечает
```bash
# Проверить процесс
ps aux | grep zen-mcp

# Перезапустить
killall -9 python3
# Перезапустить Claude Code
```

#### API-ключи не работают
```bash
# Проверить .env
cat ~/.zen-mcp-server/.env | grep API_KEY

# Убедиться, что ключи не имеют лишних пробелов
sed -i 's/ *= */=/g' ~/.zen-mcp-server/.env
```

#### Python модуль не найден
```bash
# Переустановить зависимости
cd ~/.zen-mcp-server
source .zen_venv/bin/activate
pip install --force-reinstall -r requirements.txt
```

### Результаты использования

По отзывам пользователей (Reddit 800+ upvotes):
- Обнаружение SQL-инъекций, которые пропустил Claude
- Оптимизация алгоритмов (GPT-5 предложил на 40% быстрее)
- Архитектурные ревью (Gemini нашёл 3 проблемы масштабируемости)

---

## 📖 Дополнительные ресурсы

- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/) - источник многих практик
- [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) - Robert C. Martin
- [Conventional Commits](https://www.conventionalcommits.org/) - стандарт коммитов
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID) - принципы ООП
- [Zen MCP Server](https://github.com/BeehiveInnovations/zen-mcp-server) - мультиагентная консультация

