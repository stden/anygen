"""
Behave environment configuration для Codev тестов
"""
import os
import sys
from pathlib import Path


def before_all(context):
    """Настройка перед всеми тестами"""
    # Добавить project root в PYTHONPATH
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    # Сохранить оригинальные переменные окружения
    context.original_env = dict(os.environ)

    # Установить тестовое окружение
    context.project_root = project_root
    context.test_mode = True

    print(f"\n🧪 Starting Codev BDD tests")
    print(f"📁 Project root: {project_root}")
    print(f"🐍 Python: {sys.version}")


def after_all(context):
    """Очистка после всех тестов"""
    # Восстановить оригинальное окружение
    os.environ.clear()
    os.environ.update(context.original_env)

    print(f"\n✅ Codev BDD tests completed")


def before_scenario(context, scenario):
    """Настройка перед каждым сценарием"""
    # Сброс состояния контекста
    context.test_dir = None
    context.installation_failed = False
    context.error_message = None


def after_scenario(context, scenario):
    """Очистка после каждого сценария"""
    # Вызов cleanup функций из steps если они определены
    if hasattr(context, 'cleanup_functions'):
        for cleanup_fn in context.cleanup_functions:
            try:
                cleanup_fn(context)
            except Exception as e:
                print(f"⚠️  Cleanup error: {e}")


def before_feature(context, feature):
    """Настройка перед каждым feature файлом"""
    print(f"\n📝 Feature: {feature.name}")


def after_feature(context, feature):
    """Очистка после каждого feature файла"""
    pass


def before_step(context, step):
    """Настройка перед каждым шагом (опционально)"""
    pass


def after_step(context, step):
    """Очистка после каждого шага"""
    if step.status == 'failed':
        # Вывести дополнительную информацию при ошибке
        if hasattr(context, 'error_message') and context.error_message:
            print(f"   💥 Error: {context.error_message}")
