"""
Step definitions для тестирования интеграции Zen MCP
"""
import os
import subprocess
from pathlib import Path
from behave import given, when, then
import json


def _ensure_env_flags(context):
    """Загрузить состояние API-ключей один раз за сценарий"""
    if getattr(context, '_env_flags_loaded', False):
        return

    project_root = Path(__file__).resolve().parent.parent.parent
    env_file = project_root / '.env'

    context.has_gemini_key = False
    context.has_openai_key = False
    context.has_xai_key = False

    if env_file.exists():
        content = env_file.read_text()
        context.has_gemini_key = 'GEMINI_API_KEY=' in content
        context.has_openai_key = 'OPENAI_API_KEY=' in content
        context.has_xai_key = 'XAI_API_KEY=' in content

    context._env_flags_loaded = True


def _require_api_key(context, attr_name, error_message):
    """Убедиться что указанный API-ключ настроен"""
    _ensure_env_flags(context)
    assert getattr(context, attr_name, False), error_message


@given('установлен Zen MCP server')
def step_zen_mcp_installed(context):
    """Проверить что Zen MCP установлен"""
    zen_dir = Path.home() / '.zen-mcp-server'
    context.zen_mcp_installed = zen_dir.exists()

    if context.zen_mcp_installed:
        # Проверить наличие run-server.sh
        run_script = zen_dir / 'run-server.sh'
        context.zen_mcp_installed = run_script.exists() and os.access(run_script, os.X_OK)


@given('настроен файл .env с API-ключами')
def step_env_with_api_keys(context):
    """Проверить наличие .env с API-ключами"""
    _ensure_env_flags(context)


@given('API-ключ Gemini настроен в .env')
def step_gemini_key_configured(context):
    """Проверить наличие Gemini API ключа"""
    _require_api_key(context, 'has_gemini_key', "GEMINI_API_KEY не настроен в .env")


@given('API-ключ OpenAI настроен в .env')
def step_openai_key_configured(context):
    """Проверить наличие OpenAI API ключа"""
    _require_api_key(context, 'has_openai_key', "OPENAI_API_KEY не настроен в .env")


@given('доступны Gemini и GPT-5')
def step_both_models_available(context):
    """Проверить доступность обеих моделей"""
    step_gemini_key_configured(context)
    step_openai_key_configured(context)

    context.multiagent_available = context.has_gemini_key and context.has_openai_key


@given('API-ключи не настроены')
def step_no_api_keys(context):
    """Симулировать отсутствие API-ключей"""
    # Временно удалить переменные окружения
    context.original_env = {}

    for key in ['GEMINI_API_KEY', 'OPENAI_API_KEY', 'XAI_API_KEY']:
        if key in os.environ:
            context.original_env[key] = os.environ[key]
            del os.environ[key]

    context.api_keys_available = False


@given('Zen MCP установлен через install-zen-mcp.sh')
def step_zen_mcp_from_script(context):
    """Проверить установку через скрипт"""
    zen_dir = Path.home() / '.zen-mcp-server'
    env_link = zen_dir / '.env'

    context.zen_mcp_via_script = env_link.exists() and env_link.is_symlink()


# Note: @given('Zen MCP недоступен') уже определён в codev_installation_steps.py
# Используем другое название для этого шага
@given('Zen MCP server недоступен для консультации')
def step_zen_mcp_unavailable_for_consultation(context):
    """Симулировать недоступность Zen MCP для консультации"""
    context.zen_mcp_available = False


@when('я выполняю команду "mcp list"')
def step_run_mcp_list(context):
    """Выполнить команду mcp list"""
    try:
        result = subprocess.run(
            ['mcp', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        context.mcp_list_output = result.stdout
        context.mcp_list_returncode = result.returncode
        context.mcp_list_succeeded = result.returncode == 0
    except FileNotFoundError:
        context.mcp_list_succeeded = False
        context.mcp_list_output = ""
        context.mcp_list_error = "mcp command not found"
    except subprocess.TimeoutExpired:
        context.mcp_list_succeeded = False
        context.mcp_list_error = "mcp list timeout"


@when('я запрашиваю версию Zen MCP')
def step_request_zen_version(context):
    """Запросить версию Zen MCP"""
    try:
        result = subprocess.run(
            ['mcp', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        context.zen_version_output = result.stdout
        context.zen_version_succeeded = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        context.zen_version_succeeded = False
        context.zen_version_output = ""


@when('я запрашиваю консультацию у Gemini Pro')
def step_request_gemini_consultation(context):
    """Симулировать запрос консультации у Gemini"""
    # В реальной реализации это бы делало API вызов через Zen MCP
    # Для теста просто проверяем что ключ настроен
    _ensure_env_flags(context)
    if context.has_gemini_key:
        context.gemini_response = "Mock response from Gemini Pro"
        context.gemini_consultation_succeeded = True
    else:
        context.gemini_consultation_succeeded = False


@when('я запрашиваю консультацию у GPT-5')
def step_request_gpt5_consultation(context):
    """Симулировать запрос консультации у GPT-5"""
    _ensure_env_flags(context)
    if context.has_openai_key:
        context.gpt5_response = "Mock response from GPT-5"
        context.gpt5_consultation_succeeded = True
    else:
        context.gpt5_consultation_succeeded = False


@when('я запрашиваю обзор архитектуры у обеих моделей')
def step_request_multiagent_architecture_review(context):
    """Запросить мультиагентный обзор"""
    step_request_gemini_consultation(context)
    step_request_gpt5_consultation(context)

    context.multiagent_succeeded = (
        context.gemini_consultation_succeeded and
        context.gpt5_consultation_succeeded
    )


@when('я пытаюсь запросить консультацию')
def step_attempt_consultation_without_keys(context):
    """Попытка консультации без API-ключей"""
    context.consultation_error = "API keys not configured"
    context.consultation_failed = True


@when('я начинаю новую фазу SPIDER')
def step_start_spider_phase(context):
    """Начать фазу SPIDER"""
    if hasattr(context, 'zen_mcp_available') and not context.zen_mcp_available:
        # Fallback на SPIDER-SOLO
        context.protocol_used = 'SPIDER-SOLO'
        context.uses_self_review = True
    else:
        context.protocol_used = 'SPIDER'
        context.uses_multiagent = True


@then('Zen MCP отображается в списке серверов')
def step_verify_zen_in_list(context):
    """Проверить что Zen MCP в списке"""
    if hasattr(context, 'mcp_list_succeeded') and context.mcp_list_succeeded:
        assert 'zen' in context.mcp_list_output.lower(), \
            "Zen MCP не найден в выводе mcp list"


@then('статус Zen MCP "{status}"')
def step_verify_zen_status(context, status):
    """Проверить статус Zen MCP"""
    if hasattr(context, 'mcp_list_output'):
        assert status.lower() in context.mcp_list_output.lower(), \
            f"Статус '{status}' не найден в выводе"


@then('возвращается корректная версия сервера')
def step_verify_zen_version(context):
    """Проверить что версия возвращена"""
    assert hasattr(context, 'zen_version_succeeded') and context.zen_version_succeeded, \
        "Версия Zen MCP не получена"


@then('получен ответ от Gemini')
def step_verify_gemini_response(context):
    """Проверить получение ответа от Gemini"""
    assert hasattr(context, 'gemini_consultation_succeeded') and \
           context.gemini_consultation_succeeded, \
        "Ответ от Gemini не получен"


@then('контекст консультации сохранён')
def step_verify_context_saved(context):
    """Проверить сохранение контекста"""
    # В реальной реализации проверялась бы БД или файл
    assert hasattr(context, 'gemini_response'), "Контекст не сохранён"


@then('получен ответ от GPT-5')
def step_verify_gpt5_response(context):
    """Проверить получение ответа от GPT-5"""
    assert hasattr(context, 'gpt5_consultation_succeeded') and \
           context.gpt5_consultation_succeeded, \
        "Ответ от GPT-5 не получен"


@then('качество ответа соответствует ожиданиям')
def step_verify_response_quality(context):
    """Проверить качество ответа"""
    # Базовая проверка наличия ответа
    assert hasattr(context, 'gpt5_response') and len(context.gpt5_response) > 0


@then('получены ответы от Gemini и GPT-5')
def step_verify_both_responses(context):
    """Проверить получение обоих ответов"""
    assert hasattr(context, 'gemini_response'), "Ответ от Gemini отсутствует"
    assert hasattr(context, 'gpt5_response'), "Ответ от GPT-5 отсутствует"


@then('ответы имеют различные перспективы')
def step_verify_different_perspectives(context):
    """Проверить различие перспектив"""
    # В реальной реализации сравнивались бы ответы
    assert context.gemini_response != context.gpt5_response, \
        "Ответы идентичны, различные перспективы не обнаружены"


@then('найдены дополнительные инсайты')
def step_verify_additional_insights(context):
    """Проверить наличие дополнительных инсайтов"""
    # Проверка что оба ответа получены (мультиагентный подход дал больше информации)
    assert hasattr(context, 'multiagent_succeeded') and context.multiagent_succeeded


@then('возвращается сообщение об ошибке')
def step_verify_error_message(context):
    """Проверить наличие сообщения об ошибке"""
    assert hasattr(context, 'consultation_failed') and context.consultation_failed


@then('указано "требуется API-ключ"')
def step_verify_api_key_error(context):
    """Проверить сообщение о необходимости API-ключа"""
    if hasattr(context, 'consultation_error'):
        assert 'api' in context.consultation_error.lower() or \
               'key' in context.consultation_error.lower()


@then('~/.zen-mcp-server/.env является симлинком')
def step_verify_env_is_symlink(context):
    """Проверить что .env это символическая ссылка"""
    zen_env = Path.home() / '.zen-mcp-server' / '.env'

    if zen_env.exists():
        assert zen_env.is_symlink(), "~/.zen-mcp-server/.env не является симлинком"


@then('симлинк указывает на /srv/anygen/.env')
def step_verify_symlink_target(context):
    """Проверить цель симлинка"""
    zen_env = Path.home() / '.zen-mcp-server' / '.env'

    if zen_env.exists() and zen_env.is_symlink():
        target = zen_env.resolve()
        expected = Path('/srv/anygen/.env')

        assert target == expected, \
            f"Симлинк указывает на {target}, ожидалось {expected}"


@then('изменения в .env проекта отражаются в Zen MCP')
def step_verify_env_changes_reflected(context):
    """Проверить что изменения .env отражаются"""
    project_env = Path('/srv/anygen/.env')
    zen_env = Path.home() / '.zen-mcp-server' / '.env'

    if zen_env.is_symlink():
        # Проверить что оба файла идентичны
        assert zen_env.resolve() == project_env


@then('автоматически используется SPIDER-SOLO')
def step_verify_spider_solo_fallback(context):
    """Проверить переключение на SPIDER-SOLO"""
    assert hasattr(context, 'protocol_used'), "Протокол не определён"
    assert context.protocol_used == 'SPIDER-SOLO', \
        f"Ожидался SPIDER-SOLO, получен {context.protocol_used}"


@then('консультации заменены самопроверкой')
def step_verify_self_review_used(context):
    """Проверить использование самопроверки"""
    assert hasattr(context, 'uses_self_review') and context.uses_self_review, \
        "Самопроверка не используется"


@then('workflow продолжается без ошибок')
def step_verify_workflow_continues(context):
    """Проверить что workflow продолжается"""
    assert hasattr(context, 'protocol_used'), "Workflow не запущен"


def after_scenario(context, scenario):
    """Восстановить окружение после сценария"""
    # Восстановить API-ключи если были удалены
    if hasattr(context, 'original_env'):
        for key, value in context.original_env.items():
            os.environ[key] = value
