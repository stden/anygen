#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# Zen MCP Server Installation Script для AnyGen
#
# Устанавливает Zen MCP server для мультиагентной консультации в Codev
# ============================================================================

# Цвета для вывода
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly RED='\033[0;31m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Конфигурация
readonly ZEN_INSTALL_DIR="${HOME}/.zen-mcp-server"
readonly ZEN_REPO="https://github.com/BeehiveInnovations/zen-mcp-server.git"
readonly REQUIRED_PYTHON_VERSION="3.10"

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
# Проверка предварительных условий
# ----------------------------------------------------------------------------

check_python() {
    print_info "Проверка версии Python..."

    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 не установлен"
        echo "Установите Python 3.10+ перед продолжением:"
        echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
        echo "  macOS: brew install python@3.10"
        exit 1
    fi

    local python_version
    python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)

    if (( $(echo "$python_version < $REQUIRED_PYTHON_VERSION" | bc -l) )); then
        print_error "Python версия $python_version < $REQUIRED_PYTHON_VERSION"
        exit 1
    fi

    print_success "Python $python_version найден"
}

check_git() {
    print_info "Проверка Git..."

    if ! command -v git &> /dev/null; then
        print_error "Git не установлен"
        echo "Установите Git: sudo apt install git"
        exit 1
    fi

    print_success "Git найден"
}

# ----------------------------------------------------------------------------
# Установка Zen MCP
# ----------------------------------------------------------------------------

install_zen_mcp() {
    print_header "Установка Zen MCP Server"

    # Удалить старую версию если есть
    if [[ -d "$ZEN_INSTALL_DIR" ]]; then
        print_warning "Найдена существующая установка в $ZEN_INSTALL_DIR"
        read -p "Удалить и переустановить? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$ZEN_INSTALL_DIR"
            print_success "Старая версия удалена"
        else
            print_info "Обновление существующей установки..."
            cd "$ZEN_INSTALL_DIR"
            git pull origin main
            return 0
        fi
    fi

    # Клонировать репозиторий
    print_info "Клонирование репозитория..."
    git clone "$ZEN_REPO" "$ZEN_INSTALL_DIR"
    print_success "Репозиторий склонирован в $ZEN_INSTALL_DIR"

    cd "$ZEN_INSTALL_DIR"

    # Создать виртуальное окружение
    print_info "Создание виртуального окружения..."
    python3 -m venv .zen_venv
    print_success "Виртуальное окружение создано"

    # Активировать venv и установить зависимости
    print_info "Установка зависимостей..."
    source .zen_venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Зависимости установлены"
}

# ----------------------------------------------------------------------------
# Настройка переменных окружения
# ----------------------------------------------------------------------------

configure_env() {
    print_header "Настройка переменных окружения"

    local zen_env="$ZEN_INSTALL_DIR/.env"
    local project_env="${PROJECT_ROOT:-.}/.env"

    # Создать симлинк на .env проекта
    if [[ -f "$project_env" ]]; then
        print_info "Используется .env из проекта: $project_env"

        # Удалить старый .env если есть
        if [[ -f "$zen_env" || -L "$zen_env" ]]; then
            rm "$zen_env"
        fi

        # Создать символическую ссылку
        ln -s "$project_env" "$zen_env"
        print_success "Создана символическая ссылка: $zen_env -> $project_env"

        # Проверить наличие необходимых переменных
        echo ""
        print_info "Проверка наличия API-ключей в $project_env..."

        local has_keys=false
        if grep -q "^GEMINI_API_KEY=" "$project_env" 2>/dev/null; then
            print_success "GEMINI_API_KEY найден"
            has_keys=true
        fi

        if grep -q "^OPENAI_API_KEY=" "$project_env" 2>/dev/null; then
            print_success "OPENAI_API_KEY найден"
            has_keys=true
        fi

        if grep -q "^XAI_API_KEY=" "$project_env" 2>/dev/null; then
            print_success "XAI_API_KEY найден"
            has_keys=true
        fi

        if [[ "$has_keys" == "false" ]]; then
            echo ""
            print_warning "API-ключи для Zen MCP не найдены в .env"
            echo ""
            echo "Добавьте следующие переменные в $project_env:"
            echo ""
            echo "# Zen MCP API Keys"
            echo "GEMINI_API_KEY=your_gemini_api_key_here    # https://makersuite.google.com/app/apikey"
            echo "OPENAI_API_KEY=your_openai_api_key_here    # https://platform.openai.com/api-keys"
            echo "XAI_API_KEY=your_xai_api_key_here          # https://console.x.ai/"
            echo ""
            print_warning "ВАЖНО: Хотя бы один API-ключ ОБЯЗАТЕЛЕН для работы Zen MCP"
            echo ""
        fi
    else
        print_warning "Файл $project_env не найден"
        print_info "Создание локального .env для Zen MCP"

        # Копировать пример
        cp "$ZEN_INSTALL_DIR/.env.example" "$zen_env"
        print_success ".env файл создан: $zen_env"

        echo ""
        print_info "Для работы Zen MCP нужны API-ключи:"
        echo ""
        echo "  1. Gemini API Key - https://makersuite.google.com/app/apikey"
        echo "  2. OpenAI API Key - https://platform.openai.com/api-keys (опционально)"
        echo "  3. XAI API Key - https://console.x.ai/ (опционально)"
        echo ""
        print_warning "ВАЖНО: Хотя бы один API-ключ ОБЯЗАТЕЛЕН"
        echo ""
        print_info "Отредактируйте: $zen_env"
    fi
}

# ----------------------------------------------------------------------------
# Настройка Claude MCP Config
# ----------------------------------------------------------------------------

configure_claude() {
    print_header "Настройка Claude MCP Config"

    local claude_config="${HOME}/.claude/mcp_config.json"
    local claude_dir
    claude_dir=$(dirname "$claude_config")

    # Создать директорию если нет
    if [[ ! -d "$claude_dir" ]]; then
        mkdir -p "$claude_dir"
        print_success "Создана директория $claude_dir"
    fi

    # Проверить существующий конфиг
    if [[ -f "$claude_config" ]]; then
        print_warning "Claude MCP config уже существует: $claude_config"
        read -p "Создать резервную копию и обновить? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cp "$claude_config" "${claude_config}.backup.$(date +%Y%m%d_%H%M%S)"
            print_success "Резервная копия создана"
        else
            print_info "Добавьте Zen MCP вручную в $claude_config"
            show_manual_config
            return 0
        fi
    fi

    # Создать новый конфиг
    cat > "$claude_config" << EOF
{
  "mcpServers": {
    "zen": {
      "command": "bash",
      "args": [
        "${ZEN_INSTALL_DIR}/run-server.sh"
      ],
      "env": {
        "PYTHONPATH": "${ZEN_INSTALL_DIR}"
      }
    }
  }
}
EOF

    print_success "Claude MCP config настроен: $claude_config"
}

show_manual_config() {
    echo ""
    print_info "Добавьте в ~/.claude/mcp_config.json:"
    echo ""
    cat << EOF
{
  "mcpServers": {
    "zen": {
      "command": "bash",
      "args": [
        "${ZEN_INSTALL_DIR}/run-server.sh"
      ],
      "env": {
        "PYTHONPATH": "${ZEN_INSTALL_DIR}"
      }
    }
  }
}
EOF
    echo ""
}

# ----------------------------------------------------------------------------
# Тестирование установки
# ----------------------------------------------------------------------------

test_installation() {
    print_header "Тестирование установки"

    print_info "Активация виртуального окружения..."
    cd "$ZEN_INSTALL_DIR"
    source .zen_venv/bin/activate

    print_info "Запуск тестового вызова..."

    # Проверить импорт
    if python3 -c "import sys; sys.path.insert(0, '$ZEN_INSTALL_DIR'); import server" 2>/dev/null; then
        print_success "Python модули загружаются корректно"
    else
        print_error "Ошибка импорта модулей"
        echo "Проверьте логи для деталей"
        return 1
    fi

    print_success "Базовая проверка пройдена"

    print_warning "Для полного теста запустите сервер и проверьте в Claude:"
    echo "  mcp__zen__version"
    echo ""
}

# ----------------------------------------------------------------------------
# Инструкции по использованию
# ----------------------------------------------------------------------------

show_usage_instructions() {
    print_header "Установка завершена!"

    echo ""
    echo "📋 Следующие шаги:"
    echo ""
    echo "1. Настройте API-ключи в .env:"
    echo "   ${EDITOR:-nano} ${ZEN_INSTALL_DIR}/.env"
    echo ""
    echo "2. Перезапустите Claude Code для загрузки MCP конфига"
    echo ""
    echo "3. Проверьте работу в Claude:"
    echo "   mcp__zen__version"
    echo ""
    echo "4. Используйте мультиагентную консультацию:"
    echo "   \"Consult Gemini Pro about this architecture\""
    echo "   \"Ask GPT-5 to review this code\""
    echo ""
    echo "📁 Установлено в: $ZEN_INSTALL_DIR"
    echo "📝 Конфиг Claude: ~/.claude/mcp_config.json"
    echo "🔑 API ключи: ${ZEN_INSTALL_DIR}/.env"
    echo ""
    print_success "Zen MCP готов к использованию!"
    echo ""
}

# ----------------------------------------------------------------------------
# Главная функция
# ----------------------------------------------------------------------------

main() {
    print_header "Установка Zen MCP Server для AnyGen"

    # Проверки
    check_python
    check_git

    # Установка
    install_zen_mcp
    configure_env
    configure_claude

    # Тестирование
    test_installation

    # Инструкции
    show_usage_instructions
}

# Запуск
main "$@"
