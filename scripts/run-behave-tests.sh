#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# Behave BDD Tests Runner для Codev
#
# Запускает BDD-тесты с использованием behave и uv
# ============================================================================

# Цвета для вывода
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly RED='\033[0;31m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Директории
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ----------------------------------------------------------------------------
# Утилиты вывода
# ----------------------------------------------------------------------------

print_success() {
    echo -e "${GREEN}✓${NC} $1" >&2
}

print_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1" >&2
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1" >&2
}

print_header() {
    echo ""
    echo -e "${BLUE}=====================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=====================================${NC}"
    echo ""
}

# ----------------------------------------------------------------------------
# Проверка зависимостей
# ----------------------------------------------------------------------------

check_uv() {
    if ! command -v uv &> /dev/null; then
        print_error "uv не установлен"
        echo "Установите uv:"
        echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
    print_success "uv найден: $(uv --version)"
}

check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 не установлен"
        exit 1
    fi

    local python_version
    python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)

    print_success "Python найден: $(python3 --version)"
}

# ----------------------------------------------------------------------------
# Установка зависимостей
# ----------------------------------------------------------------------------

install_dependencies() {
    print_header "Установка зависимостей"

    cd "$PROJECT_ROOT"

    # Установить зависимости через uv
    print_info "Установка зависимостей через uv..."

    uv pip install -e ".[dev]"

    print_success "Зависимости установлены"
}

# ----------------------------------------------------------------------------
# Запуск тестов
# ----------------------------------------------------------------------------

run_behave_tests() {
    print_header "Запуск BDD тестов с behave"

    cd "$PROJECT_ROOT"

    # Параметры behave
    local behave_args=(
        "features"               # Путь к директории с тестами
        "--no-capture"           # Показывать print() во время тестов
        "--no-capture-stderr"    # Показывать stderr
        "--format=progress"      # Прогресс-бар
        "--format=pretty"        # Красивый вывод
        "--color"                # Цветной вывод
        "--lang=ru"              # Русский язык
    )

    # Добавить дополнительные аргументы из командной строки
    if [[ $# -gt 0 ]]; then
        behave_args+=("$@")
    fi

    # Запустить behave
    print_info "Запуск: uv run behave ${behave_args[*]}"
    echo ""

    if uv run behave "${behave_args[@]}"; then
        echo ""
        print_success "Все тесты пройдены!"
        return 0
    else
        echo ""
        print_error "Некоторые тесты не прошли"
        return 1
    fi
}

# ----------------------------------------------------------------------------
# Генерация отчёта покрытия
# ----------------------------------------------------------------------------

generate_coverage_report() {
    print_header "Генерация отчёта покрытия"

    cd "$PROJECT_ROOT"

    # Запустить тесты с coverage
    uv run coverage run -m behave features

    # Сгенерировать отчёты
    uv run coverage report
    uv run coverage html

    print_success "HTML отчёт создан: htmlcov/index.html"
}

# ----------------------------------------------------------------------------
# Справка
# ----------------------------------------------------------------------------

show_usage() {
    cat << EOF
Использование: $0 [опции]

Опции:
  -h, --help              Показать эту справку
  -i, --install           Установить зависимости
  -c, --coverage          Запустить с генерацией отчёта покрытия
  -t, --tags TAGS         Запустить только тесты с указанными тегами
  -f, --feature FEATURE   Запустить конкретный feature файл
  -v, --verbose           Подробный вывод

Примеры:
  $0                                    # Запустить все тесты
  $0 --install                          # Установить зависимости и запустить
  $0 --coverage                         # С отчётом покрытия
  $0 --feature codev_installation       # Только установка
  $0 --tags @smoke                      # Только smoke тесты
  $0 --verbose                          # Подробный вывод

EOF
}

# ----------------------------------------------------------------------------
# Главная функция
# ----------------------------------------------------------------------------

main() {
    local install_deps=false
    local run_coverage=false
    local behave_extra_args=()

    # Парсинг аргументов
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -i|--install)
                install_deps=true
                shift
                ;;
            -c|--coverage)
                run_coverage=true
                shift
                ;;
            -t|--tags)
                behave_extra_args+=("--tags=$2")
                shift 2
                ;;
            -f|--feature)
                behave_extra_args+=("--name=$2")
                shift 2
                ;;
            -v|--verbose)
                behave_extra_args+=("--verbose")
                shift
                ;;
            *)
                print_error "Неизвестная опция: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    print_header "Codev BDD Tests Runner"

    # Проверки
    check_python
    check_uv

    # Установка зависимостей если нужно
    if [[ "$install_deps" == "true" ]]; then
        install_dependencies
    fi

    # Запуск тестов
    if [[ "$run_coverage" == "true" ]]; then
        generate_coverage_report
    else
        run_behave_tests "${behave_extra_args[@]}"
    fi
}

# Запуск
main "$@"
