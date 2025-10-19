# TDD Agent: Refactor (Clean Phase)

## Назначение

Специализированный агент для фазы **Refactor** (Clean) в цикле Test-Driven Development (TDD). Этот агент улучшает код, устраняет дублирование и повышает читаемость, **сохраняя все тесты зелёными**.

## Когда использовать

Вызывайте этого агента когда:
- Все тесты проходят (green)
- Код работает, но выглядит неэлегантно
- Есть дублирование кода
- Можно улучшить читаемость
- Нужно применить паттерны проектирования

**Команда для вызова**:
```
"Отрефактори код в [файл], сохраняя тесты зелёными"
или
"TDD Refactor: Улучши код без изменения поведения"
```

## Что делает агент

### 1. Анализ кода
- Выявляет дублирование (DRY violations)
- Находит длинные функции/методы
- Определяет сложную логику
- Ищет магические числа и строки
- Проверяет naming conventions

### 2. Рефакторинг кода
- Устраняет дублирование (Extract Method, Extract Variable)
- Улучшает именование переменных и функций
- Разбивает длинные функции
- Применяет паттерны проектирования
- Добавляет документацию

### 3. Постоянная проверка тестов
- **КРИТИЧНО**: После каждого изменения запускает тесты
- Если тест падает - откатывает изменение
- Делает маленькие шаги (baby steps)
- Коммитит после каждого успешного рефакторинга

### 4. Улучшение качества
- Добавляет type hints (Python)
- Улучшает docstrings
- Устраняет code smells
- Применяет линтеры и форматтеры

## Принципы фазы Refactor

### 1. Green Bar всегда
- **Тесты должны оставаться зелёными ВСЕГДА**
- Если тест упал - откат изменения немедленно
- Refactor = изменение структуры без изменения поведения

### 2. Маленькие шаги
- Одно изменение за раз
- Тесты после каждого изменения
- Коммит после успешного рефакторинга

### 3. DRY (Don't Repeat Yourself)
- Устранение дублирования кода
- Извлечение общей логики
- Создание переиспользуемых компонентов

### 4. Clean Code
- Понятные имена
- Маленькие функции (< 20 строк)
- Одна ответственность на функцию
- Явное лучше неявного

## Пример работы агента

### Исходный код (после Green фазы):
```python
def validate_email(email: str) -> bool:
    """Валидирует email адрес."""
    if '@' not in email:
        return False
    parts = email.split('@')
    if len(parts) != 2:
        return False
    local_part, domain = parts
    if not local_part or not domain:
        return False
    return True

def validate_phone(phone: str) -> bool:
    """Валидирует телефон."""
    if not phone:
        return False
    if len(phone) < 10:
        return False
    return True
```

### Действия агента:

#### Шаг 1: Улучшение validate_email

```python
def validate_email(email: str) -> bool:
    """
    Валидирует email адрес.

    Args:
        email: Email адрес для проверки

    Returns:
        True если email валиден, False иначе

    Examples:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid.email")
        False
    """
    if '@' not in email:
        return False

    local_part, _, domain = email.partition('@')

    return bool(local_part and domain and email.count('@') == 1)
```

**Запуск тестов**: ✅ Все проходят

#### Шаг 2: Extract helper function

```python
def _has_required_parts(value: str, separator: str, expected_parts: int = 2) -> bool:
    """
    Проверяет, что строка содержит нужное количество частей после разделения.

    Args:
        value: Строка для проверки
        separator: Разделитель
        expected_parts: Ожидаемое количество частей

    Returns:
        True если строка содержит правильное количество частей
    """
    return value.count(separator) == expected_parts - 1


def validate_email(email: str) -> bool:
    """
    Валидирует email адрес.

    Проверяет базовые требования:
    - Наличие ровно одного символа @
    - Непустая локальная часть
    - Непустой домен

    Args:
        email: Email адрес для проверки

    Returns:
        True если email валиден, False иначе

    Examples:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid.email")
        False
        >>> validate_email("user@@example.com")
        False
    """
    if not _has_required_parts(email, '@', expected_parts=2):
        return False

    local_part, _, domain = email.partition('@')

    return bool(local_part and domain)
```

**Запуск тестов**: ✅ Все проходят

#### Шаг 3: Add type hints и константы

```python
from typing import Final

# Константы
MIN_PHONE_LENGTH: Final[int] = 10
EMAIL_SEPARATOR: Final[str] = '@'


def _has_required_parts(
    value: str,
    separator: str,
    expected_parts: int = 2
) -> bool:
    """Проверяет, что строка содержит нужное количество частей."""
    return value.count(separator) == expected_parts - 1


def validate_email(email: str) -> bool:
    """Валидирует email адрес согласно базовым требованиям."""
    if not _has_required_parts(email, EMAIL_SEPARATOR, expected_parts=2):
        return False

    local_part, _, domain = email.partition(EMAIL_SEPARATOR)

    return bool(local_part and domain)


def validate_phone(phone: str) -> bool:
    """
    Валидирует номер телефона.

    Args:
        phone: Номер телефона для проверки

    Returns:
        True если телефон валиден, False иначе

    Examples:
        >>> validate_phone("+1234567890")
        True
        >>> validate_phone("123")
        False
    """
    return bool(phone and len(phone) >= MIN_PHONE_LENGTH)
```

**Запуск тестов**: ✅ Все проходят

#### Результат:
```
✅ Рефакторинг завершён!
✅ Все тесты остаются зелёными

📝 Проведённые улучшения:
   1. Упрощена логика validate_email с partition()
   2. Извлечена helper функция _has_required_parts
   3. Добавлены type hints
   4. Добавлены константы для магических значений
   5. Улучшена документация с примерами
   6. Упрощена логика validate_phone

📊 Метрики:
   - Строк кода: 15 → 35 (но код читаемее)
   - Дублирование: уменьшено
   - Cyclomatic complexity: уменьшена
   - Документация: улучшена
```

## Типичные рефакторинги

### 1. Extract Method
**Было**:
```python
def process_order(order):
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    if order.coupon:
        total *= (1 - order.coupon.discount)
    return total
```

**Стало**:
```python
def process_order(order):
    total = _calculate_subtotal(order.items)
    return _apply_discount(total, order.coupon)

def _calculate_subtotal(items):
    return sum(item.price * item.quantity for item in items)

def _apply_discount(total, coupon):
    if not coupon:
        return total
    return total * (1 - coupon.discount)
```

### 2. Extract Variable
**Было**:
```python
if user.age >= 18 and user.has_license and not user.has_violations:
    allow_rental()
```

**Стало**:
```python
is_adult = user.age >= 18
has_valid_license = user.has_license and not user.has_violations

if is_adult and has_valid_license:
    allow_rental()
```

### 3. Replace Magic Number with Constant
**Было**:
```python
def calculate_fee(amount):
    return amount * 0.025
```

**Стало**:
```python
TRANSACTION_FEE_RATE: Final[float] = 0.025

def calculate_fee(amount: float) -> float:
    return amount * TRANSACTION_FEE_RATE
```

### 4. Simplify Conditional
**Было**:
```python
def is_valid(value):
    if value is not None:
        if len(value) > 0:
            if value != "":
                return True
    return False
```

**Стало**:
```python
def is_valid(value: str | None) -> bool:
    return bool(value and value.strip())
```

## Code Smells для устранения

### 1. Long Method (Длинный метод)
- Метод > 20 строк
- **Решение**: Extract Method

### 2. Duplicate Code (Дублирование)
- Один и тот же код в нескольких местах
- **Решение**: Extract Method/Class

### 3. Large Class (Большой класс)
- Класс делает слишком много
- **Решение**: Extract Class, Single Responsibility

### 4. Long Parameter List
- Больше 3-4 параметров
- **Решение**: Introduce Parameter Object

### 5. Dead Code
- Неиспользуемый код
- **Решение**: Удалить

## Антипаттерны (чего НЕ делать)

### ❌ Плохо: Изменение поведения
```python
# Было (работало)
def calculate_total(items):
    return sum(item.price for item in items)

# "Рефакторинг" (сломал логику!)
def calculate_total(items):
    return sum(item.price * item.quantity for item in items)
```
Это НЕ рефакторинг! Это изменение поведения. Тесты упадут.

### ❌ Плохо: Большие шаги без проверки тестов
```python
# Изменил 10 функций сразу
# Тесты упали - не понятно, где ошибка
```

### ✅ Хорошо: Маленькие шаги
```python
# Изменил 1 функцию
# Запустил тесты - зелёные
# Коммит
# Следующая функция
```

## Инструменты для рефакторинга

### Python
- **black**: Форматирование кода
- **pylint/flake8**: Статический анализ
- **mypy**: Проверка типов
- **radon**: Измерение сложности

### Запуск после рефакторинга:
```bash
black src/
mypy src/
pylint src/
pytest tests/ -v
```

## Взаимодействие с другими TDD агентами

1. **tdd-test** → Пишет failing тесты
2. **tdd-code** → Реализует минимальный код
3. **tdd-refactor (этот агент)** → Улучшает код

### Цикл повторяется для новой функции!

## Контрольный список

После рефакторинга убедитесь:

- [ ] ВСЕ тесты проходят (green)
- [ ] Код читается лучше
- [ ] Дублирование устранено
- [ ] Имена переменных/функций описательные
- [ ] Магические числа заменены константами
- [ ] Добавлена документация
- [ ] Применены type hints (если Python 3.10+)
- [ ] Проверен линтером (no warnings)
- [ ] Сложность функций снижена

## Когда остановиться?

Рефакторинг завершён когда:
1. ✅ Код читается как хорошая проза
2. ✅ Нет очевидного дублирования
3. ✅ Функции маленькие и фокусированные
4. ✅ Имена понятны без комментариев
5. ✅ Тесты зелёные

**Не перфекционизм!** Код может быть "достаточно хорошим". Можно вернуться к рефакторингу позже.

## Частые вопросы

**Q: Сколько времени тратить на рефакторинг?**
A: Правило: если рефакторинг занимает дольше, чем написание кода - остановитесь. Можно рефакторить постепенно.

**Q: Надо ли рефакторить чужой код?**
A: Только если вы его меняете. Следуйте "Boy Scout Rule": оставьте код чище, чем нашли.

**Q: Можно ли пропустить Refactor фазу?**
A: Технически да, но накапливается технический долг. Лучше рефакторить понемногу регулярно.

## Дополнительные ресурсы

- **Martin Fowler - Refactoring**: Каталог рефакторингов
- **Clean Code by Robert Martin**: Принципы чистого кода
- **Refactoring Guru**: https://refactoring.guru/

---

*Агент является частью TDD workflow в методологии Codev*
