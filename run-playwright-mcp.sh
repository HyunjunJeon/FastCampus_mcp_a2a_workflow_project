#!/bin/bash

# Playwright MCP Server 실행 스크립트
# FastCampus Multi-Agent Workflow Automation

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
    echo "  start       Start Playwright MCP server (default)"
    echo "  stop        Stop Playwright MCP server"
    echo "  status      Check if Playwright MCP server is running"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run-playwright-mcp.sh start"
    echo "  ./run-playwright-mcp.sh status"
    echo "  ./run-playwright-mcp.sh stop"
}

# Function to check if Node.js is installed
check_nodejs() {
    if ! command -v node >/dev/null 2>&1; then
        print_error "Node.js is not installed"
        print_info "Please install Node.js from: https://nodejs.org/"
        exit 1
    fi
    
    if ! command -v npx >/dev/null 2>&1; then
        print_error "npx is not available"
        print_info "Please install a newer version of Node.js"
        exit 1
    fi
    
    print_success "Node.js and npx are available"
}

# Function to start Playwright MCP server
start_server() {
    print_info "Starting Playwright MCP server on port 8931..."
    
    # Check if already running
    if lsof -i :8931 >/dev/null 2>&1; then
        print_warning "Port 8931 is already in use"
        print_info "Use '$0 stop' to stop the existing server first"
        exit 1
    fi
    
    # Start the server in background
    nohup npx @playwright/mcp@latest --port 8931 > /tmp/playwright-mcp.log 2>&1 &
    
    # Save PID
    echo $! > /tmp/playwright-mcp.pid
    
    # Wait a moment for server to start
    sleep 3
    
    # Check if server is running
    if check_server_running; then
        print_success "Playwright MCP server started successfully"
        print_info "Server is running on: http://localhost:8931"
        print_info "PID: $(cat /tmp/playwright-mcp.pid)"
        print_info "Logs: /tmp/playwright-mcp.log"
        print_info "Docker containers can access it via: host.docker.internal:8931"
    else
        print_error "Failed to start Playwright MCP server"
        print_info "Check logs: /tmp/playwright-mcp.log"
        exit 1
    fi
}

# Function to stop Playwright MCP server
stop_server() {
    print_info "Stopping Playwright MCP server..."
    
    if [ -f /tmp/playwright-mcp.pid ]; then
        local pid=$(cat /tmp/playwright-mcp.pid)
        if kill "$pid" 2>/dev/null; then
            print_success "Playwright MCP server stopped (PID: $pid)"
        else
            print_warning "Process not found or already stopped"
        fi
        rm -f /tmp/playwright-mcp.pid
    else
        print_warning "No PID file found"
    fi
    
    # Force kill any remaining processes on port 8931
    local port_pid=$(lsof -ti :8931 2>/dev/null)
    if [ -n "$port_pid" ]; then
        kill -9 "$port_pid" 2>/dev/null
        print_info "Killed process using port 8931"
    fi
    
    print_success "Playwright MCP server stopped"
}

# Function to check server status
check_server_running() {
    if lsof -i :8931 >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to show server status
show_status() {
    print_info "Checking Playwright MCP server status..."
    
    if check_server_running; then
        local pid_info=""
        if [ -f /tmp/playwright-mcp.pid ]; then
            local pid=$(cat /tmp/playwright-mcp.pid)
            pid_info=" (PID: $pid)"
        fi
        
        print_success "Playwright MCP server is running on port 8931$pid_info"
        print_info "Server URL: http://localhost:8931"
        print_info "Docker access: host.docker.internal:8931"
        
        # Test server response
        if command -v curl >/dev/null 2>&1; then
            if curl -s http://localhost:8931 >/dev/null 2>&1; then
                print_success "Server is responding to HTTP requests"
            else
                print_warning "Server is running but not responding to HTTP requests"
            fi
        fi
    else
        print_warning "Playwright MCP server is not running"
        print_info "Use '$0 start' to start the server"
    fi
}

# Main execution
main() {
    # Parse command line arguments
    local command=${1:-start}
    
    case $command in
        help|--help|-h)
            print_usage
            exit 0
            ;;
        start|stop|status)
            ;;
        *)
            print_error "Unknown command: $command"
            print_usage
            exit 1
            ;;
    esac
    
    # Check Node.js for start command
    if [[ "$command" == "start" ]]; then
        check_nodejs
    fi
    
    # Execute the requested command
    case $command in
        start)
            start_server
            ;;
        stop)
            stop_server
            ;;
        status)
            show_status
            ;;
    esac
}

# Run main function
main "$@"