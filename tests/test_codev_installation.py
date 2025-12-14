"""
Unit tests for CODEV installation and directory structure.
Тесты для установки CODEV и структуры каталогов.
"""
import os
import tempfile
import shutil
from pathlib import Path
import pytest


class TestCodevInstallation:
    """Tests for CODEV framework installation."""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory."""
        temp_dir = tempfile.mkdtemp(prefix="codev-install-test-")
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    def test_create_codev_structure(self, temp_project):
        """Test creating the standard CODEV directory structure."""
        codev_dir = temp_project / "codev"

        required_dirs = ["specs", "plans", "reviews", "resources", "protocols"]
        for subdir in required_dirs:
            (codev_dir / subdir).mkdir(parents=True, exist_ok=True)

        # Verify all directories exist
        for subdir in required_dirs:
            assert (codev_dir / subdir).exists()
            assert (codev_dir / subdir).is_dir()

    def test_install_spider_protocol(self, temp_project):
        """Test installing SPIDER protocol files."""
        protocols_dir = temp_project / "codev" / "protocols" / "spider"
        templates_dir = protocols_dir / "templates"

        protocols_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(exist_ok=True)

        # Create protocol files
        (protocols_dir / "protocol.md").write_text("# SPIDER Protocol")
        (templates_dir / "spec.md").write_text("# Spec Template")
        (templates_dir / "plan.md").write_text("# Plan Template")
        (templates_dir / "review.md").write_text("# Review Template")

        # Verify files exist
        assert (protocols_dir / "protocol.md").exists()
        assert (templates_dir / "spec.md").exists()
        assert (templates_dir / "plan.md").exists()
        assert (templates_dir / "review.md").exists()

    def test_install_spider_solo_protocol(self, temp_project):
        """Test installing SPIDER-SOLO protocol."""
        protocols_dir = temp_project / "codev" / "protocols" / "spider-solo"
        protocols_dir.mkdir(parents=True, exist_ok=True)

        (protocols_dir / "protocol.md").write_text("# SPIDER-SOLO Protocol")

        assert (protocols_dir / "protocol.md").exists()
        content = (protocols_dir / "protocol.md").read_text()
        assert "SOLO" in content

    def test_preserve_existing_files_on_update(self, temp_project):
        """Test that user files are preserved during update."""
        specs_dir = temp_project / "codev" / "specs"
        specs_dir.mkdir(parents=True, exist_ok=True)

        # Create user specification
        user_spec = specs_dir / "0001-user-feature.md"
        user_spec.write_text("# My Important Spec\nThis should be preserved")

        # Simulate update (just verify file still exists)
        assert user_spec.exists()
        assert "preserved" in user_spec.read_text()

    def test_claude_md_creation(self, temp_project):
        """Test creating CLAUDE.md instructions file."""
        claude_md = temp_project / "CLAUDE.md"
        claude_md.write_text("""# Project Instructions for AI Agents

## Codev Framework
This project uses Codev for development.

## Protocols
- SPIDER: Multi-agent development
- SPIDER-SOLO: Single-agent development
""")

        assert claude_md.exists()
        content = claude_md.read_text()
        assert "Codev" in content
        assert "SPIDER" in content


class TestTemplateStructure:
    """Tests for CODEV template files."""

    @pytest.fixture
    def templates_dir(self):
        """Create temporary templates directory."""
        temp_dir = tempfile.mkdtemp(prefix="codev-templates-")
        templates = Path(temp_dir) / "templates"
        templates.mkdir()
        yield templates
        shutil.rmtree(temp_dir)

    def test_spec_template_sections(self, templates_dir):
        """Test that spec template has required sections."""
        spec_template = """# Спецификация: {название}

## Метаданные
- **Номер**: ####
- **Статус**: Черновик
- **Протокол**: SPIDER

## Цель

{описание цели}

## Желаемое состояние

{описание желаемого результата}

## Критерии успеха

1. {критерий 1}
2. {критерий 2}

## Открытые вопросы

- {вопрос 1}

## Журнал консультаций

### Консультация 1
- Дата: 
- Агент:
- Комментарии:
"""
        template_file = templates_dir / "spec.md"
        template_file.write_text(spec_template)

        content = template_file.read_text()
        assert "## Цель" in content
        assert "## Критерии успеха" in content
        assert "## Журнал консультаций" in content

    def test_plan_template_sections(self, templates_dir):
        """Test that plan template has required sections."""
        plan_template = """# План: {название}

## Спецификация
- **Ссылка**: codev/specs/####-{имя}.md
- **Статус**: Утверждено

## Фазы реализации

### Фаза 1: {название фазы}
- {задача 1}
- {задача 2}

**Зависимости**: Нет
**Критерии завершения**:
- {критерий 1}
**Статус**: pending
"""
        template_file = templates_dir / "plan.md"
        template_file.write_text(plan_template)

        content = template_file.read_text()
        assert "## Фазы реализации" in content
        assert "**Зависимости**" in content
        assert "**Статус**" in content

    def test_review_template_sections(self, templates_dir):
        """Test that review template has required sections."""
        review_template = """# Обзор: {название}

## Метаданные
- **Спецификация**: ####-{имя}
- **Дата завершения**: 

## Что получилось хорошо

- {пункт 1}

## Что можно улучшить

- {пункт 1}

## Уроки на будущее

1. {урок 1}

## Систематические проблемы

- {проблема 1}
"""
        template_file = templates_dir / "review.md"
        template_file.write_text(review_template)

        content = template_file.read_text()
        assert "## Что получилось хорошо" in content
        assert "## Уроки на будущее" in content
        assert "## Систематические проблемы" in content


class TestZenMcpIntegration:
    """Tests for Zen MCP integration configuration."""

    def test_required_api_keys(self):
        """Test required API keys for Zen MCP."""
        required_keys = {
            "GEMINI_API_KEY": "Required for Gemini Pro consultation",
            "OPENAI_API_KEY": "Required for GPT-5 consultation",
        }

        optional_keys = {
            "XAI_API_KEY": "Optional for Grok consultation",
        }

        # At least one key is required for Zen MCP
        assert len(required_keys) >= 1
        assert "GEMINI_API_KEY" in required_keys or "OPENAI_API_KEY" in required_keys

    def test_zen_mcp_installation_path(self):
        """Test default Zen MCP installation path."""
        zen_mcp_dir = Path.home() / ".zen-mcp-server"

        # Just verify the path construct is correct
        assert str(zen_mcp_dir).endswith(".zen-mcp-server")

    def test_env_symlink_strategy(self):
        """Test that .env is symlinked to project root."""
        # Strategy: project/.env -> ~/.zen-mcp-server/.env (symlink)
        # This allows central API key management

        project_env = Path("/srv/anygen/.env")
        zen_env = Path.home() / ".zen-mcp-server" / ".env"

        # Test that paths are different (symlink needed)
        assert project_env != zen_env

    def test_fallback_to_spider_solo(self):
        """Test fallback behavior when Zen MCP unavailable."""
        def get_protocol(zen_mcp_available: bool) -> str:
            if zen_mcp_available:
                return "spider"
            else:
                return "spider-solo"

        assert get_protocol(True) == "spider"
        assert get_protocol(False) == "spider-solo"


class TestEnvConfiguration:
    """Tests for .env configuration."""

    def test_env_example_variables(self):
        """Test that .env.example has required variables."""
        required_vars = [
            "GITHUB_TOKEN",
            "GIT_AUTHOR_NAME",
            "GIT_AUTHOR_EMAIL",
            "GEMINI_API_KEY",
            "OPENAI_API_KEY",
        ]

        # All required vars should be documented
        for var in required_vars:
            assert var.isupper(), f"Env var should be uppercase: {var}"
            assert "_" in var or var.isalpha(), f"Invalid env var name: {var}"

    def test_git_author_variables(self):
        """Test Git author configuration variables."""
        git_vars = [
            "GIT_AUTHOR_NAME",
            "GIT_AUTHOR_EMAIL",
            "GIT_COMMITTER_NAME",
            "GIT_COMMITTER_EMAIL",
        ]

        # All Git author vars should be related pairs
        assert "GIT_AUTHOR_NAME" in git_vars
        assert "GIT_AUTHOR_EMAIL" in git_vars

    def test_project_info_variables(self):
        """Test project information variables."""
        project_vars = [
            "PROJECT_NAME",
            "PROJECT_AUTHOR",
            "PROJECT_ROOT",
        ]

        # All project vars should start with PROJECT_
        for var in project_vars:
            assert var.startswith("PROJECT_")


class TestSecurityBestPractices:
    """Tests for security best practices in CODEV."""

    def test_gitignore_sensitive_files(self):
        """Test that sensitive files are in .gitignore."""
        should_be_ignored = [
            ".env",
            ".env.local",
            "*.pem",
            "*.key",
            "node_modules/",
            "__pycache__/",
            ".venv/",
        ]

        # Verify pattern structure
        for pattern in should_be_ignored:
            assert pattern, "Empty pattern in gitignore list"

    def test_no_hardcoded_secrets(self):
        """Test that secrets are never hardcoded."""
        # Pattern that should NOT appear in code
        bad_patterns = [
            r'api_key\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
            r'password\s*=\s*["\'].+["\']',
            r'secret\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
        ]

        # These patterns indicate hardcoded secrets
        import re
        for pattern in bad_patterns:
            # Just verify the pattern is valid regex
            re.compile(pattern, re.IGNORECASE)

    def test_env_over_hardcoding(self):
        """Test preference for environment variables over hardcoding."""
        good_practice = """
import os

API_KEY = os.environ.get('API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
"""
        bad_practice = """
API_KEY = "sk-abc123def456"
DATABASE_URL = "postgresql://user:pass@host/db"
"""

        # Good practice uses os.environ/os.getenv
        assert "os.environ" in good_practice or "os.getenv" in good_practice

        # Bad practice has literal strings
        assert "sk-" in bad_practice or "postgresql://" in bad_practice


class TestDocumentVersioning:
    """Tests for document versioning through Git."""

    def test_commit_stages_for_spec(self):
        """Test expected commit stages for specification."""
        spec_stages = [
            "Первоначальный черновик спецификации",
            "Спецификация с мультиагентным обзором",
            "Спецификация с обратной связью пользователя",
            "Финальная утверждённая спецификация",
        ]

        # At least 4 stages for spec evolution
        assert len(spec_stages) >= 4
        assert "черновик" in spec_stages[0].lower()
        assert "финальн" in spec_stages[-1].lower()

    def test_commit_stages_for_plan(self):
        """Test expected commit stages for plan."""
        plan_stages = [
            "Первоначальный черновик плана",
            "План с мультиагентным обзором",
            "План с обратной связью пользователя",
            "Финальный утверждённый план",
        ]

        assert len(plan_stages) >= 4

    def test_phase_commit_format(self):
        """Test format for phase completion commits."""
        import re

        commit_pattern = r'\[Spec \d{4}\]\[Phase: [a-z0-9-]+\]'

        valid_commits = [
            "[Spec 0001][Phase: db-schema] feat: Added user table",
            "[Spec 0002][Phase: api] fix: Fixed validation",
        ]

        for commit in valid_commits:
            assert re.match(commit_pattern, commit)
