# BDD Agent: Feature Files

## Назначение

Специализированный агент для создания и поддержки **feature файлов** в Behavior-Driven Development (BDD). Использует Gherkin синтаксис (Given-When-Then) для описания поведения системы на языке бизнеса.

## Когда использовать

Вызывайте этого агента когда:
- Нужно описать поведение функции с точки зрения пользователя
- Требуется живая документация системы
- Бизнес-аналитики должны понимать тесты
- Создаёте приёмочные тесты (acceptance tests)
- Работаете с cucumber/behave/pytest-bdd

**Команда для вызова**:
```
"Создай feature файл для [функциональность]"
или
"BDD: Опиши [пользовательский сценарий] на Gherkin"
```

## Где размещать feature файлы в Python проектах

### Рекомендуемая структура проекта:

```
project-root/
├── src/
│   └── myapp/
│       ├── __init__.py
│       └── validators.py
├── tests/
│   ├── unit/              # Юнит-тесты (pytest)
│   ├── integration/       # Интеграционные тесты
│   └── features/          # 🎯 BDD Feature файлы
│       ├── email_validation.feature
│       ├── user_registration.feature
│       └── steps/         # Step definitions
│           ├── __init__.py
│           ├── email_steps.py
│           └── user_steps.py
├── codev/
│   ├── specs/
│   │   └── 0001-email-validator.md     # Техническая спецификация
│   └── plans/
│       └── 0001-email-validator.md     # План реализации
└── pytest.ini            # Конфигурация pytest-bdd
```

### Альтернативная структура (рядом с функцией):

```
src/
├── myapp/
│   ├── features/          # Feature файлы рядом с кодом
│   │   └── validators.feature
│   ├── validators.py
│   └── __init__.py
tests/
└── bdd/
    └── steps/
        └── validator_steps.py
```

## Интеграция с Codev

Feature файлы **дополняют**, но **не заменяют** спецификации Codev:

| Документ | Назначение | Аудитория |
|----------|-----------|-----------|
| **Codev Spec** (`codev/specs/*.md`) | Техническая спецификация с архитектурой, решениями, рисками | Разработчики, архитекторы |
| **Feature файлы** (`tests/features/*.feature`) | Поведение системы с точки зрения пользователя | Бизнес, QA, разработчики |
| **Unit тесты** (`tests/unit/*.py`) | Тестирование отдельных функций | Разработчики |

### Workflow с Codev:

1. **Spec Phase**: Создаётся техническая спецификация в `codev/specs/`
2. **Plan Phase**: План реализации в `codev/plans/`
3. **Feature файлы**: Агент создаёт `.feature` файлы в `tests/features/`
4. **Step Definitions**: Реализация шагов в `tests/features/steps/`
5. **Implement**: TDD цикл (Red-Green-Refactor)

## Что делает агент

### 1. Создание Feature файлов
- Переводит требования в Gherkin синтаксис
- Использует Given-When-Then структуру
- Создаёт множество сценариев (Scenario Outline)
- Добавляет tags для организации тестов

### 2. Генерация Step Definitions
- Создаёт Python функции для каждого шага
- Использует pytest-bdd декораторы
- Интегрируется с существующим кодом

### 3. Поддержка живой документации
- Feature файлы служат документацией
- Автоматическая генерация отчётов
- Синхронизация с поведением системы

## Пример работы агента

### Запрос пользователя:
```
"Создай feature файл для валидации email адресов"
```

### Создаваемые файлы:

#### 1. Feature файл: `tests/features/email_validation.feature`

```gherkin
# language: ru
Функция: Валидация email адресов
  Как пользователь системы
  Я хочу, чтобы система проверяла корректность email адресов
  Чтобы избежать ошибок при регистрации и коммуникации

  Контекст:
    Допустим у нас есть система валидации email

  @positive @smoke
  Сценарий: Валидация корректного email адреса
    Дано email адрес "user@example.com"
    Когда я проверяю валидность email
    Тогда результат должен быть "валидный"

  @negative
  Сценарий: Отклонение email без символа @
    Дано email адрес "userexample.com"
    Когда я проверяю валидность email
    Тогда результат должен быть "невалидный"
    И сообщение об ошибке должно содержать "отсутствует @"

  @negative
  Сценарий: Отклонение email без домена
    Дано email адрес "user@"
    Когда я проверяю валидность email
    Тогда результат должен быть "невалидный"

  @parametrized
  Структура сценария: Проверка различных форматов email
    Дано email адрес "<email>"
    Когда я проверяю валидность email
    Тогда результат должен быть "<результат>"

    Примеры:
      | email                  | результат   |
      | simple@example.com     | валидный    |
      | user.name@example.com  | валидный    |
      | user+tag@example.com   | валидный    |
      | пользователь@пример.рф | валидный    |
      | @example.com           | невалидный  |
      | user@                  | невалидный  |
      | userexample.com        | невалидный  |
      | user@@example.com      | невалидный  |

  @edge-cases
  Сценарий: Обработка специальных символов
    Дано следующие email адреса:
      | email                    |
      | test.email@test.com      |
      | test+filter@example.com  |
      | test_underscore@test.com |
    Когда я проверяю валидность каждого email
    Тогда все должны быть "валидные"
```

#### 2. Step Definitions: `tests/features/steps/email_steps.py`

```python
"""
Step definitions для валидации email адресов.

Этот модуль содержит реализацию шагов из email_validation.feature
для использования с pytest-bdd.
"""

from pytest_bdd import scenarios, given, when, then, parsers
from typing import Dict, Any
import pytest

# Загружаем все сценарии из feature файла
scenarios('../email_validation.feature')


# ==================== GIVEN ====================

@given('у нас есть система валидации email')
def email_validation_system():
    """Инициализация системы валидации."""
    # Можно настроить систему, если нужно
    pass


@given(parsers.parse('email адрес "{email}"'))
@given(parsers.parse('email адрес "{email:String}"'), target_fixture="test_email")
def test_email(email: str) -> str:
    """
    Сохраняет email для тестирования.

    Args:
        email: Email адрес для проверки

    Returns:
        Email адрес
    """
    return email


@given('следующие email адреса:', target_fixture="email_list")
def email_list(datatable):
    """
    Создаёт список email адресов из таблицы.

    Args:
        datatable: Таблица с email адресами

    Returns:
        Список email адресов
    """
    return [row['email'] for row in datatable]


# ==================== WHEN ====================

@when('я проверяю валидность email', target_fixture="validation_result")
def validate_email_address(test_email: str) -> Dict[str, Any]:
    """
    Выполняет валидацию email адреса.

    Args:
        test_email: Email адрес для проверки

    Returns:
        Результат валидации с деталями
    """
    from myapp.validators import validate_email, get_validation_error

    is_valid = validate_email(test_email)
    error_message = get_validation_error(test_email) if not is_valid else None

    return {
        'is_valid': is_valid,
        'email': test_email,
        'error_message': error_message
    }


@when('я проверяю валидность каждого email', target_fixture="validation_results")
def validate_all_emails(email_list: list) -> list:
    """
    Валидирует список email адресов.

    Args:
        email_list: Список email адресов

    Returns:
        Список результатов валидации
    """
    from myapp.validators import validate_email

    return [
        {'email': email, 'is_valid': validate_email(email)}
        for email in email_list
    ]


# ==================== THEN ====================

@then(parsers.parse('результат должен быть "{expected_result}"'))
def check_validation_result(validation_result: Dict[str, Any], expected_result: str):
    """
    Проверяет результат валидации.

    Args:
        validation_result: Результат валидации
        expected_result: Ожидаемый результат ("валидный" или "невалидный")
    """
    is_valid = validation_result['is_valid']

    if expected_result == "валидный":
        assert is_valid, f"Email '{validation_result['email']}' должен быть валидным"
    elif expected_result == "невалидный":
        assert not is_valid, f"Email '{validation_result['email']}' должен быть невалидным"
    else:
        raise ValueError(f"Неизвестный результат: {expected_result}")


@then(parsers.parse('сообщение об ошибке должно содержать "{text}"'))
def check_error_message(validation_result: Dict[str, Any], text: str):
    """
    Проверяет содержимое сообщения об ошибке.

    Args:
        validation_result: Результат валидации
        text: Ожидаемый текст в сообщении
    """
    error_message = validation_result.get('error_message', '')
    assert text in error_message, \
        f"Ожидалось '{text}' в сообщении об ошибке, получено: '{error_message}'"


@then(parsers.parse('все должны быть "{expected}"'))
def check_all_valid(validation_results: list, expected: str):
    """
    Проверяет, что все результаты соответствуют ожиданию.

    Args:
        validation_results: Список результатов валидации
        expected: Ожидаемое состояние
    """
    expected_valid = (expected == "валидные")

    for result in validation_results:
        assert result['is_valid'] == expected_valid, \
            f"Email '{result['email']}' не соответствует ожиданию"
```

#### 3. Конфигурация pytest: `pytest.ini`

```ini
[pytest]
# Поддержка pytest-bdd
bdd_features_base_dir = tests/features

# Маркеры для организации тестов
markers =
    bdd: BDD тесты с feature файлами
    smoke: Быстрые smoke тесты
    positive: Позитивные тест-кейсы
    negative: Негативные тест-кейсы
    edge_cases: Граничные случаи
    parametrized: Параметризованные тесты

# Опции запуска
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=src
    --cov-report=term-missing
    --cov-report=html

# Паттерны для обнаружения тестов
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
```

## Запуск BDD тестов

### Все BDD тесты:
```bash
pytest tests/features/ --verbose
```

### Только smoke тесты:
```bash
pytest tests/features/ -m smoke
```

### С отчётом в формате Gherkin:
```bash
pytest tests/features/ --gherkin-terminal-reporter
```

### Генерация HTML отчёта:
```bash
pytest tests/features/ --html=reports/bdd_report.html --self-contained-html
```

## Установка зависимостей

### Для Python проектов:

```bash
pip install pytest-bdd pytest-cov pytest-html
```

### requirements.txt:
```
pytest>=7.0.0
pytest-bdd>=6.0.0
pytest-cov>=4.0.0
pytest-html>=3.1.0
```

## Преимущества feature файлов

### 1. Живая документация
- Feature файлы = документация = тесты
- Всегда актуально
- Понятно бизнесу

### 2. Язык предметной области
- Используйте термины вашего бизнеса
- Нет технических деталей
- Фокус на поведении

### 3. Переиспользование шагов
```gherkin
# Один шаг используется в разных сценариях
Дано пользователь авторизован
Когда пользователь нажимает "Выход"
Тогда пользователь видит страницу входа
```

### 4. Параметризация
```gherkin
Структура сценария: Вход с разными учётными данными
  Дано пользователь "<пользователь>"
  Когда вводит пароль "<пароль>"
  Тогда результат "<результат>"

  Примеры:
    | пользователь | пароль  | результат |
    | admin        | admin123| успех     |
    | user         | wrong   | ошибка    |
```

## Лучшие практики

### 1. Используйте русский язык
```gherkin
# language: ru
# Gherkin поддерживает русский!
```

### 2. Декларативный стиль (не императивный)
```gherkin
# ❌ Плохо (императивный - как делать)
Дано я открываю браузер
И ввожу URL "example.com"
И нажимаю кнопку "Войти"
И ввожу email "user@test.com"

# ✅ Хорошо (декларативный - что происходит)
Дано пользователь на странице входа
Когда пользователь вводит валидные учётные данные
```

### 3. Один сценарий = одна концепция
```gherkin
# ❌ Плохо (тестирует несколько вещей)
Сценарий: Создание и удаление пользователя
  Когда я создаю пользователя
  И удаляю пользователя
  Тогда пользователя нет в системе

# ✅ Хорошо (разделено на два сценария)
Сценарий: Создание пользователя
  Когда я создаю пользователя
  Тогда пользователь существует в системе

Сценарий: Удаление пользователя
  Дано существующий пользователь
  Когда я удаляю пользователя
  Тогда пользователя нет в системе
```

### 4. Используйте Background для общих шагов
```gherkin
Функция: Управление корзиной

  Контекст:
    Дано пользователь авторизован
    И в корзине 0 товаров

  Сценарий: Добавление товара
    ...

  Сценарий: Удаление товара
    ...
```

## Интеграция с CI/CD

### GitHub Actions example:
```yaml
name: BDD Tests

on: [push, pull_request]

jobs:
  bdd-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run BDD tests
        run: |
          pytest tests/features/ -v --html=reports/bdd.html
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: bdd-report
          path: reports/bdd.html
```

## Дополнительные ресурсы

- **pytest-bdd documentation**: https://pytest-bdd.readthedocs.io/
- **Gherkin reference**: https://cucumber.io/docs/gherkin/reference/
- **Behave** (альтернатива): https://behave.readthedocs.io/
- **BDD Best Practices**: https://cucumber.io/blog/bdd/bdd-best-practices/

---

*Агент является частью BDD workflow в методологии Codev*
