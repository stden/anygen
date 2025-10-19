# TDD Agent: Code (Green Phase)

## Назначение

Специализированный агент для фазы **Code** (Green) в цикле Test-Driven Development (TDD). Этот агент реализует минимальный код, необходимый для прохождения failing тестов, написанных в Red фазе.

## Когда использовать

Вызывайте этого агента когда:
- Есть failing тесты из фазы Red
- Нужно реализовать функциональность для прохождения тестов
- Требуется минимальная, но рабочая реализация

**Команда для вызова**:
```
"Реализуй код для прохождения тестов в [файл]"
или
"TDD Code: Сделай тесты зелёными"
```

## Что делает агент

### 1. Анализ failing тестов
- Читает все failing тесты
- Понимает, какая функциональность требуется
- Определяет минимальный объём кода для прохождения
- Выявляет зависимости и необходимые импорты

### 2. Реализация минимального кода (Green Phase)
- Пишет **МИНИМАЛЬНЫЙ** код для прохождения тестов
- Не добавляет лишней функциональности
- Избегает преждевременной оптимизации
- Следует принципу YAGNI (You Aren't Gonna Need It)

### 3. Запуск тестов
- Запускает все тесты
- Проверяет, что ВСЕ тесты теперь проходят (green)
- Если есть failing тесты - дорабатывает код

### 4. Быстрая проверка качества
- Код компилируется без ошибок
- Нет очевидных багов
- Базовая обработка ошибок присутствует

## Принципы фазы Green

### 1. Make it work (Заставь работать)
- Главная цель - сделать тесты зелёными
- Простота важнее элегантности
- Дублирование кода допустимо (будет устранено в refactor)

### 2. Минимализм
- Не пишите код, который не требуют тесты
- Если тест не проверяет - не реализуйте
- "Simplest thing that could possibly work"

### 3. Следование тестам
- Тесты определяют API и поведение
- Не меняйте интерфейс функции без обновления тестов
- Если нужно изменить API - вернитесь к Red фазе

## Пример работы агента

### Исходные failing тесты (из Red фазы):
```python
class TestEmailValidation:
    def test_validate_email_with_valid_simple_email_returns_true(self):
        email = "user@example.com"
        result = validate_email(email)
        assert result == True

    def test_validate_email_with_missing_at_symbol_returns_false(self):
        email = "userexample.com"
        result = validate_email(email)
        assert result == False

    def test_validate_email_with_missing_domain_returns_false(self):
        email = "user@"
        result = validate_email(email)
        assert result == False
```

### Действия агента:

1. **Анализ тестов**:
   - Функция: `validate_email(email: str) -> bool`
   - Требования: проверка наличия @, проверка домена
   - Возврат: True/False

2. **Минимальная реализация**:
```python
def validate_email(email: str) -> bool:
    """
    Валидирует email адрес.

    Args:
        email: Строка с email адресом

    Returns:
        True если email валидный, False иначе
    """
    # Проверка наличия @
    if '@' not in email:
        return False

    # Разделяем на локальную часть и домен
    parts = email.split('@')

    # Проверка, что есть и локальная часть, и домен
    if len(parts) != 2:
        return False

    local_part, domain = parts

    # Проверка, что обе части не пустые
    if not local_part or not domain:
        return False

    return True
```

3. **Запуск тестов**:
```bash
pytest tests/test_email_validator.py -v
```

4. **Результат**:
```
tests/test_email_validator.py::TestEmailValidation::test_validate_email_with_valid_simple_email_returns_true PASSED
tests/test_email_validator.py::TestEmailValidation::test_validate_email_with_missing_at_symbol_returns_false PASSED
tests/test_email_validator.py::TestEmailValidation::test_validate_email_with_missing_domain_returns_false PASSED

======================== 3 passed in 0.01s ========================
```

5. **Передача управления**:
```
✅ Все тесты проходят!
✅ Реализована минимальная функция validate_email
📝 Код:
   - Проверяет наличие @
   - Проверяет наличие локальной части и домена
   - Возвращает True/False

⚠️  Примечание: Код простой и может иметь дублирование.
Следующий шаг: Используй агента 'tdd-refactor' для улучшения кода.
```

## Примеры минимальной реализации

### Пример 1: Слишком простая (fake it)

Иногда самая простая реализация - это захардкодить результат:

```python
def test_add_two_numbers_returns_sum():
    result = add(2, 3)
    assert result == 5

# Минимальная реализация:
def add(a, b):
    return 5  # Проходит тест!
```

Это валидно для TDD! Следующий тест заставит сделать правильную реализацию:

```python
def test_add_different_numbers_returns_correct_sum():
    result = add(4, 7)
    assert result == 11  # Теперь return 5 не работает

# Минимальная реализация:
def add(a, b):
    return a + b  # Теперь правильно
```

### Пример 2: Обработка ошибок

```python
def test_divide_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

# Минимальная реализация:
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
```

## Антипаттерны (чего НЕ делать)

### ❌ Плохо: Преждевременная оптимизация
```python
def validate_email(email: str) -> bool:
    # Полная RFC 5322 валидация с regex
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```
Это слишком сложно, если тесты не требуют такой детальной проверки!

### ❌ Плохо: Добавление нетестируемой функциональности
```python
def validate_email(email: str) -> bool:
    # Проверка DNS записи (тесты этого не требуют!)
    import dns.resolver
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except:
        return False
```

### ✅ Хорошо: Минимальная реализация
```python
def validate_email(email: str) -> bool:
    if '@' not in email:
        return False
    parts = email.split('@')
    return len(parts) == 2 and all(parts)
```

## Когда код "достаточно минимален"?

Код достаточно минимален, когда:
1. ✅ Все тесты проходят
2. ✅ Нет unused кода
3. ✅ Нет очевидных багов
4. ✅ Базовая обработка ошибок есть

Код НЕ обязан быть:
- ❌ Идеально оптимизированным
- ❌ DRY (без дублирования)
- ❌ Красиво отрефакторенным
- ❌ С полной документацией

Всё это будет в фазе Refactor!

## Взаимодействие с другими TDD агентами

1. **tdd-test** → Пишет failing тесты
2. **tdd-code (этот агент)** → Реализует минимальный код для прохождения
3. **tdd-refactor** → Улучшает код, сохраняя зелёные тесты

## Контрольный список

Перед передачей управления агенту tdd-refactor, убедитесь:

- [ ] ВСЕ тесты проходят (green)
- [ ] Нет failing или skipped тестов
- [ ] Код компилируется без ошибок
- [ ] Базовая обработка ошибок присутствует
- [ ] Нет очевидных багов
- [ ] Функция делает то, что требуют тесты (не больше, не меньше)

## Частые вопросы

**Q: Что если я вижу способ сделать код лучше?**
A: Заметьте, но не реализуйте сейчас. Запишите в TODO для фазы Refactor.

**Q: Код дублируется в нескольких местах. Надо исправить?**
A: Нет. Дублирование будет устранено в фазе Refactor.

**Q: Можно ли добавить дополнительную функциональность "на всякий случай"?**
A: Нет! Следуйте YAGNI. Если нужна функциональность - напишите тест для неё сначала.

**Q: Код выглядит некрасиво. Это нормально?**
A: Да. Красота - задача Refactor фазы. Сейчас важно сделать тесты зелёными.

## Дополнительные ресурсы

- **Kent Beck - TDD by Example**: Классическая книга по TDD
- **YAGNI Principle**: https://martinfowler.com/bliki/Yagni.html
- **Fake It Till You Make It**: https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html

---

*Агент является частью TDD workflow в методологии Codev*
