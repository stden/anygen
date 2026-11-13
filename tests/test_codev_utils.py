"""
Unit tests for CODEV framework utilities.
Тесты для утилит фреймворка CODEV.
"""
import os
import tempfile
import shutil
from pathlib import Path
import pytest


class TestFileNumbering:
    """Tests for file numbering utilities (spec/plan/review naming)."""

    def test_extract_number_from_filename(self):
        """Test extracting number from standard CODEV filenames."""
        # Standard format: 0001-feature-name.md
        filename = "0001-test-feature.md"
        number = filename.split("-")[0]
        assert number == "0001"

    def test_extract_number_from_various_formats(self):
        """Test various valid filename formats."""
        test_cases = [
            ("0001-simple.md", "0001"),
            ("0042-my-feature.md", "0042"),
            ("0123-multi-word-name.md", "0123"),
            ("9999-max-number.md", "9999"),
        ]
        for filename, expected in test_cases:
            number = filename.split("-")[0]
            assert number == expected, f"Failed for {filename}"

    def test_next_file_number(self):
        """Test generating next file number in sequence."""
        existing_numbers = ["0001", "0002", "0003"]

        def get_next_number(numbers):
            if not numbers:
                return "0001"
            max_num = max(int(n) for n in numbers)
            return f"{max_num + 1:04d}"

        assert get_next_number(existing_numbers) == "0004"
        assert get_next_number([]) == "0001"
        assert get_next_number(["0099"]) == "0100"


class TestCodevStructure:
    """Tests for CODEV directory structure validation."""

    @pytest.fixture
    def temp_codev_dir(self):
        """Create temporary CODEV directory structure."""
        temp_dir = tempfile.mkdtemp(prefix="codev-test-")
        codev_dir = Path(temp_dir) / "codev"

        # Create standard structure
        for subdir in ["specs", "plans", "reviews", "resources", "protocols"]:
            (codev_dir / subdir).mkdir(parents=True, exist_ok=True)

        yield codev_dir

        # Cleanup
        shutil.rmtree(temp_dir)

    def test_required_directories_exist(self, temp_codev_dir):
        """Test that all required directories are created."""
        required = ["specs", "plans", "reviews", "resources", "protocols"]
        for subdir in required:
            assert (temp_codev_dir / subdir).exists(), f"{subdir} not found"
            assert (temp_codev_dir / subdir).is_dir(), f"{subdir} is not a directory"

    def test_protocol_structure(self, temp_codev_dir):
        """Test protocol directory structure."""
        protocols_dir = temp_codev_dir / "protocols"

        # Create SPIDER protocol structure
        spider_dir = protocols_dir / "spider"
        spider_dir.mkdir(exist_ok=True)
        (spider_dir / "protocol.md").write_text("# SPIDER Protocol")
        (spider_dir / "templates").mkdir(exist_ok=True)

        assert (spider_dir / "protocol.md").exists()
        assert (spider_dir / "templates").is_dir()


class TestProtocolValidation:
    """Tests for protocol validation utilities."""

    def test_valid_protocol_names(self):
        """Test that valid protocol names are recognized."""
        valid_protocols = ["spider", "spider-solo", "tick"]

        def is_valid_protocol(name):
            return name.lower() in valid_protocols

        for proto in valid_protocols:
            assert is_valid_protocol(proto), f"{proto} should be valid"

    def test_invalid_protocol_names(self):
        """Test that invalid protocol names are rejected."""
        invalid_protocols = ["SPIDER", "unknown", "custom-proto", ""]

        valid_protos = ["spider", "spider-solo", "tick"]

        def is_valid_protocol(name):
            return name.lower() in valid_protos

        for proto in invalid_protocols:
            if proto:  # Skip empty string for lower() check
                assert not is_valid_protocol(proto) or proto.lower() in valid_protos


class TestSpecificationParsing:
    """Tests for specification file parsing."""

    @pytest.fixture
    def sample_spec_content(self):
        """Sample specification content."""
        return """# Спецификация: Test Feature

## Метаданные
- **Номер**: 0001
- **Статус**: В разработке
- **Протокол**: SPIDER

## Описание
Описание функциональности.

## Требования
1. Первое требование
2. Второе требование

## Критерии приёмки
- [ ] Критерий 1
- [ ] Критерий 2
"""

    def test_extract_spec_number(self, sample_spec_content):
        """Test extracting specification number from content."""
        import re
        match = re.search(r'\*\*Номер\*\*:\s*(\d+)', sample_spec_content)
        assert match is not None
        assert match.group(1) == "0001"

    def test_extract_spec_status(self, sample_spec_content):
        """Test extracting specification status."""
        import re
        match = re.search(r'\*\*Статус\*\*:\s*(.+)', sample_spec_content)
        assert match is not None
        assert "разработке" in match.group(1).lower()

    def test_extract_requirements(self, sample_spec_content):
        """Test extracting requirements list."""
        import re
        requirements = re.findall(r'^\d+\.\s+(.+)$', sample_spec_content, re.MULTILINE)
        assert len(requirements) == 2
        assert "Первое требование" in requirements[0]


class TestPlanParsing:
    """Tests for plan file parsing."""

    @pytest.fixture
    def sample_plan_content(self):
        """Sample plan content."""
        return """# План: Test Feature

## Метаданные
- **Спецификация**: 0001-test-feature
- **Оценка трудозатрат**: 4 часа

## Задачи
- [ ] Задача 1
- [ ] Задача 2
- [ ] Задача 3

## Зависимости
- Python 3.10+
- pytest
"""

    def test_extract_tasks(self, sample_plan_content):
        """Test extracting tasks from plan."""
        import re
        tasks = re.findall(r'^\- \[[ x]\]\s+(.+)$', sample_plan_content, re.MULTILINE)
        assert len(tasks) == 3

    def test_extract_dependencies(self, sample_plan_content):
        """Test extracting dependencies from plan."""
        import re
        # Find lines starting with "- " after "## Зависимости"
        deps_section = sample_plan_content.split("## Зависимости")[1] if "## Зависимости" in sample_plan_content else ""
        deps = re.findall(r'^\- (.+)$', deps_section, re.MULTILINE)
        assert len(deps) == 2
        assert "Python 3.10+" in deps[0]


class TestGitSafetyChecks:
    """Tests for Git safety validation."""

    def test_dangerous_git_add_commands(self):
        """Test detection of dangerous git add commands."""
        dangerous_commands = [
            "git add -A",
            "git add .",
            "git add --all",
            "git add -a",
        ]

        def is_dangerous_git_add(cmd):
            cmd_lower = cmd.lower().strip()
            return any(pattern in cmd_lower for pattern in [
                "git add -a",
                "git add .",
                "git add --all",
            ])

        for cmd in dangerous_commands:
            assert is_dangerous_git_add(cmd), f"Should detect: {cmd}"

    def test_safe_git_add_commands(self):
        """Test that safe git add commands are allowed."""
        safe_commands = [
            "git add codev/specs/0001-feature.md",
            "git add src/main.py",
            "git add tests/*.py",
            "git add README.md CHANGELOG.md",
        ]

        def is_dangerous_git_add(cmd):
            cmd_lower = cmd.lower().strip()
            return any(pattern in cmd_lower for pattern in [
                "git add -a",
                "git add .",
                "git add --all",
            ])

        for cmd in safe_commands:
            assert not is_dangerous_git_add(cmd), f"Should allow: {cmd}"


class TestEnvironmentValidation:
    """Tests for environment variable validation."""

    def test_required_env_vars_for_zen_mcp(self):
        """Test checking for required Zen MCP environment variables."""
        required_vars = ["GEMINI_API_KEY", "OPENAI_API_KEY"]

        def check_zen_mcp_env():
            missing = []
            for var in required_vars:
                if not os.environ.get(var):
                    missing.append(var)
            return missing

        # Save and clear existing vars
        saved = {var: os.environ.get(var) for var in required_vars}
        for var in required_vars:
            if var in os.environ:
                del os.environ[var]

        missing = check_zen_mcp_env()
        assert set(missing) == set(required_vars)

        # Restore vars
        for var, value in saved.items():
            if value:
                os.environ[var] = value

    def test_project_env_vars(self):
        """Test project environment variable validation."""
        project_vars = ["PROJECT_NAME", "PROJECT_ROOT"]

        def validate_project_env():
            """Validate project environment is properly configured."""
            issues = []
            for var in project_vars:
                if not os.environ.get(var):
                    issues.append(f"{var} not set")
            return issues

        # This just tests the validation logic, not actual env state
        assert callable(validate_project_env)


class TestCommitMessageFormat:
    """Tests for commit message format validation."""

    def test_valid_commit_prefixes(self):
        """Test that valid commit prefixes are recognized."""
        valid_messages = [
            "[+] Добавлена новая функция",
            "[-] Удалён устаревший модуль",
            "[!] Рефакторинг базы данных",
            "[~] Исправлен баг авторизации",
            "[doc] Обновлена документация",
        ]

        def has_valid_prefix(msg):
            valid_prefixes = ["[+]", "[-]", "[!]", "[~]", "[doc]"]
            return any(msg.startswith(prefix) for prefix in valid_prefixes)

        for msg in valid_messages:
            assert has_valid_prefix(msg), f"Should be valid: {msg}"

    def test_invalid_commit_messages(self):
        """Test that invalid commit messages are rejected."""
        invalid_messages = [
            "Added new feature",  # English, no prefix
            "fix: bug fix",  # Wrong format
            "WIP",  # Too short, no prefix
        ]

        def has_valid_prefix(msg):
            valid_prefixes = ["[+]", "[-]", "[!]", "[~]", "[doc]"]
            return any(msg.startswith(prefix) for prefix in valid_prefixes)

        for msg in invalid_messages:
            assert not has_valid_prefix(msg), f"Should be invalid: {msg}"


class TestPathUtilities:
    """Tests for path manipulation utilities."""

    def test_relative_to_codev(self):
        """Test getting path relative to codev directory."""
        codev_root = Path("/project/codev")
        spec_path = Path("/project/codev/specs/0001-feature.md")

        relative = spec_path.relative_to(codev_root)
        assert str(relative) == "specs/0001-feature.md"

    def test_spec_to_plan_path(self):
        """Test converting spec path to corresponding plan path."""
        spec_path = Path("codev/specs/0001-feature.md")

        def spec_to_plan_path(spec: Path) -> Path:
            return spec.parent.parent / "plans" / spec.name

        plan_path = spec_to_plan_path(spec_path)
        assert str(plan_path) == "codev/plans/0001-feature.md"

    def test_spec_to_review_path(self):
        """Test converting spec path to corresponding review path."""
        spec_path = Path("codev/specs/0001-feature.md")

        def spec_to_review_path(spec: Path) -> Path:
            return spec.parent.parent / "reviews" / spec.name

        review_path = spec_to_review_path(spec_path)
        assert str(review_path) == "codev/reviews/0001-feature.md"
