#!/bin/bash

# LangChain Sandbox MCP Server 실행 스크립트
# WebAssembly 기반 Python 코드 실행 서버

echo "🚀 Starting LangChain Sandbox MCP Server..."
echo "📦 WebAssembly-based Python execution environment"
echo ""

# Deno 설치 확인
if ! command -v deno &> /dev/null
then
    echo "⚠️  Deno is not installed. LangChain Sandbox requires Deno runtime."
    echo "📌 Please install Deno first:"
    echo "   curl -fsSL https://deno.land/install.sh | sh"
    echo "   or"
    echo "   brew install deno"
    exit 1
fi

# Python 버전 확인
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
MIN_VERSION="3.10"

if [ "$(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
    echo "⚠️  Python $MIN_VERSION or higher is required (current: $PYTHON_VERSION)"
    exit 1
fi

# 환경 변수 설정
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
export IS_DOCKER=false

# 기본 설정
PORT=${PORT:-8035}
HOST=${HOST:-0.0.0.0}
DEBUG=${DEBUG:-false}
ALLOW_NETWORK=${ALLOW_NETWORK:-true}
SESSION_TIMEOUT=${SESSION_TIMEOUT:-30}
MAX_SESSIONS=${MAX_SESSIONS:-10}

# 디버그 모드 플래그 설정
DEBUG_FLAG=""
if [ "$DEBUG" = "true" ]; then
    DEBUG_FLAG="--debug"
fi

# 네트워크 비활성화 플래그
NETWORK_FLAG=""
if [ "$ALLOW_NETWORK" = "false" ]; then
    NETWORK_FLAG="--no-network"
fi

echo "📋 Configuration:"
echo "   Host: $HOST"
echo "   Port: $PORT"
echo "   Debug: $DEBUG"
echo "   Network Access: $ALLOW_NETWORK"
echo "   Session Timeout: $SESSION_TIMEOUT minutes"
echo "   Max Sessions: $MAX_SESSIONS"
echo ""

echo "🔗 Endpoints:"
echo "   Health Check: http://$HOST:$PORT/health"
echo "   MCP Endpoint: http://$HOST:$PORT/mcp"
echo ""

# 서버 실행
echo "⏳ Starting server..."
python3 -m src.mcp_config_module.servers.langchain_sandbox_server \
    --port $PORT \
    --host $HOST \
    --session-timeout $SESSION_TIMEOUT \
    --max-sessions $MAX_SESSIONS \
    $DEBUG_FLAG \
    $NETWORK_FLAG