# Руководство по работе с репозиторием Codev

## Структура проекта и организация модулей

- `codev/` содержит активные спецификации, планы, протоколы и обзоры, которые обрабатывают агенты.
- `codev-skeleton/` — устанавливаемый шаблон; обновляйте его при изменении протокольных ресурсов.
- `docs/` содержит подробную методологию; пересматривайте после крупных обновлений процессов.
- `scripts/` предоставляет поддерживаемые точки входа для автоматизации; добавляйте новые скрипты сюда.
- `features/` хранит BDD тесты на Python с использованием behave framework.
- `features/steps/` содержит step definitions для behave тестов.
- `examples/` содержит пошаговые примеры, такие как `todo-manager`, для обучающих сценариев.

## Команды сборки, тестирования и разработки

### Python BDD тесты (behave)
- `./scripts/run-behave-tests.sh` запускает все BDD тесты; выполняйте перед каждым push.
- `./scripts/run-behave-tests.sh --feature codev_installation` запускает конкретный feature.
- `./scripts/run-behave-tests.sh --tags @smoke` запускает только smoke тесты.
- `./scripts/run-behave-tests.sh --coverage` генерирует отчёт покрытия кода.
- `uv run behave features --dry-run` проверяет синтаксис Gherkin без выполнения тестов.

### Зависимости
- `uv` — современный менеджер пакетов Python (устанавливается через `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- `behave` — BDD framework для Python
- `pytest`, `pytest-bdd`, `pytest-cov` — дополнительные тестовые инструменты

## Стиль кода и соглашения об именовании

### Bash скрипты
- Автоматизация использует Bash: начинайте с `#!/usr/bin/env bash`, включайте `set -euo pipefail`.
- Используйте отступ в два пробела внутри функций, четыре внутри условий.
- Предпочитайте `lower_snake_case` для вспомогательных функций (`install_from_local`).
- Держите протокольные и плановые ресурсы декларативными; избегайте путей, специфичных для окружения.

### Python код
- Используйте `black` для форматирования (line-length: 100).
- Используйте `ruff` для линтинга.
- Используйте `mypy` для проверки типов.
- Следуйте PEP 8 и Google Style Guide.

### Gherkin feature файлы
- Используйте `# language: ru` в начале файла для русского языка.
- Используйте правильные русские термины: `Структура сценария` (не "Схема сценария").
- Форматируйте таблицы примеров с выравниванием по колонкам.
- Держите сценарии фокусированными и понятными.

## Руководство по тестированию

### BDD тесты (behave)
- Feature файлы располагаются в `features/` директории.
- Step definitions в `features/steps/` именуются как `<feature_name>_steps.py`.
- Используйте `features/environment.py` для настройки окружения и hooks.
- Каждый feature файл должен иметь осмысленное описание и предысторию.
- Тесты должны быть изолированными и не влиять друг на друга.
- Используйте временные директории для тестовых проектов.
- Очищайте созданные ресурсы в after hooks.

### Структура BDD тестов
```
features/
├── environment.py              # Behave configuration и hooks
├── codev_installation.feature  # Тесты установки Codev
├── spider_protocol.feature     # Тесты протокола SPIDER
├── zen_mcp_integration.feature # Тесты интеграции Zen MCP
└── steps/
    ├── codev_installation_steps.py
    ├── zen_mcp_steps.py
    └── ... (другие step definitions)
```

### Запуск тестов в CI/CD
- GitHub Actions автоматически запускает behave тесты при push и pull requests.
- Workflow файл: `.github/workflows/codev-tests.yml`
- Тесты выполняются на Python 3.10 с использованием uv.
- Результаты тестов сохраняются как артефакты (retention: 7 дней).

## Руководство по коммитам и Pull Request

### Формат commit-сообщений (ОБЯЗАТЕЛЬНО на русском!)
Используйте префиксы:
- `[+]` — Новая функциональность
- `[-]` — Удаление устаревшего
- `[!]` — Рефакторинг
- `[~]` — Исправление багов
- `[doc]` — Только документация

Пример:
```
[+] Добавлены BDD тесты для протокола SPIDER

Созданы feature файлы:
- features/spider_protocol.feature
- features/steps/spider_protocol_steps.py

Тесты покрывают все фазы SPIDER: Specify → Plan → Implement → Defend → Evaluate → Review

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Pull Request
- Pull request должны ссылаться на управляющую спецификацию в `codev/specs`.
- Указывать затронутые протоколы и прикладывать ресурсы до/после для изменений шаблона.
- Запрашивайте проверку от агента, ответственного за область.
- Дождитесь подтверждения автоматических тестов перед слиянием.

## Советы по безопасности и конфигурации

### Управление секретами
- Храните ВСЕ секреты в `.env` файле (защищён `.gitignore`).
- Используйте `.env.example` как шаблон без реальных значений.
- НИКОГДА не коммитьте файлы с секретами (`.env`, credentials, ключи API).
- Документируйте все необходимые переменные окружения в `.env.example`.

### Git безопасность
- ❌ НИКОГДА не используйте `git add -A` или `git add .`
- ✅ ВСЕГДА добавляйте файлы явно: `git add file1.py file2.md`
- ✅ Проверяйте `git status` перед каждым commit.
- ✅ Используйте `.gitignore` для защиты чувствительных данных.

### Тестовое окружение
- Тесты используют изолированные временные директории.
- Не затрагивают хост-окружение пользователя.
- Используют XDG переменные для песочницы.
- Очищают все созданные ресурсы после выполнения.

## Специализированные агенты

### TDD агенты
- `tdd-test.md` — фаза Test (Red): написание failing тестов
- `tdd-code.md` — фаза Code (Green): минимальная реализация
- `tdd-refactor.md` — фаза Refactor: улучшение кода

### BDD агент
- `bdd-features.md` — создание feature файлов на Gherkin

### Другие агенты
- `env-manager.md` — безопасное управление .env файлами
- `spider-protocol-updater.md` — анализ улучшений SPIDER в других репозиториях
- `architecture-documenter.md` — поддержка документации архитектуры
- `codev-updater.md` — обновление Codev framework

## Zen MCP интеграция

### Установка
```bash
./scripts/install-zen-mcp.sh
```

### Конфигурация
- Zen MCP установлен в `~/.zen-mcp-server`
- Symlink `.env`: `~/.zen-mcp-server/.env -> project/.env`
- API ключи: `GEMINI_API_KEY`, `OPENAI_API_KEY`, `XAI_API_KEY`

### Использование
- Мультиагентная консультация в протоколе SPIDER
- Консультации с Gemini 2.5 Pro, GPT-5, Grok
- Консенсус нескольких AI повышает качество кода

## Полезные команды

### Проверка синтаксиса
```bash
# Проверить Gherkin синтаксис
uv run behave features --dry-run

# Проверить Python код
black --check features/
ruff check features/
mypy features/
```

### Отладка тестов
```bash
# Запустить конкретный сценарий
uv run behave features/codev_installation.feature:10

# Показать stdout во время тестов
./scripts/run-behave-tests.sh --verbose

# Запустить с отладочной информацией
uv run behave features --verbose --no-capture
```

### Генерация отчётов
```bash
# Отчёт покрытия кода
./scripts/run-behave-tests.sh --coverage

# HTML отчёт в htmlcov/index.html
open htmlcov/index.html
```

## Ссылки на документацию

- [README.md](README.md) — основная документация проекта
- [CLAUDE.md](CLAUDE.md) — инструкции для AI-агентов
- [INSTALL.md](INSTALL.md) — руководство по установке
- [RECIPES.md](RECIPES.md) — практические примеры и рецепты
- [docs/HOW_TO_USE_CODEV.md](docs/HOW_TO_USE_CODEV.md) — применение Codev к проектам
- [codev/protocols/](codev/protocols/) — протоколы разработки (SPIDER, SPIDER-SOLO, TICK)

---

**Примечание**: Этот документ автоматически генерируется и поддерживается AI-агентами. При внесении изменений в структуру проекта или процессы разработки обновляйте этот файл соответственно.
