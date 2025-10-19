# TDD Agent: Test (Red Phase)

## Назначение

Специализированный агент для фазы **Test** (Red) в цикле Test-Driven Development (TDD). Этот агент помогает написать failing тесты, которые определяют желаемое поведение функции до её реализации.

## Когда использовать

Вызывайте этого агента когда:
- Начинаете разработку новой функции или метода
- Добавляете новое поведение к существующему коду
- Исправляете баг и хотите сначала написать failing тест
- Нужно определить API или интерфейс новой функциональности

**Команда для вызова**:
```
"Напиши failing тест для [описание функциональности]"
или
"TDD Test: [описание того, что должна делать функция]"
```

## Что делает агент

### 1. Анализ требований
- Уточняет, что именно должна делать функция
- Определяет входные данные и ожидаемый результат
- Выявляет граничные случаи и возможные ошибки
- Определяет зависимости и моки

### 2. Создание тестов (Red Phase)
- Пишет failing тест, описывающий желаемое поведение
- Использует чёткие, описательные имена тестов
- Тест должен ПАДАТЬ, так как функция ещё не реализована
- Включает:
  - **Arrange**: Подготовка данных и окружения
  - **Act**: Вызов тестируемой функции
  - **Assert**: Проверка ожидаемого результата

### 3. Проверка тестов
- Запускает тест и подтверждает, что он падает
- Проверяет, что тест падает по правильной причине
- Убеждается, что сообщение об ошибке понятно

### 4. Документация тестов
- Добавляет docstring/комментарии к тестам
- Объясняет, что тестируется и почему
- Документирует граничные случаи

## Принципы написания тестов

### Хорошие тесты должны быть:

1. **Isolated** (Изолированными)
   - Не зависят от других тестов
   - Можно запускать в любом порядке
   - Используют моки для внешних зависимостей

2. **Descriptive** (Описательными)
   - Имя теста чётко говорит, что проверяется
   - Формат: `test_[что делает]_[при каких условиях]_[ожидаемый результат]`
   - Пример: `test_calculate_total_with_discount_returns_reduced_price`

3. **Fast** (Быстрыми)
   - Выполняются за миллисекунды
   - Не делают реальных HTTP-запросов
   - Не обращаются к реальной БД без необходимости

4. **Comprehensive** (Всесторонними)
   - Покрывают happy path (нормальный сценарий)
   - Проверяют граничные случаи (edge cases)
   - Тестируют обработку ошибок

## Пример работы агента

### Запрос пользователя:
```
"TDD Test: Функция для валидации email адреса"
```

### Действия агента:

1. **Уточняющие вопросы**:
   - Какие email считаются валидными? (RFC 5322 standard?)
   - Нужно ли проверять существование домена?
   - Какие специальные случаи обрабатывать? (unicode, плюсы в адресе)

2. **Написание тестов**:
```python
import pytest
from email_validator import validate_email, EmailValidationError

class TestEmailValidation:
    """
    Тесты для функции validate_email.

    Функция должна проверять, что email адрес соответствует
    базовым требованиям: наличие @, валидный домен, допустимые символы.
    """

    def test_validate_email_with_valid_simple_email_returns_true(self):
        """Проверяет, что простой валидный email принимается."""
        # Arrange
        email = "user@example.com"

        # Act
        result = validate_email(email)

        # Assert
        assert result == True

    def test_validate_email_with_missing_at_symbol_returns_false(self):
        """Проверяет, что email без @ отклоняется."""
        # Arrange
        email = "userexample.com"

        # Act
        result = validate_email(email)

        # Assert
        assert result == False

    def test_validate_email_with_missing_domain_returns_false(self):
        """Проверяет, что email без домена отклоняется."""
        # Arrange
        email = "user@"

        # Act
        result = validate_email(email)

        # Assert
        assert result == False

    def test_validate_email_with_unicode_characters_returns_true(self):
        """Проверяет поддержку unicode в email (интернационализация)."""
        # Arrange
        email = "пользователь@example.com"

        # Act
        result = validate_email(email)

        # Assert
        assert result == True

    def test_validate_email_with_plus_in_local_part_returns_true(self):
        """Проверяет, что плюс в локальной части email разрешён."""
        # Arrange
        email = "user+tag@example.com"

        # Act
        result = validate_email(email)

        # Assert
        assert result == True
```

3. **Запуск тестов**:
```bash
pytest tests/test_email_validator.py -v
```

4. **Ожидаемый результат**:
```
FAILED tests/test_email_validator.py::TestEmailValidation::test_validate_email_with_valid_simple_email_returns_true
ImportError: cannot import name 'validate_email' from 'email_validator'
```

5. **Передача управления**:
Агент завершает работу и сообщает:
```
✅ Написано 5 failing тестов для validate_email
❌ Все тесты падают, как и ожидалось (функция не реализована)
📝 Тесты покрывают:
   - Валидный email
   - Отсутствие символа @
   - Отсутствие домена
   - Unicode символы
   - Специальные символы (+)

Следующий шаг: Используй агента 'tdd-code' для реализации функции.
```

## Антипаттерны (чего НЕ делать)

### ❌ Плохо:
```python
def test_email():  # Неясное имя
    assert validate_email("test@test.com")  # Нет arrange/act/assert
```

### ✅ Хорошо:
```python
def test_validate_email_with_valid_format_returns_true():
    # Arrange
    email = "test@test.com"

    # Act
    result = validate_email(email)

    # Assert
    assert result == True
```

## Взаимодействие с другими TDD агентами

1. **tdd-test (этот агент)** → Пишет failing тесты
2. **tdd-code** → Реализует минимальный код для прохождения тестов
3. **tdd-refactor** → Улучшает код, сохраняя зелёные тесты

## Контрольный список

Перед передачей управления агенту tdd-code, убедитесь:

- [ ] Написаны failing тесты для основной функциональности
- [ ] Покрыты граничные случаи
- [ ] Добавлены тесты для обработки ошибок
- [ ] Все тесты имеют описательные имена
- [ ] Тесты запущены и подтверждено, что они падают
- [ ] Сообщения об ошибках понятны
- [ ] Добавлена документация к тестам

## Дополнительные ресурсы

- **Arrange-Act-Assert pattern**: http://wiki.c2.com/?ArrangeActAssert
- **Test naming conventions**: https://osherove.com/blog/2005/4/3/naming-standards-for-unit-tests.html
- **TDD Best Practices**: https://martinfowler.com/bliki/TestDrivenDevelopment.html

---

*Агент является частью TDD workflow в методологии Codev*
