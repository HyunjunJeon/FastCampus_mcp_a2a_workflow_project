#!/bin/bash

# FastCampus Multi-Agent Workflow Automation Docker Runner
# Bash script for Unix/Linux/macOS environments

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project constants
COMPOSE_FILE="docker-compose-full.yml"
ENV_FILE=".env"
ENV_EXAMPLE=".env.example"
PROJECT_NAME="fastcampus-workflow-automation"

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to print usage information
print_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       Start all services (default)"
    echo "  stop        Stop all services"
    echo "  restart     Restart all services"
    echo "  logs        Show logs from all services"
    echo "  status      Show status of all services"
    echo "  clean       Stop and remove all containers, networks, and volumes"
    echo "  build       Build all services"
    echo "  mcp-only    Start only MCP servers (notion-mcp, openmemory-mcp, mem0-store, langchain-sandbox-mcp, playwright-mcp)"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run-docker.sh start"
    echo "  ./run-docker.sh logs"
    echo "  ./run-docker.sh clean"
    echo "  ./run-docker.sh mcp-only"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Docker installation and status
check_docker() {
    print_info "Checking Docker installation..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed or not in PATH"
        print_info "Please install Docker from: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker daemon is not running"
        print_info "Please start Docker and try again"
        exit 1
    fi
    
    if ! command_exists docker-compose && ! docker compose version >/dev/null 2>&1; then
        print_error "Docker Compose is not available"
        print_info "Please install Docker Compose or upgrade to Docker with built-in compose"
        exit 1
    fi
    
    print_success "Docker is installed and running"
}

# Function to check if docker-compose-full.yml exists
check_compose_file() {
    if [[ ! -f "$COMPOSE_FILE" ]]; then
        print_error "Docker compose file '$COMPOSE_FILE' not found"
        print_info "Please ensure you are in the correct project directory"
        exit 1
    fi
    print_success "Docker compose file found"
}

# Function to setup .env file
setup_env_file() {
    print_info "Checking environment configuration..."
    
    if [[ ! -f "$ENV_FILE" ]]; then
        if [[ -f "$ENV_EXAMPLE" ]]; then
            print_warning ".env file not found, creating from .env.example"
            cp "$ENV_EXAMPLE" "$ENV_FILE"
            print_success ".env file created from template"
            print_warning "Please edit .env file and add your API keys before running the services"
        else
            print_error "Neither .env nor .env.example file found"
            exit 1
        fi
    else
        print_success ".env file found"
    fi
}

# Function to validate essential environment variables
validate_env_vars() {
    print_info "Validating essential environment variables..."
    
    if [[ ! -f "$ENV_FILE" ]]; then
        print_error ".env file not found"
        return 1
    fi
    
    # Source the .env file
    source "$ENV_FILE"
    
    # List of critical environment variables
    critical_vars=("OPENAI_API_KEY" "USER")
    missing_vars=()
    
    for var in "${critical_vars[@]}"; do
        if [[ -z "${!var}" ]]; then
            missing_vars+=("$var")
        fi
    done
    
    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        print_error "The following critical environment variables are missing or empty:"
        for var in "${missing_vars[@]}"; do
            echo "  - $var"
        done
        print_info "Please edit the .env file and set these variables"
        return 1
    fi
    
    print_success "Essential environment variables are set"
    return 0
}

# Function to get Docker Compose command
get_compose_command() {
    if command_exists docker-compose; then
        echo "docker-compose"
    else
        echo "docker compose"
    fi
}

# Function to start services
start_services() {
    print_info "Starting all services..."
    
    # First, stop any existing containers to ensure clean start
    local compose_cmd
    compose_cmd=$(get_compose_command)
    
    print_info "Stopping any existing Docker containers for clean start..."
    $compose_cmd -f "$COMPOSE_FILE" --project-name "$PROJECT_NAME" down
    
    # Start Playwright MCP server
    print_info "Starting Playwright MCP server..."
    start_playwright_mcp
    
    print_info "Starting Docker containers..."
    $compose_cmd -f "$COMPOSE_FILE" --project-name "$PROJECT_NAME" up -d
    
    if [[ $? -eq 0 ]]; then
        print_success "Docker services started successfully"
        
        # Check if Playwright MCP is still running
        if check_playwright_mcp; then
            print_success "All services (including Playwright MCP) are running"
        else
            print_warning "Docker services started, but Playwright MCP is not running"
            print_info "Some browser-related functionality may not work properly"
        fi
        
        print_info "Services are now running in the background"
        print_info "You can check logs with: $0 logs"
        print_info "You can check status with: $0 status"
    else
        print_error "Failed to start Docker services"
        exit 1
    fi
}

# Function to start only MCP services
start_mcp_services() {
    print_info "Starting MCP services only..."
    
    local compose_cmd
    compose_cmd=$(get_compose_command)
    
    # First, stop any existing MCP containers for clean start
    print_info "Stopping any existing MCP containers for clean start..."
    local mcp_services=("mem0-store" "notion-mcp" "openmemory-mcp" "langchain-sandbox-mcp")
    $compose_cmd -f "$COMPOSE_FILE" --project-name "$PROJECT_NAME" stop "${mcp_services[@]}"
    $compose_cmd -f "$COMPOSE_FILE" --project-name "$PROJECT_NAME" rm -f "${mcp_services[@]}"
    
    # Start Playwright MCP server
    print_info "Starting Playwright MCP server..."
    start_playwright_mcp
    
    print_info "Starting Docker MCP containers..."
    $compose_cmd -f "$COMPOSE_FILE" --project-name "$PROJECT_NAME" up -d "${mcp_services[@]}"
    
    if [[ $? -eq 0 ]]; then
        print_success "Docker MCP services started successfully"
        
        # Check overall status
        local all_running=true
        if ! check_playwright_mcp; then
            print_warning "Playwright MCP server is not running"
            all_running=false
        fi
        
        if [[ "$all_running" == true ]]; then
            print_success "All MCP services are running"
        else
            print_warning "Some MCP services may not be fully operational"
        fi
        
        print_info "MCP services status:"
        print_info "  - Notion MCP: http://localhost:8930"
        print_info "  - OpenMemory MCP: http://localhost:8031"
        print_info "  - Qdrant (Mem0 Store): http://localhost:6333"
        print_info "  - LangChain Sandbox MCP: http://localhost:8035"
        
        if check_playwright_mcp; then
            print_info "  - Playwright MCP: http://localhost:8931 ✓"
        else
            print_info "  - Playwright MCP: Not running ✗"
        fi
        
        print_info "You can check logs with: $0 logs"
        print_info "You can check status with: $0 status"
    else
        print_error "Failed to start Docker MCP services"
        exit 1
    fi
}

# Function to stop services
stop_services() {
    print_info "Stopping all services..."
    
    local compose_cmd
    compose_cmd=$(get_compose_command)
    
    print_info "Stopping Docker containers..."
    $compose_cmd -f "$COMPOSE_FILE" --project-name "$PROJECT_NAME" down
    
    local docker_stopped=false
    if [[ $? -eq 0 ]]; then
        print_success "Docker services stopped successfully"
        docker_stopped=true
    else
        print_error "Failed to stop Docker services"
    fi
    
    # Stop Playwright MCP server
    print_info "Stopping Playwright MCP server..."
    stop_playwright_mcp
    
    if [[ "$docker_stopped" == true ]]; then
        print_success "All services stopped successfully"
    else
        print_error "Some services failed to stop properly"
        exit 1
    fi
}

# Function to restart services
restart_services() {
    print_info "Restarting all services..."
    stop_services
    start_services
}

# Function to show logs
show_logs() {
    print_info "Showing logs from all services..."
    
    local compose_cmd
    compose_cmd=$(get_compose_command)
    
    $compose_cmd -f "$COMPOSE_FILE" --project-name "$PROJECT_NAME" logs -f
}

# Function to check HTTP service availability
check_http_service() {
    local url="$1"
    local timeout="${2:-2}"
    
    if command -v curl >/dev/null 2>&1; then
        curl -s --connect-timeout "$timeout" "$url" >/dev/null 2>&1
        return $?
    else
        return 1
    fi
}

# Function to show status
show_status() {
    print_info "Showing status of all services..."
    
    local compose_cmd
    compose_cmd=$(get_compose_command)
    
    print_info "Docker containers status:"
    $compose_cmd -f "$COMPOSE_FILE" --project-name "$PROJECT_NAME" ps
    
    echo ""
    print_info "MCP Services detailed status:"
    
    # Check Playwright MCP
    if check_playwright_mcp; then
        if check_http_service "http://localhost:8931" 2; then
            print_success "  ✓ Playwright MCP: Running and responding (http://localhost:8931)"
        else
            print_warning "  ~ Playwright MCP: Running but not responding properly"
        fi
    else
        print_error "  ✗ Playwright MCP: Not running"
        print_info "    Start with: npx @playwright/mcp@latest --port 8931"
    fi
    
    # Check Notion MCP
    if check_http_service "http://localhost:8930" 3; then
        print_success "  ✓ Notion MCP: Running and responding (http://localhost:8930)"
    else
        print_warning "  ~ Notion MCP: Container running but service may not be ready"
    fi
    
    # Check OpenMemory MCP
    if check_http_service "http://localhost:8031" 3; then
        print_success "  ✓ OpenMemory MCP: Running and responding (http://localhost:8031)"
    else
        print_warning "  ~ OpenMemory MCP: Container running but service may not be ready"
    fi

    # Check Qdrant (Mem0 Store)
    if check_http_service "http://localhost:6333" 2; then
        print_success "  ✓ Qdrant (Mem0 Store): Running and responding (http://localhost:6333)"
    else
        print_warning "  ~ Qdrant (Mem0 Store): Container running but service may not be ready"
    fi

    # Check LangChain Sandbox MCP
    if check_http_service "http://localhost:8035" 3; then
        print_success "  ✓ LangChain Sandbox MCP: Running and responding (http://localhost:8035)"
    else
        print_warning "  ~ LangChain Sandbox MCP: Container running but service may not be ready"
    fi

    echo ""
    print_info "Service URLs for Docker containers:"
    print_info "  - Notion MCP: http://notion-mcp:3000/mcp"
    print_info "  - OpenMemory MCP: http://openmemory-mcp:8031/mcp"
    print_info "  - LangChain Sandbox MCP: http://langchain-sandbox-mcp:8035/mcp"
    print_info "  - Playwright MCP: http://host.docker.internal:8931/mcp"
    
    echo ""
    print_info "For more detailed logs, use: $0 logs"
}

# Function to clean up everything
clean_services() {
    print_warning "This will stop and remove all containers, networks, and volumes"
    read -p "Are you sure? (y/N): " -r
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Cleaning up all services and data..."
        
        local compose_cmd
        compose_cmd=$(get_compose_command)
        
        $compose_cmd -f "$COMPOSE_FILE" --project-name "$PROJECT_NAME" down -v --remove-orphans
        
        # Remove any dangling volumes
        docker volume prune -f
        
        print_success "Cleanup completed"
    else
        print_info "Cleanup cancelled"
    fi
}

# Function to check if Node.js is installed
check_nodejs() {
    if ! command_exists node; then
        print_warning "Node.js is not installed"
        print_info "Please install Node.js from: https://nodejs.org/"
        return 1
    fi
    
    if ! command_exists npx; then
        print_warning "npx is not available"
        print_info "Please install a newer version of Node.js"
        return 1
    fi
    
    return 0
}

# Function to start Playwright MCP server
start_playwright_mcp() {
    print_info "Starting Playwright MCP server..."
    
    # Check Node.js prerequisites
    if ! check_nodejs; then
        print_warning "Playwright MCP server cannot be started due to Node.js requirements"
        return 1
    fi
    
    # Check if already running
    if lsof -i :8931 >/dev/null 2>&1; then
        print_success "Playwright MCP server is already running on port 8931"
        return 0
    fi
    
    # Start the server in background
    nohup npx @playwright/mcp@latest --port 8931 > /tmp/playwright-mcp.log 2>&1 &
    
    # Save PID
    echo $! > /tmp/playwright-mcp.pid
    
    # Wait a moment for server to start
    sleep 3
    
    # Check if server is running
    if lsof -i :8931 >/dev/null 2>&1; then
        print_success "Playwright MCP server started successfully on port 8931"
        print_info "Server can be accessed via: http://localhost:8931"
        print_info "Docker containers access via: host.docker.internal:8931"
        return 0
    else
        print_warning "Playwright MCP server failed to start"
        print_info "Check logs: /tmp/playwright-mcp.log"
        return 1
    fi
}

# Function to stop Playwright MCP server
stop_playwright_mcp() {
    print_info "Stopping Playwright MCP server..."
    
    local stopped=false
    
    # Stop using PID file if available
    if [[ -f /tmp/playwright-mcp.pid ]]; then
        local pid=$(cat /tmp/playwright-mcp.pid)
        if kill "$pid" 2>/dev/null; then
            print_success "Playwright MCP server stopped (PID: $pid)"
            stopped=true
        fi
        rm -f /tmp/playwright-mcp.pid
    fi
    
    # Force kill any remaining processes on port 8931
    local port_pid
    port_pid=$(lsof -ti :8931 2>/dev/null)
    if [[ -n "$port_pid" ]]; then
        kill -9 "$port_pid" 2>/dev/null
        print_info "Killed remaining process on port 8931"
        stopped=true
    fi
    
    if [[ "$stopped" == true ]]; then
        print_success "Playwright MCP server stopped"
    else
        print_info "Playwright MCP server was not running"
    fi
}

# Function to check Playwright MCP server status
check_playwright_mcp() {
    if lsof -i :8931 >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to build services
build_services() {
    print_info "Building all services..."
    
    local compose_cmd
    compose_cmd=$(get_compose_command)
    
    $compose_cmd -f "$COMPOSE_FILE" --project-name "$PROJECT_NAME" build
    
    if [[ $? -eq 0 ]]; then
        print_success "All services built successfully"
    else
        print_error "Failed to build services"
        exit 1
    fi
}

# Main execution
main() {
    # Parse command line arguments
    COMMAND=${1:-start}
    
    case $COMMAND in
        help|--help|-h)
            print_usage
            exit 0
            ;;
        start|stop|restart|logs|status|clean|build|mcp-only)
            ;;
        *)
            print_error "Unknown command: $COMMAND"
            print_usage
            exit 1
            ;;
    esac
    
    # Pre-flight checks
    check_docker
    check_compose_file
    setup_env_file
    
    # Validate environment for start/restart commands
    if [[ "$COMMAND" == "start" ]] || [[ "$COMMAND" == "restart" ]]; then
        if ! validate_env_vars; then
            print_error "Environment validation failed. Please fix the issues above."
            exit 1
        fi
    fi
    
    # Execute the requested command
    case $COMMAND in
        start)
            start_services
            ;;
        stop)
            stop_services
            ;;
        restart)
            restart_services
            ;;
        logs)
            show_logs
            ;;
        status)
            show_status
            ;;
        clean)
            clean_services
            ;;
        build)
            build_services
            ;;
        mcp-only)
            start_mcp_services
            ;;
    esac
}

# Run main function
main "$@"