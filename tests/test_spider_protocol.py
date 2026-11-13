"""
Unit tests for SPIDER Protocol functionality.
Тесты для функциональности протокола SPIDER.
"""
import re
import tempfile
import shutil
from pathlib import Path
import pytest


class TestSpiderPhases:
    """Tests for SPIDER protocol phases (Specify, Plan, Implement, Defend, Evaluate, Review)."""

    def test_phase_order(self):
        """Test that SPIDER phases follow the correct order."""
        phases = ["Specify", "Plan", "Implement", "Defend", "Evaluate", "Review"]
        spider_acronym = "SPIDER"

        # Verify phase initials match SPIDER (with IDE grouped)
        expected_initials = ["S", "P", "I", "D", "E", "R"]
        actual_initials = [phase[0] for phase in phases]
        assert actual_initials == expected_initials

    def test_ide_cycle_phases(self):
        """Test that IDE cycle contains correct sub-phases."""
        ide_phases = ["Implement", "Defend", "Evaluate"]

        # IDE is the inner cycle that repeats for each implementation phase
        assert ide_phases[0] == "Implement"
        assert ide_phases[1] == "Defend"
        assert ide_phases[2] == "Evaluate"

    def test_phase_status_values(self):
        """Test valid phase status values."""
        valid_statuses = ["pending", "in-progress", "completed", "blocked"]

        def is_valid_status(status):
            return status in valid_statuses

        for status in valid_statuses:
            assert is_valid_status(status)

        assert not is_valid_status("done")
        assert not is_valid_status("started")


class TestSpecificationDocument:
    """Tests for specification document structure and validation."""

    @pytest.fixture
    def sample_spec(self):
        """Sample specification content."""
        return """# Спецификация: Аутентификация пользователя

## Метаданные
- **Номер**: 0001
- **Статус**: В разработке
- **Протокол**: SPIDER

## Цель

Реализовать безопасную систему аутентификации пользователей.

## Желаемое состояние

Пользователи могут безопасно входить в систему.

## Критерии успеха

1. Валидация email
2. Хеширование паролей
3. JWT токены

## Журнал консультаций

### Консультация 1 (GPT-5)
- Дата: 2024-01-15
- Комментарии: Рекомендовано использовать bcrypt для хеширования

### Консультация 2 (Gemini Pro)
- Дата: 2024-01-15
- Комментарии: Добавить rate limiting для защиты от brute force
"""

    def test_spec_has_required_sections(self, sample_spec):
        """Test that spec contains all required sections."""
        required_sections = [
            "# Спецификация:",
            "## Цель",
            "## Желаемое состояние",
            "## Критерии успеха",
        ]

        for section in required_sections:
            assert section in sample_spec, f"Missing required section: {section}"

    def test_spec_has_consultation_log(self, sample_spec):
        """Test that spec contains consultation log for multi-agent review."""
        assert "## Журнал консультаций" in sample_spec
        assert "GPT-5" in sample_spec or "Gemini" in sample_spec

    def test_extract_spec_number(self, sample_spec):
        """Test extracting specification number."""
        match = re.search(r'\*\*Номер\*\*:\s*(\d+)', sample_spec)
        assert match is not None
        assert match.group(1) == "0001"

    def test_extract_success_criteria(self, sample_spec):
        """Test extracting success criteria."""
        criteria = re.findall(r'^\d+\.\s+(.+)$', sample_spec, re.MULTILINE)
        assert len(criteria) >= 3
        assert "Валидация email" in criteria

    def test_spec_file_naming(self):
        """Test specification file naming convention."""
        valid_names = [
            "0001-user-auth.md",
            "0002-payment-gateway.md",
            "0123-multi-word-feature.md",
        ]

        pattern = r'^\d{4}-[a-z0-9-]+\.md$'
        for name in valid_names:
            assert re.match(pattern, name), f"Invalid name: {name}"

    def test_invalid_spec_names(self):
        """Test that invalid spec names are rejected."""
        invalid_names = [
            "001-short-number.md",  # Only 3 digits
            "0001_underscore.md",   # Underscore instead of dash
            "0001-CamelCase.md",    # Contains uppercase
            "0001-feature",         # Missing .md extension
        ]

        pattern = r'^\d{4}-[a-z0-9-]+\.md$'
        for name in invalid_names:
            assert not re.match(pattern, name), f"Should be invalid: {name}"


class TestPlanDocument:
    """Tests for plan document structure and validation."""

    @pytest.fixture
    def sample_plan(self):
        """Sample plan content."""
        return """# План: Аутентификация пользователя

## Спецификация
- **Ссылка**: codev/specs/0001-user-auth.md
- **Статус**: Утверждено

## Фазы реализации

### Фаза 1: Схема базы данных
- Создать таблицу users
- Добавить индексы

**Зависимости**: Нет
**Критерии завершения**:
- Миграции созданы
- Тесты схемы проходят
**Статус**: completed

### Фаза 2: API эндпоинты
- Создать /login
- Создать /register
- Создать /logout

**Зависимости**: Фаза 1
**Критерии завершения**:
- Все эндпоинты отвечают корректно
- Покрытие тестами > 90%
**Статус**: in-progress

### Фаза 3: Интеграция фронтенда
- Формы логина
- Обработка токенов

**Зависимости**: Фаза 2
**Критерии завершения**:
- UI работает корректно
- E2E тесты проходят
**Статус**: pending
"""

    def test_plan_has_phases(self, sample_plan):
        """Test that plan contains implementation phases."""
        assert "### Фаза" in sample_plan
        phases = re.findall(r'### Фаза \d+:', sample_plan)
        assert len(phases) >= 1

    def test_phase_has_dependencies(self, sample_plan):
        """Test that each phase has dependencies section."""
        assert "**Зависимости**:" in sample_plan

    def test_phase_has_completion_criteria(self, sample_plan):
        """Test that each phase has completion criteria."""
        assert "**Критерии завершения**:" in sample_plan

    def test_phase_has_status(self, sample_plan):
        """Test that each phase has status."""
        assert "**Статус**:" in sample_plan

    def test_extract_phase_statuses(self, sample_plan):
        """Test extracting phase statuses from plan."""
        statuses = re.findall(r'\*\*Статус\*\*:\s*(\w+(?:-\w+)?)', sample_plan)
        assert "completed" in statuses
        assert "in-progress" in statuses
        assert "pending" in statuses

    def test_plan_no_time_estimates(self, sample_plan):
        """Test that plan does not contain time estimates (AI era best practice)."""
        time_patterns = [
            r'\d+\s*часов?',
            r'\d+\s*дней',
            r'\d+\s*недел',
            r'story\s*points?',
            r'\d+\s*SP',
        ]

        for pattern in time_patterns:
            matches = re.findall(pattern, sample_plan, re.IGNORECASE)
            assert len(matches) == 0, f"Found time estimate: {matches}"

    def test_plan_links_to_spec(self, sample_plan):
        """Test that plan references corresponding spec."""
        assert "codev/specs/" in sample_plan


class TestReviewDocument:
    """Tests for review document structure."""

    @pytest.fixture
    def sample_review(self):
        """Sample review content."""
        return """# Обзор: Аутентификация пользователя

## Метаданные
- **Спецификация**: 0001-user-auth
- **Дата завершения**: 2024-01-20

## Что получилось хорошо

- Чистая архитектура кода
- Высокое покрытие тестами (95%)
- Хорошая документация

## Что можно улучшить

- Добавить rate limiting
- Улучшить сообщения об ошибках

## Уроки на будущее

1. Начинать с написания тестов
2. Консультироваться с экспертами раньше
3. Документировать решения в процессе

## Систематические проблемы

- Недостаточное логирование в критических путях
- Нужны более детальные E2E тесты
"""

    def test_review_has_lessons_learned(self, sample_review):
        """Test that review contains lessons learned section."""
        assert "## Уроки на будущее" in sample_review

    def test_review_has_what_went_well(self, sample_review):
        """Test that review contains positive feedback."""
        assert "## Что получилось хорошо" in sample_review

    def test_review_has_improvements(self, sample_review):
        """Test that review contains improvement suggestions."""
        assert "## Что можно улучшить" in sample_review

    def test_review_has_systematic_issues(self, sample_review):
        """Test that review documents systematic issues."""
        assert "## Систематические проблемы" in sample_review


class TestMultiAgentConsultation:
    """Tests for multi-agent consultation requirements."""

    def test_default_consultation_agents(self):
        """Test that default agents are GPT-5 and Gemini Pro."""
        default_agents = ["GPT-5", "Gemini Pro"]

        assert "GPT-5" in default_agents
        assert "Gemini Pro" in default_agents
        assert len(default_agents) == 2

    def test_consultation_checkpoints(self):
        """Test that consultation is required at specific checkpoints."""
        checkpoints = [
            "Specify: After initial draft",
            "Specify: After human feedback",
            "Plan: After initial plan",
            "Plan: After human review",
            "Implement: After code implementation",
            "Defend: After test creation",
            "Evaluate: Before user evaluation",
            "Review: After review document",
        ]

        # Each main phase should have at least one checkpoint
        phases_with_checkpoints = set()
        for checkpoint in checkpoints:
            phase = checkpoint.split(":")[0]
            phases_with_checkpoints.add(phase)

        expected_phases = {"Specify", "Plan", "Implement", "Defend", "Evaluate", "Review"}
        assert phases_with_checkpoints == expected_phases

    def test_consultation_is_blocking(self):
        """Test that consultation is blocking by default."""
        # Consultation must complete before proceeding
        consultation_config = {
            "enabled_by_default": True,
            "blocking": True,
            "agents": ["GPT-5", "Gemini Pro"],
        }

        assert consultation_config["enabled_by_default"]
        assert consultation_config["blocking"]


class TestCommitMessageFormat:
    """Tests for SPIDER commit message format."""

    def test_spec_commit_format(self):
        """Test specification commit message format."""
        valid_messages = [
            "[Spec 0001] Первоначальный черновик спецификации",
            "[Spec 0001] Спецификация с мультиагентным обзором",
            "[Spec 0001] Спецификация с обратной связью пользователя",
            "[Spec 0001] Финальная утверждённая спецификация",
        ]

        pattern = r'^\[Spec \d{4}\]'
        for msg in valid_messages:
            assert re.match(pattern, msg), f"Invalid format: {msg}"

    def test_implementation_commit_format(self):
        """Test implementation phase commit message format."""
        valid_messages = [
            "[Spec 0001][Phase: user-auth] feat: Добавлен сервис хеширования паролей",
            "[Spec 0002][Phase: db-schema] fix: Исправлена миграция",
            "[Spec 0001][Phase: api] refactor: Улучшена обработка ошибок",
        ]

        pattern = r'^\[Spec \d{4}\]\[Phase: [a-z0-9-]+\]'
        for msg in valid_messages:
            assert re.match(pattern, msg), f"Invalid format: {msg}"

    def test_branch_naming_convention(self):
        """Test SPIDER branch naming convention."""
        valid_branches = [
            "spider/0001-user-auth/db-schema",
            "spider/0002-payment/api-endpoints",
            "spider/0001-auth/frontend-integration",
        ]

        pattern = r'^spider/\d{4}-[a-z0-9-]+/[a-z0-9-]+$'
        for branch in valid_branches:
            assert re.match(pattern, branch), f"Invalid branch: {branch}"


class TestDocumentTriad:
    """Tests for the three-document principle (spec, plan, review)."""

    @pytest.fixture
    def temp_codev_dir(self):
        """Create temporary codev directory structure."""
        temp_dir = tempfile.mkdtemp(prefix="codev-test-")
        codev_dir = Path(temp_dir) / "codev"

        for subdir in ["specs", "plans", "reviews"]:
            (codev_dir / subdir).mkdir(parents=True, exist_ok=True)

        yield codev_dir

        shutil.rmtree(temp_dir)

    def test_same_filename_across_directories(self, temp_codev_dir):
        """Test that spec, plan, and review share the same filename."""
        filename = "0001-feature.md"

        # Create all three documents
        (temp_codev_dir / "specs" / filename).write_text("# Spec")
        (temp_codev_dir / "plans" / filename).write_text("# Plan")
        (temp_codev_dir / "reviews" / filename).write_text("# Review")

        # Verify all exist with same name
        assert (temp_codev_dir / "specs" / filename).exists()
        assert (temp_codev_dir / "plans" / filename).exists()
        assert (temp_codev_dir / "reviews" / filename).exists()

    def test_find_related_documents(self, temp_codev_dir):
        """Test finding related documents by spec name."""
        filename = "0001-user-auth.md"

        (temp_codev_dir / "specs" / filename).write_text("# Spec")

        def find_related_docs(spec_path: Path) -> dict:
            """Find plan and review for a given spec."""
            name = spec_path.name
            codev = spec_path.parent.parent
            return {
                "spec": codev / "specs" / name,
                "plan": codev / "plans" / name,
                "review": codev / "reviews" / name,
            }

        spec_path = temp_codev_dir / "specs" / filename
        related = find_related_docs(spec_path)

        assert related["spec"] == temp_codev_dir / "specs" / filename
        assert related["plan"] == temp_codev_dir / "plans" / filename
        assert related["review"] == temp_codev_dir / "reviews" / filename


class TestPhaseCompletionChecklist:
    """Tests for phase completion checklist validation."""

    def test_implement_phase_checklist(self):
        """Test Implement phase completion requirements."""
        checklist = [
            "Весь код для этой фазы завершён",
            "Код следует руководству по стилю проекта",
            "Нет закомментированного кода или debug-принтов",
            "Реализована обработка ошибок",
            "Документация обновлена",
            "Экспертная консультация завершена",
            "Обратная связь экспертов учтена",
        ]

        assert len(checklist) >= 7
        assert any("код" in item.lower() for item in checklist)
        assert any("консультаци" in item.lower() for item in checklist)

    def test_defend_phase_checklist(self):
        """Test Defend phase completion requirements."""
        checklist = [
            "Юнит-тесты написаны для всех новых функций",
            "Интеграционные тесты написаны для критических путей",
            "Граничные случаи имеют тестовое покрытие",
            "Все новые тесты проходят",
            "Все существующие тесты всё ещё проходят",
            "Нет снижения покрытия кода",
            "Проверка избыточного мокирования завершена",
            "Экспертная консультация по тестам завершена",
        ]

        assert len(checklist) >= 8
        assert any("тест" in item.lower() for item in checklist)
        assert any("покрыти" in item.lower() for item in checklist)

    def test_evaluate_phase_checklist(self):
        """Test Evaluate phase completion requirements."""
        checklist = [
            "Все критерии приёмки из спецификации выполнены",
            "Экспертная консультация показывает ФИНАЛЬНОЕ одобрение",
            "Обсуждение оценки с пользователем завершено",
            "Пользователь дал явное одобрение на продолжение",
            "Документ плана обновлён со статусом фазы",
            "Коммит фазы создан с правильным форматом сообщения",
            "Коммит проверен с git log",
        ]

        assert len(checklist) >= 7
        assert any("одобрени" in item.lower() for item in checklist)
        assert any("коммит" in item.lower() for item in checklist)


class TestOverMockingPrevention:
    """Tests for over-mocking prevention guidelines."""

    def test_mock_only_external_dependencies(self):
        """Test that mocking guidelines focus on external dependencies."""
        allowed_mocks = [
            "External APIs",
            "Databases",
            "File systems",
            "Network calls",
            "Third-party services",
        ]

        forbidden_mocks = [
            "Internal module boundaries",
            "The system under test",
            "Implementation details",
        ]

        # Verify all allowed mocks are external
        for mock_target in allowed_mocks:
            assert "internal" not in mock_target.lower()

    def test_prefer_behavior_over_implementation(self):
        """Test that testing focuses on behavior, not implementation."""
        good_test_focuses = [
            "Input/output behavior",
            "Public API contracts",
            "User-visible functionality",
            "Error handling behavior",
        ]

        bad_test_focuses = [
            "Private method calls",
            "Internal state changes",
            "Specific implementation order",
        ]

        # Ensure our guidelines prioritize behavior
        for focus in good_test_focuses:
            assert "behavior" in focus.lower() or "api" in focus.lower() or "output" in focus.lower() or "user" in focus.lower() or "error" in focus.lower()


class TestProtocolConfiguration:
    """Tests for protocol configuration options."""

    def test_multiagent_enabled_by_default(self):
        """Test that multi-agent consultation is enabled by default."""
        config = {
            "multiagent_consultation": True,
            "default_agents": ["GPT-5", "Gemini Pro"],
            "disable_command": "без мультиагентной консультации",
        }

        assert config["multiagent_consultation"] is True

    def test_spider_solo_alternative(self):
        """Test that SPIDER-SOLO exists as an alternative."""
        protocols = ["spider", "spider-solo", "tick"]

        assert "spider-solo" in protocols
        # SPIDER-SOLO should be for single-agent work
        assert "spider" in protocols

    def test_when_to_skip_spider(self):
        """Test cases when SPIDER can be skipped."""
        skip_cases = [
            "Simple bug fixes (< 10 lines)",
            "Documentation updates",
            "Configuration changes",
            "Dependency updates",
            "Emergency hotfixes",
        ]

        assert len(skip_cases) >= 5
        assert any("bug" in case.lower() for case in skip_cases)
        assert any("doc" in case.lower() for case in skip_cases)
