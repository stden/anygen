# Проект Codev

## Описание

**Codev** - фреймворк для context-driven разработки с расширенными возможностями для AI-driven разработки.

## Основная информация

- **Название**: Codev Framework
- **Базовый фреймворк**: Codev (ansari-project/codev)
- **Репозиторий**: Настраивается через переменные окружения ($PROJECT_GITHUB_USER/$PROJECT_GITHUB_REPO)
- **Язык**: Русский (100% документации)
- **Статус**: В активной разработке
- **Лицензия**: MIT

## Цели проекта

1. **Полная русификация** Codev для русскоязычных разработчиков
2. **Добавление специализированных агентов** для TDD, BDD, управления окружением
3. **Интеграция лучших практик** из реальных production проектов
4. **Безопасность по умолчанию** - все личные данные в `.env`

## Ключевые отличия от оригинального Codev

### 1. Полный перевод на русский

**Переведено:**
- README.md, INSTALL.md, CLAUDE.md
- Все протоколы: SPIDER, SPIDER-SOLO, TICK
- Все шаблоны (spec.md, plan.md, review.md)
- Документация агентов
- Примеры и тесты
- Практические руководства

**Статистика:**
- 20+ переведённых документов
- ~8000+ строк документации
- 0 английских инструкций в critical path

### 2. Специализированные AI-агенты

| Агент | Назначение | Файл |
|-------|-----------|------|
| **tdd-test.md** | TDD Red Phase - написание failing тестов | [.claude/agents/tdd-test.md](/.claude/agents/tdd-test.md) |
| **tdd-code.md** | TDD Green Phase - минимальная реализация | [.claude/agents/tdd-code.md](/.claude/agents/tdd-code.md) |
| **tdd-refactor.md** | TDD Refactor - улучшение кода | [.claude/agents/tdd-refactor.md](/.claude/agents/tdd-refactor.md) |
| **bdd-features.md** | BDD - feature файлы на Gherkin | [.claude/agents/bdd-features.md](/.claude/agents/bdd-features.md) |
| **env-manager.md** | Управление .env и секретами | [.claude/agents/env-manager.md](/.claude/agents/env-manager.md) |
| **spider-protocol-updater.md** | Обновление протокола SPIDER | [.claude/agents/spider-protocol-updater.md](/.claude/agents/spider-protocol-updater.md) |

### 3. Лучшие практики из production

**Источник**: Анализ 44 реальных проектов

**Добавлено:**
- Контрольный чек-лист перед каждым коммитом
- DRY, KISS, SOLID принципы с примерами
- Контрактное программирование (Design by Contract)
- Рекомендации по оптимизации (MySQL, Redis, Node.js)
- Conventional Commits на русском

**Файлы:**
- [RECIPES.md](/RECIPES.md) - Полный набор рецептов и лучших практик
- [CLAUDE.md](/CLAUDE.md#контрольный-чек-лист-перед-каждым-коммитом) - Встроенные практики

### 4. Безопасность

**Обязательные меры:**
- ✅ `.env` в `.gitignore` по умолчанию
- ✅ `.env.example` с шаблонами (без реальных данных)
- ✅ Запрет на `git add -A` (в инструкциях)
- ✅ Все личные данные (GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL) в `.env`
- ✅ Валидация перед коммитом

**Проверки:**
- Email и имена не попадают в Git history
- API ключи только в `.env`
- SSH ключи и сертификаты не в репозитории

### 5. CI/CD Infrastructure

**GitHub Actions:**
- Автоматический запуск 64 тестов при push/PR
- Установка bats-core и зависимостей
- Опциональные интеграционные тесты с Claude CLI
- Сохранение артефактов тестирования

**Тестовая инфраструктура:**
- 64 теста BATS (Bash Automated Testing System)
- Покрытие: фреймворк, протоколы, агенты, интеграция
- Документация: [tests/README.md](/tests/README.md)

## Структура проекта

```
project-root/
├── .claude/
│   └── agents/                 # AI-агенты
│       ├── tdd-test.md
│       ├── tdd-code.md
│       ├── tdd-refactor.md
│       ├── bdd-features.md
│       ├── env-manager.md
│       └── spider-protocol-updater.md
├── .github/
│   └── workflows/
│       └── codev-tests.yml     # CI/CD pipeline
├── codev/
│   ├── protocols/              # Протоколы разработки
│   │   ├── spider/
│   │   ├── spider-solo/
│   │   └── tick/
│   ├── specs/                  # Спецификации (WHAT)
│   ├── plans/                  # Планы (HOW)
│   ├── reviews/                # Ретроспективы
│   └── resources/              # Ресурсы проекта
│       └── project.md          # Этот файл
├── codev-skeleton/             # Скелет для новых проектов
├── docs/
│   └── HOW_TO_USE_CODEV.md    # Практическое руководство
├── examples/
│   └── todo-manager/           # Пример приложения
├── scripts/
│   ├── run-tests.sh
│   └── run-integration-tests.sh
├── tests/                      # 64 BATS теста
├── .env.example                # Шаблон переменных окружения
├── .gitignore                  # Защита секретов
├── CLAUDE.md                   # Инструкции для AI
├── INSTALL.md                  # Руководство по установке
├── README.md                   # Основная документация
├── README-translations.md      # Статус перевода
└── RECIPES.md                  # Лучшие практики
```

## Использование

### Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone git@github.com:$PROJECT_GITHUB_USER/$PROJECT_GITHUB_REPO.git
cd $PROJECT_GITHUB_REPO

# 2. Настроить .env
cp .env.example .env
# Отредактировать .env, добавить свои данные

# 3. Запустить тесты
./scripts/run-tests.sh

# 4. Начать работу с AI
# Открыть проект в Claude Code или другом AI IDE
```

### Workflow разработки

1. **Выбрать протокол** (SPIDER, SPIDER-SOLO, TICK) в зависимости от размера задачи
2. **Создать спецификацию** в `codev/specs/`
3. **Следовать протоколу**: Specify → Plan → Implement → Defend → Evaluate → Review
4. **Использовать агентов** для TDD/BDD/ENV задач
5. **Документировать** изменения в `codev/reviews/`

### Применение к своим проектам

См. подробное руководство: [docs/HOW_TO_USE_CODEV.md](/docs/HOW_TO_USE_CODEV.md)

**Три шага:**
1. **Минимальная настройка** (30 минут): CLAUDE.md, .env, CI/CD
2. **Добавление агентов** (1 час): TDD/BDD/ENV
3. **DRY утилиты** (2-4 часа): устранение дублирований

## Метрики проекта

### Текущие показатели

- **Документация**: 892 строки в CLAUDE.md
- **Рецепты**: 581 строка в RECIPES.md
- **Тесты**: 64 автотеста (BATS)
- **Агенты**: 6 специализированных
- **Переводы**: 20+ файлов
- **Коммиты**: Соблюдение Conventional Commits

### Цели качества

- ✅ Все личные данные в `.env` (НЕ в Git)
- ✅ 100% документации на русском
- ✅ Чек-лист перед каждым коммитом
- ✅ CI/CD с автотестами
- ✅ Type hints + docstrings
- ✅ DRY, KISS, SOLID

## Вклад в проект

### Как добавить новый рецепт

Когда вы находите решение проблемы после нескольких попыток:

1. Добавить в [CLAUDE.md](/CLAUDE.md#удачные-рецепты-записываем-что-сработало):
   ```markdown
   ### Рецепт N: Название проблемы

   **Проблема**: Описание проблемы

   **Решение**: Что сработало

   **Когда применять**: Условия применения
   ```

2. Опционально добавить в [RECIPES.md](/RECIPES.md)

3. Закоммитить: `docs: добавлен рецепт для [название]`

### Как улучшить агента

1. Внести изменения в файл агента (`.claude/agents/*.md`)
2. Протестировать на реальной задаче
3. Документировать изменения
4. Закоммитить: `feat: улучшен агент [название]`

## Roadmap

### Ближайшие планы

- [ ] Создать arch.md с текущей архитектурой AnyGen
- [ ] Добавить агента для code review
- [ ] Добавить агента для документирования API
- [ ] Интеграция с русскоязычными LLM (GigaChat, YandexGPT)
- [ ] Примеры использования с FastAPI/Django проектами

### Долгосрочные цели

- [ ] Полноценная документация для контрибьюторов
- [ ] Перевод примеров из оригинального Codev
- [ ] Сборник кейсов использования в реальных проектах
- [ ] Интеграция с популярными Russian DevOps tools

## Лицензия

MIT License (наследуется от ansari-project/codev)

## Контакты и поддержка

- **Репозиторий**: Настраивается через $PROJECT_GITHUB_USER/$PROJECT_GITHUB_REPO
- **Базовый проект**: https://github.com/ansari-project/codev
- **Вопросы**: Открыть Issue в GitHub
- **Документация**: См. README.md, CLAUDE.md, RECIPES.md

---

*Документ создан: 2025-10-19*
*Последнее обновление: 2025-10-19*
*Статус: Living document (обновляется по мере развития проекта)*
