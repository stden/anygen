"""
Step definitions для тестирования установки Codev
"""
import os
import shutil
import tempfile
from pathlib import Path
from behave import given, when, then
import subprocess


@given('создан временный тестовый проект')
def step_create_temp_project(context):
    """Создать временный директорий для тестирования"""
    context.test_dir = tempfile.mkdtemp(prefix='codev-test-')
    context.project_root = Path(__file__).parent.parent.parent
    os.chdir(context.test_dir)

    # Инициализировать git
    subprocess.run(['git', 'init'], check=True, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True)


@given('файл CLAUDE.md существует с содержимым "{content}"')
def step_create_claude_md(context, content):
    """Создать CLAUDE.md с заданным содержимым"""
    claude_md = Path(context.test_dir) / 'CLAUDE.md'
    claude_md.write_text(content)
    context.original_claude_content = content


@given('Zen MCP недоступен')
def step_zen_mcp_unavailable(context):
    """Симулировать отсутствие Zen MCP"""
    # Удалить mcp из PATH
    if 'PATH' in os.environ:
        paths = os.environ['PATH'].split(os.pathsep)
        # Фильтровать пути содержащие mcp
        filtered_paths = [p for p in paths if 'mcp' not in p.lower()]
        os.environ['PATH'] = os.pathsep.join(filtered_paths)

    context.zen_mcp_available = False


@given('Codev уже установлен')
def step_codev_already_installed(context):
    """Установить Codev в тестовый проект"""
    # Сначала установить Codev
    step_install_codev(context)

    # Создать пользовательские файлы
    specs_dir = Path(context.test_dir) / 'codev' / 'specs'
    specs_dir.mkdir(parents=True, exist_ok=True)
    (specs_dir / '0001-user-feature.md').write_text('# User Feature Spec')

    plans_dir = Path(context.test_dir) / 'codev' / 'plans'
    plans_dir.mkdir(parents=True, exist_ok=True)
    (plans_dir / '0001-user-feature.md').write_text('# User Feature Plan')


@given('файл CLAUDE.md с правами "{permissions}"')
def step_claude_md_with_permissions(context, permissions):
    """Создать CLAUDE.md с конкретными правами"""
    claude_md = Path(context.test_dir) / 'CLAUDE.md'
    claude_md.write_text('# Test Project')

    # Установить права
    os.chmod(claude_md, int(permissions, 8))
    context.original_permissions = permissions


@when('я запускаю установку Codev')
def step_install_codev(context):
    """Запустить установку Codev"""
    skeleton_dir = context.project_root / 'codev-skeleton'

    if not skeleton_dir.exists():
        context.installation_failed = True
        context.error_message = f"codev-skeleton not found at {skeleton_dir}"
        return

    try:
        # Копировать структуру из codev-skeleton
        codev_dir = Path(context.test_dir) / 'codev'

        # Создать основную структуру
        for subdir in ['specs', 'plans', 'reviews', 'resources', 'protocols']:
            (codev_dir / subdir).mkdir(parents=True, exist_ok=True)

        # Копировать протоколы
        protocols_src = skeleton_dir / 'protocols'
        protocols_dst = codev_dir / 'protocols'

        if protocols_src.exists():
            for protocol_dir in protocols_src.iterdir():
                if protocol_dir.is_dir():
                    dst = protocols_dst / protocol_dir.name
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(protocol_dir, dst)

        # Создать или обновить CLAUDE.md
        claude_md = Path(context.test_dir) / 'CLAUDE.md'
        if not claude_md.exists():
            claude_template = skeleton_dir / 'CLAUDE.md'
            if claude_template.exists():
                shutil.copy(claude_template, claude_md)
            else:
                # Создать минимальный CLAUDE.md если шаблон не найден
                claude_md.write_text("# Codev Project Instructions\n\nThis is a test project.\n", encoding='utf-8')

        context.installation_failed = False

    except Exception as e:
        context.installation_failed = True
        context.error_message = str(e)


@when('я запускаю обновление Codev')
def step_update_codev(context):
    """Обновить существующую установку Codev"""
    skeleton_dir = context.project_root / 'codev-skeleton'
    codev_dir = Path(context.test_dir) / 'codev'

    try:
        # Обновить только протоколы, сохраняя пользовательские файлы
        protocols_src = skeleton_dir / 'protocols'
        protocols_dst = codev_dir / 'protocols'

        if protocols_src.exists():
            for protocol_dir in protocols_src.iterdir():
                if protocol_dir.is_dir():
                    dst = protocols_dst / protocol_dir.name
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(protocol_dir, dst)

        context.update_failed = False

    except Exception as e:
        context.update_failed = True
        context.error_message = str(e)


@then('создана структура каталогов Codev')
def step_verify_codev_structure(context):
    """Проверить что структура Codev создана"""
    codev_dir = Path(context.test_dir) / 'codev'

    assert codev_dir.exists(), "Директория codev не создана"

    for subdir in ['specs', 'plans', 'reviews', 'resources', 'protocols']:
        subdir_path = codev_dir / subdir
        assert subdir_path.exists(), f"Директория {subdir} не создана"


@then('файл CLAUDE.md содержит инструкции Codev')
def step_verify_claude_md_content(context):
    """Проверить что CLAUDE.md содержит инструкции Codev"""
    claude_md = Path(context.test_dir) / 'CLAUDE.md'

    assert claude_md.exists(), "CLAUDE.md не создан"

    content = claude_md.read_text()
    assert 'Codev' in content or 'codev' in content, \
        "CLAUDE.md не содержит упоминания Codev"


@then('протоколы SPIDER и SPIDER-SOLO доступны')
def step_verify_protocols(context):
    """Проверить наличие протоколов"""
    protocols_dir = Path(context.test_dir) / 'codev' / 'protocols'

    spider_dir = protocols_dir / 'spider'
    spider_solo_dir = protocols_dir / 'spider-solo'

    assert spider_dir.exists(), "Протокол SPIDER не установлен"
    assert spider_solo_dir.exists(), "Протокол SPIDER-SOLO не установлен"

    # Проверить основные файлы протоколов
    assert (spider_dir / 'protocol.md').exists(), "protocol.md SPIDER отсутствует"
    assert (spider_solo_dir / 'protocol.md').exists(), "protocol.md SPIDER-SOLO отсутствует"


@then('содержимое CLAUDE.md сохранено')
def step_verify_claude_md_preserved(context):
    """Проверить что оригинальное содержимое CLAUDE.md сохранено"""
    claude_md = Path(context.test_dir) / 'CLAUDE.md'
    current_content = claude_md.read_text()

    assert context.original_claude_content in current_content, \
        "Оригинальное содержимое CLAUDE.md было изменено"


@then('CLAUDE.md содержит оригинальное содержимое "{content}"')
def step_verify_original_content(context, content):
    """Проверить конкретное оригинальное содержимое"""
    claude_md = Path(context.test_dir) / 'CLAUDE.md'
    current_content = claude_md.read_text()

    assert content in current_content, \
        f"CLAUDE.md не содержит '{content}'"


@then('структура Codev создана корректно')
def step_verify_structure_correct(context):
    """Проверить корректность структуры"""
    step_verify_codev_structure(context)


@then('установлен протокол SPIDER-SOLO')
def step_verify_spider_solo_installed(context):
    """Проверить установку SPIDER-SOLO"""
    protocols_dir = Path(context.test_dir) / 'codev' / 'protocols'
    spider_solo_dir = protocols_dir / 'spider-solo'

    assert spider_solo_dir.exists(), "SPIDER-SOLO не установлен"


@then('файлы протокола SPIDER-SOLO скопированы')
def step_verify_spider_solo_files(context):
    """Проверить наличие всех файлов SPIDER-SOLO"""
    spider_solo_dir = Path(context.test_dir) / 'codev' / 'protocols' / 'spider-solo'

    assert (spider_solo_dir / 'protocol.md').exists()

    templates_dir = spider_solo_dir / 'templates'
    if templates_dir.exists():
        assert (templates_dir / 'spec.md').exists()
        assert (templates_dir / 'plan.md').exists()
        assert (templates_dir / 'review.md').exists()


@then('протокол не требует мультиагентной консультации')
def step_verify_no_multiagent_requirement(context):
    """Проверить что SPIDER-SOLO не требует мультиагентной консультации"""
    protocol_file = Path(context.test_dir) / 'codev' / 'protocols' / 'spider-solo' / 'protocol.md'
    content = protocol_file.read_text()

    # Проверить что упоминается одиночный агент или самопроверка
    assert 'solo' in content.lower() or 'самопроверка' in content.lower() or \
           'single agent' in content.lower()


@then('существует директория "{directory}"')
def step_verify_directory_exists(context, directory):
    """Проверить существование конкретной директории"""
    dir_path = Path(context.test_dir) / directory
    assert dir_path.exists(), f"Директория {directory} не существует"


@then('пользовательские спецификации сохранены')
def step_verify_user_specs_preserved(context):
    """Проверить что пользовательские спецификации не удалены"""
    specs_dir = Path(context.test_dir) / 'codev' / 'specs'
    user_spec = specs_dir / '0001-user-feature.md'

    assert user_spec.exists(), "Пользовательская спецификация удалена"
    assert 'User Feature Spec' in user_spec.read_text()


@then('пользовательские планы сохранены')
def step_verify_user_plans_preserved(context):
    """Проверить что пользовательские планы не удалены"""
    plans_dir = Path(context.test_dir) / 'codev' / 'plans'
    user_plan = plans_dir / '0001-user-feature.md'

    assert user_plan.exists(), "Пользовательский план удалён"
    assert 'User Feature Plan' in user_plan.read_text()


@then('протоколы обновлены до новой версии')
def step_verify_protocols_updated(context):
    """Проверить что протоколы обновлены"""
    protocols_dir = Path(context.test_dir) / 'codev' / 'protocols'

    # Проверить что протоколы существуют (обновление прошло)
    assert (protocols_dir / 'spider' / 'protocol.md').exists()
    assert (protocols_dir / 'spider-solo' / 'protocol.md').exists()


@then('права файла CLAUDE.md остались "{permissions}"')
def step_verify_permissions_preserved(context, permissions):
    """Проверить что права файла сохранены"""
    claude_md = Path(context.test_dir) / 'CLAUDE.md'
    current_perms = oct(os.stat(claude_md).st_mode)[-3:]

    assert current_perms == permissions, \
        f"Права изменились: {permissions} → {current_perms}"


def after_scenario(context, scenario):
    """Очистка после каждого сценария"""
    if hasattr(context, 'test_dir') and os.path.exists(context.test_dir):
        shutil.rmtree(context.test_dir)
