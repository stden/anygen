# Как использовать Codev для совершенствования ваших проектов

## 🎯 Цель этого руководства

Показать, как применить методологию Codev и лучшие практики из анализа production проектов к **ВАШИМ** проектам для повышения качества, скорости разработки и поддерживаемости кода.

---

## 📋 Быстрый старт: 3 шага к улучшению проекта

### Шаг 1: Минимальная настройка (30 минут)

**Цель**: Получить немедленную пользу от базовых практик.

#### 1.1 Создайте CLAUDE.md

```bash
cd ${PROJECT_ROOT}

# Скопируйте шаблон из каталога с Codev
cp /path/to/codev/CLAUDE.md CLAUDE.md

# Или создайте минимальный вариант
cat > CLAUDE.md << 'EOF'
# Название проекта

## Обзор проекта
[2-3 предложения о том, что делает проект]

## Архитектура
### Основные компоненты
- Backend: [технологии]
- Frontend: [технологии]
- База данных: [технологии]

## Структура проекта
```
project/
├── src/          # Исходный код
├── tests/        # Тесты
├── docs/         # Документация
└── .env.example  # Шаблон конфигурации
```

## 🚨 КРИТИЧЕСКИЕ ПРАВИЛА

### Git Safety Protocol
**НИКОГДА не используйте:**
```bash
git add -A        # ❌ ЗАПРЕЩЕНО
git add .         # ❌ ЗАПРЕЩЕНО
```

**ВСЕГДА используйте:**
```bash
git add конкретный-файл.py
git add src/module.py
```

### Секреты только в .env
- ❌ НИКОГДА: пароли, API ключи в коде
- ✅ ВСЕГДА: все секреты в .env
- ✅ ВСЕГДА: .env в .gitignore

## Команды разработки

### Установка
```bash
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
```

### Тестирование
```bash
pytest tests/
```

### Запуск
```bash
python main.py
```
EOF
```

**Результат**: AI теперь понимает контекст проекта с первого промпта.

#### 1.2 Защитите секреты

```bash
# Проверьте, что .env в .gitignore
grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore

# Создайте .env.example
cat > .env.example << 'EOF'
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API Keys
OPENAI_API_KEY=sk-your-key-here
API_SECRET=your-secret-here

# External Services
REDIS_URL=redis://localhost:6379
EOF

# Если у вас УЖЕ есть .env с секретами
cp .env .env.example
# Замените реальные значения на плейсхолдеры в .env.example
```

**Результат**: 0 утечек секретов в Git.

#### 1.3 Настройте базовый CI/CD

```bash
mkdir -p .github/workflows

cat > .github/workflows/test.yml << 'EOF'
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pytest
          pip install -e .

      - name: Run tests
        run: pytest tests/ -v
EOF
```

**Результат**: Автоматическая проверка при каждом push.

---

### Шаг 2: Добавьте специализированных агентов (1 час)

**Цель**: Ускорить разработку с помощью TDD/BDD агентов.

#### 2.1 Скопируйте агенты из codev

```bash
cd /path/to/your-project/

# Создайте директорию для агентов
mkdir -p .claude/agents

# Скопируйте TDD агенты
cp /path/to/codev/.claude/agents/tdd-test.md .claude/agents/
cp /path/to/codev/.claude/agents/tdd-code.md .claude/agents/
cp /path/to/codev/.claude/agents/tdd-refactor.md .claude/agents/

# Скопируйте BDD агент
cp /path/to/codev/.claude/agents/bdd-features.md .claude/agents/

# Скопируйте ENV manager
cp /path/to/codev/.claude/agents/env-manager.md .claude/agents/
```

#### 2.2 Используйте агенты в разработке

**TDD Workflow** (Red → Green → Refactor):

```bash
# Промпт 1: RED Phase - Напишите failing тесты
"TDD Test: Функция для валидации email адресов"

# AI создаст:
# tests/test_email_validator.py с failing тестами

# Промпт 2: GREEN Phase - Минимальная реализация
"TDD Code: Сделай тесты зелёными"

# AI создаст:
# src/email_validator.py с минимальным кодом

# Промпт 3: REFACTOR Phase - Улучшение
"TDD Refactor: Отрефактори код с сохранением тестов"

# AI улучшит код, не ломая тесты
```

**BDD Workflow** (для бизнес-требований):

```bash
# Промпт: Создать feature файл
"BDD: Создай feature файл для процесса регистрации пользователя"

# AI создаст:
# tests/features/user_registration.feature на Gherkin
```

**ENV Workflow** (для безопасности):

```bash
# Промпт: Настроить секреты
"ENV: Добавь DATABASE_URL, REDIS_URL и OPENAI_API_KEY в .env"

# AI:
# 1. Обновит .env (не закоммитит!)
# 2. Обновит .env.example
# 3. Проверит .gitignore
```

**Результат**: TDD по умолчанию, безопасное управление секретами.

---

### Шаг 3: Внедрите DRY утилиты (2-4 часа)

**Цель**: Устранить дублирование кода.

#### 3.1 Найдите дублирования

```bash
cd ${PROJECT_ROOT}

# SQL запросы
rg "SELECT.*FROM" --count-matches | head -10

# Форматирование
rg "round.*100" --count-matches | head -10

# API вызовы к Google Sheets (если используете)
rg "clear_sheet|update_values" --count-matches | head -10

# Хардкоды
rg "password|api_key|secret" --ignore-case src/
```

#### 3.2 Создайте утилитарные классы

**Пример 1: DataFormatter** (если много форматирования)

```bash
mkdir -p src/utils

cat > src/utils/data_formatter.py << 'EOF'
"""Утилиты для форматирования данных."""

from datetime import datetime
from typing import Optional

class DataFormatter:
    """Форматирование дат, процентов, периодов."""

    @staticmethod
    def format_percentage(
        numerator: float,
        denominator: float,
        precision: int = 2
    ) -> str:
        """Форматирует процент с защитой от деления на ноль."""
        if denominator == 0:
            return "0%"
        percentage = round(numerator / denominator * 100, precision)
        return f"{percentage}%"

    @staticmethod
    def format_date(date: datetime, format_str: str = "%Y-%m-%d") -> str:
        """Форматирует дату."""
        return date.strftime(format_str)

    @staticmethod
    def format_period(date: datetime, grouping: str = "month") -> str:
        """Форматирует период для группировки."""
        formats = {
            "day": "%Y-%m-%d",
            "week": "%Y-W%W",
            "month": "%Y-%m",
            "quarter": "%Y-Q%q",
            "year": "%Y"
        }
        return date.strftime(formats.get(grouping, "%Y-%m"))
EOF

# Напишите тесты
cat > tests/test_data_formatter.py << 'EOF'
from src.utils.data_formatter import DataFormatter

def test_format_percentage_normal():
    result = DataFormatter.format_percentage(15, 100)
    assert result == "15.0%"

def test_format_percentage_zero_denominator():
    result = DataFormatter.format_percentage(10, 0)
    assert result == "0%"
EOF
```

**Пример 2: SQL шаблоны** (если много SQL)

```python
# src/utils/sql_templates.py
class SQLTemplates:
    """SQL шаблоны для типовых операций."""

    @staticmethod
    def conditional_count(field: str, condition: str) -> str:
        """Генерирует SUM(CASE WHEN ...) для подсчёта."""
        return f"SUM(CASE WHEN {field} {condition} THEN 1 ELSE 0 END)"

    @staticmethod
    def select_with_pagination(
        table: str,
        where: str = "1=1",
        limit: int = 100,
        offset: int = 0
    ) -> str:
        """Генерирует SELECT с пагинацией."""
        return f"""
            SELECT * FROM {table}
            WHERE {where}
            LIMIT {limit} OFFSET {offset}
        """
```

#### 3.3 Мигрируйте на утилиты

```bash
# Промпт для AI:
"Замени все вхождения расчёта процентов на DataFormatter.format_percentage()
в файлах src/*.py"

# AI автоматически:
# 1. Найдёт все места
# 2. Заменит на вызов утилиты
# 3. Добавит import
```

**Результат**: Один источник правды, легкое обслуживание.

---

## 🚀 Продвинутое использование: Codev SPIDER

### Когда применять SPIDER:

- ✅ Новая сложная функция (> 300 строк кода)
- ✅ Изменение архитектуры
- ✅ Неясные требования (нужна спецификация)
- ✅ Работа в команде (нужна документация)

### Шаг 1: Подготовка структуры Codev

```bash
cd ${PROJECT_ROOT}

# Создайте структуру Codev
mkdir -p codev/{specs,plans,reviews,protocols,resources}

# Скопируйте протоколы
cp -r /path/to/codev/codev/protocols/* codev/protocols/

# Или только SPIDER-SOLO (если работаете один)
cp -r /path/to/codev/codev/protocols/spider-solo codev/protocols/
```

### Шаг 2: Работа по протоколу SPIDER-SOLO

**Фаза Specify** (Спецификация):

```bash
# Промпт:
"Создай спецификацию для функции отправки email уведомлений.
Используй протокол SPIDER-SOLO из codev/protocols/spider-solo/protocol.md"

# AI создаст:
# codev/specs/0001-email-notifications.md с:
# - Проблема
# - Варианты решения
# - Выбранное решение
# - Критерии успеха
# - Зависимости
```

**Фаза Plan** (План):

```bash
# Промпт:
"Создай план реализации для 0001-email-notifications"

# AI создаст:
# codev/plans/0001-email-notifications.md с:
# - Фазами реализации
# - Временными оценками
# - Метриками готовности
```

**Фаза Implement** (Реализация):

```bash
# Промпт:
"Реализуй фазу 1 из плана 0001-email-notifications"

# AI напишет код согласно плану
```

**Фаза Defend** (Защита тестами):

```bash
# Промпт:
"Напиши тесты для email notifications"

# AI создаст тесты
```

**Фаза Evaluate** (Оценка):

```bash
# Промпт:
"Проверь, выполнены ли критерии успеха из спецификации"

# AI проверит и сообщит
```

**Фаза Review** (Обзор):

```bash
# Промпт:
"Создай review document для 0001-email-notifications"

# AI создаст:
# codev/reviews/0001-email-notifications.md с:
# - Что сработало
# - Что не сработало
# - Извлечённые уроки
# - Улучшения для следующего раза
```

**Результат**: Полная трассируемость от идеи до кода.

---

## 📊 Практические примеры из реальных проектов

### Пример 1: Production проект (BDD тестирование)

**Проблема**: Частые регрессии при изменениях.

**Решение**:
```bash
# 1. Создали структуру BDD
mkdir -p tests/features tests/steps

# 2. Написали feature файлы
cat > tests/features/analytics.feature << 'EOF'
Feature: Analytics Reports
  As a data analyst
  I want to generate reports
  So that I can make informed decisions

  Scenario: Generate monthly report
    Given data for month "2025-10"
    When I generate analytics report
    Then report contains 15 rows
    And all percentages are valid
EOF

# 3. Реализовали steps
# tests/steps/analytics_steps.py

# 4. Запускали тесты
behave tests/features/
```

**Результат**: Сотни scenarios, 0 регрессий за длительный период.

### Пример 2: Production проект (DRY - устранение дублирований)

**Проблема**: 86 файлов с одинаковыми SQL запросами.

**Решение**:
```python
# До (дублировалось 86 раз):
query = """
    SELECT
        COUNT(*) as total,
        SUM(CASE WHEN duplicates > 0 THEN 1 ELSE 0 END) as with_duplicates
    FROM deals
    WHERE marketer = :marketer
"""

# После (1 класс):
# utils/sql_templates.py
class DealsQueryBuilder:
    @staticmethod
    def by_marketer(marketer: str):
        return """
            SELECT
                COUNT(*) as total,
                {duplicates_count}
            FROM deals
            WHERE marketer = :marketer
        """.format(
            duplicates_count=SQLTemplates.conditional_count(
                'duplicates', '> 0'
            )
        )

# Использование:
query = DealsQueryBuilder.by_marketer('john')
```

**Результат**: 99% устранение дублирований.

### Пример 3: Production проект (Профилирование)

**Проблема**: Медленная генерация отчётов (2.754s).

**Решение**:
```python
# 1. Добавили профилирование
import time

def profile_operation(name):
    start = time.time()
    yield
    print(f"⏱️ {name}: {(time.time() - start)*1000:.2f}ms")

# 2. Замерили узкие места
with profile_operation("SQL query"):
    result = db.execute(query)  # 5-15 секунд!

# 3. Добавили индексы
CREATE INDEX idx_deals_marketer_date
ON deals(marketer(100), date_create, stage_id(50));

# 4. Добавили Redis кеш
@cache_bitrix_async(ttl=3600)
async def get_users(self):
    ...
```

**Результат**: Значительное ускорение (3x-4x улучшение).

---

## 🎯 Чеклист применения к проекту

### Минимум (1-2 часа работы):

- [ ] Создать CLAUDE.md с обзором проекта
- [ ] Добавить Git Safety Protocol (запрет `git add -A`)
- [ ] Создать .env.example
- [ ] Добавить .env в .gitignore
- [ ] Настроить базовый GitHub Actions

### Рекомендуется (4-8 часов):

- [ ] Скопировать TDD/BDD/ENV агенты из codev
- [ ] Создать базовые тесты (smoke tests)
- [ ] Найти и устранить основные дублирования
- [ ] Добавить профилирование критичных операций
- [ ] Настроить mypy (type checking)

### Опционально (1-2 недели):

- [ ] Внедрить полную Codev структуру (specs/plans/reviews)
- [ ] Написать 50+ BDD scenarios
- [ ] Создать все DRY утилиты
- [ ] Настроить Redis кеширование
- [ ] Достичь 90%+ type coverage

---

## 💡 Частые вопросы

### Q: Нужно ли переписывать весь проект?

**A**: Нет! Применяйте практики **инкрементально**:
1. Начните с CLAUDE.md (30 минут)
2. Добавьте Git Safety (5 минут)
3. Новые функции пишите с TDD (естественный рост)
4. Рефакторите старый код постепенно

### Q: Какие практики самые важные?

**A**: Приоритет по ROI:
1. **CLAUDE.md** - немедленная польза
2. **Git Safety** - защита от утечек
3. **TDD агенты** - качество новых функций
4. **CI/CD** - автоматический контроль
5. **DRY утилиты** - долгосрочная выгода

### Q: Сколько времени займёт внедрение?

**A**: Зависит от уровня:
- **Минимум** (безопасность): 1-2 часа
- **Базовый** (+ TDD): 1-2 дня
- **Продвинутый** (+ DRY): 1-2 недели
- **Полный Codev**: 1-2 месяца

### Q: Что делать с legacy кодом?

**A**: Стратегия "Boy Scout Rule":
1. Новый код - по новым практикам
2. При изменении старого - рефакторить
3. Не трогать работающий код без необходимости

### Q: Как убедить команду?

**A**: Покажите результаты:
1. Начните с одного модуля
2. Замерьте метрики (скорость, ошибки)
3. Покажите разницу
4. Масштабируйте

---

## 🚀 Следующие шаги

### Для вашего текущего проекта:

```bash
# 1. Скопируйте codev-skeleton
cp -r /path/to/codev/codev-skeleton /path/to/your-project/codev

# 2. Скопируйте агенты
cp -r /path/to/codev/.claude /path/to/your-project/

# 3. Адаптируйте CLAUDE.md
cp /path/to/codev/CLAUDE.md /path/to/your-project/
# Отредактируйте под свой проект

# 4. Запустите первый TDD цикл
cd /path/to/your-project
# "TDD Test: Функция X"
# "TDD Code: Сделай тесты зелёными"
# "TDD Refactor: Улучши код"
```

### Для нового проекта:

```bash
# 1. Создайте проект из codev-skeleton
cp -r /path/to/codev/codev-skeleton /path/to/new-project
cd /path/to/new-project

# 2. Инициализируйте Git
git init
git add .
git commit -m "Initial commit with Codev structure"

# 3. Создайте первую спецификацию
# "Создай спецификацию для [ваша функция]"

# 4. Следуйте SPIDER-SOLO протоколу
```

---

## 📚 Полезные ресурсы

### Документация Codev:
- [README.md](../README.md) - Обзор методологии
- [INSTALL.md](../INSTALL.md) - Установка для новых проектов
- [codev/protocols/spider-solo/protocol.md](../codev/protocols/spider-solo/protocol.md) - Полный протокол

### Примеры из реальных проектов:
- **Production проект A** - Сотни BDD тестов, DRY утилиты, профилирование (значительное ускорение)
- **Production проект B** - SPIDER-SOLO протокол, Git Safety, CI/CD автоматизация
- **Production проект C** - Безопасность, защита секретов, 0 утечек

### Агенты:
- [.claude/agents/tdd-test.md](../.claude/agents/tdd-test.md)
- [.claude/agents/tdd-code.md](../.claude/agents/tdd-code.md)
- [.claude/agents/tdd-refactor.md](../.claude/agents/tdd-refactor.md)
- [.claude/agents/bdd-features.md](../.claude/agents/bdd-features.md)
- [.claude/agents/env-manager.md](../.claude/agents/env-manager.md)

---

## ✅ Резюме

**3 ключевых действия прямо сейчас**:

1. **Создайте CLAUDE.md** в вашем проекте (30 минут)
2. **Скопируйте TDD агенты** из codev (5 минут)
3. **Напишите первую функцию по TDD** (1 час)

**Результат через неделю**:
- ✅ AI понимает ваш проект
- ✅ 0 утечек секретов
- ✅ Новый код с тестами
- ✅ Автоматические проверки в CI/CD

**Результат через месяц**:
- ✅ 50+ тестов
- ✅ 90%+ устранение дублирований
- ✅ Документация актуальна
- ✅ Скорость разработки +50%

---

*Помните: Не пытайтесь внедрить всё сразу. Начните с малого, покажите результаты, масштабируйте.*

*Эта методология проверена на 44 production проектах. Она работает.*
