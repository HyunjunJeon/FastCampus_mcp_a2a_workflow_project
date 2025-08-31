# FastCampus Multi-Agent Workflow Automation Docker Runner
# PowerShell script for Windows environments

# Requires -Version 5.0

[CmdletBinding()]
param(
    [ValidateSet("start", "stop", "restart", "logs", "status", "clean", "build", "mcp-only", "help")]
    [string]$Command = "start"
)

# Project constants
$COMPOSE_FILE = "docker-compose-full.yml"
$ENV_FILE = ".env"
$ENV_EXAMPLE = ".env.example"
$PROJECT_NAME = "fastcampus-workflow-automation"

# Color definitions for console output
$Colors = @{
    Info = "Cyan"
    Success = "Green"
    Warning = "Yellow"
    Error = "Red"
}

# Function to print colored messages
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Colors.Info
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Colors.Success
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Colors.Warning
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Colors.Error
}

# Function to print usage information
function Show-Usage {
    Write-Host "Usage: .\run-docker.ps1 [COMMAND]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  start       Start all services (default)"
    Write-Host "  stop        Stop all services"
    Write-Host "  restart     Restart all services"
    Write-Host "  logs        Show logs from all services"
    Write-Host "  status      Show status of all services"
    Write-Host "  clean       Stop and remove all containers, networks, and volumes"
    Write-Host "  build       Build all services"
    Write-Host "  mcp-only    Start only MCP servers (notion-mcp, openmemory-mcp, mem0-store)"
    Write-Host "  help        Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\run-docker.ps1 start"
    Write-Host "  .\run-docker.ps1 logs"
    Write-Host "  .\run-docker.ps1 clean"
    Write-Host "  .\run-docker.ps1 mcp-only"
}

# Function to check if command exists
function Test-Command {
    param([string]$CommandName)
    return $null -ne (Get-Command $CommandName -ErrorAction SilentlyContinue)
}

# Function to check Docker installation and status
function Test-Docker {
    Write-Info "Checking Docker installation..."
    
    if (-not (Test-Command "docker")) {
        Write-Error "Docker is not installed or not in PATH"
        Write-Info "Please install Docker Desktop from: https://docs.docker.com/desktop/windows/"
        exit 1
    }
    
    try {
        $dockerInfo = docker info 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Docker daemon is not running"
            Write-Info "Please start Docker Desktop and try again"
            exit 1
        }
    }
    catch {
        Write-Error "Failed to connect to Docker daemon"
        Write-Info "Please ensure Docker Desktop is running and try again"
        exit 1
    }
    
    # Check Docker Compose
    $composeAvailable = $false
    try {
        docker compose version 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $composeAvailable = $true
        }
    }
    catch { }
    
    if (-not $composeAvailable -and -not (Test-Command "docker-compose")) {
        Write-Error "Docker Compose is not available"
        Write-Info "Please install Docker Compose or upgrade to Docker Desktop with built-in compose"
        exit 1
    }
    
    Write-Success "Docker is installed and running"
}

# Function to check if docker-compose-full.yml exists
function Test-ComposeFile {
    if (-not (Test-Path $COMPOSE_FILE)) {
        Write-Error "Docker compose file '$COMPOSE_FILE' not found"
        Write-Info "Please ensure you are in the correct project directory"
        exit 1
    }
    Write-Success "Docker compose file found"
}

# Function to setup .env file
function Initialize-EnvFile {
    Write-Info "Checking environment configuration..."
    
    if (-not (Test-Path $ENV_FILE)) {
        if (Test-Path $ENV_EXAMPLE) {
            Write-Warning ".env file not found, creating from .env.example"
            Copy-Item $ENV_EXAMPLE $ENV_FILE
            Write-Success ".env file created from template"
            Write-Warning "Please edit .env file and add your API keys before running the services"
        }
        else {
            Write-Error "Neither .env nor .env.example file found"
            exit 1
        }
    }
    else {
        Write-Success ".env file found"
    }
}

# Function to validate essential environment variables
function Test-EnvironmentVariables {
    Write-Info "Validating essential environment variables..."
    
    if (-not (Test-Path $ENV_FILE)) {
        Write-Error ".env file not found"
        return $false
    }
    
    # Read .env file and parse environment variables
    $envVars = @{}
    Get-Content $ENV_FILE | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.*)$') {
            $envVars[$matches[1].Trim()] = $matches[2].Trim('"').Trim("'")
        }
    }
    
    # List of critical environment variables
    $criticalVars = @("OPENAI_API_KEY", "USER")
    $missingVars = @()
    
    foreach ($var in $criticalVars) {
        if (-not $envVars.ContainsKey($var) -or [string]::IsNullOrWhiteSpace($envVars[$var])) {
            $missingVars += $var
        }
    }
    
    if ($missingVars.Count -gt 0) {
        Write-Error "The following critical environment variables are missing or empty:"
        $missingVars | ForEach-Object { Write-Host "  - $_" }
        Write-Info "Please edit the .env file and set these variables"
        return $false
    }
    
    Write-Success "Essential environment variables are set"
    return $true
}

# Function to get Docker Compose command
function Get-ComposeCommand {
    try {
        docker compose version 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            return "docker compose"
        }
    }
    catch { }
    
    if (Test-Command "docker-compose") {
        return "docker-compose"
    }
    
    Write-Error "Docker Compose command not available"
    exit 1
}

# Function to execute Docker Compose command
function Invoke-DockerCompose {
    param(
        [string]$Arguments,
        [switch]$Interactive
    )
    
    $composeCmd = Get-ComposeCommand
    $fullCommand = "$composeCmd -f `"$COMPOSE_FILE`" --project-name `"$PROJECT_NAME`" $Arguments"
    
    Write-Info "Executing: $fullCommand"
    
    if ($Interactive) {
        # For interactive commands like logs
        Invoke-Expression $fullCommand
    }
    else {
        try {
            Invoke-Expression $fullCommand
            if ($LASTEXITCODE -ne 0) {
                throw "Command failed with exit code $LASTEXITCODE"
            }
        }
        catch {
            Write-Error "Failed to execute Docker Compose command: $_"
            exit 1
        }
    }
}

# Function to start services
function Start-Services {
    Write-Info "Starting all services..."
    
    Invoke-DockerCompose "up -d"
    
    Write-Success "All services started successfully"
    Write-Info "Services are now running in the background"
    Write-Info "You can check logs with: .\run-docker.ps1 logs"
    Write-Info "You can check status with: .\run-docker.ps1 status"
}

# Function to start only MCP services
function Start-McpServices {
    Write-Info "Starting MCP services only..."
    
    # MCP services: notion-mcp, openmemory-mcp, mem0-store (playwright-mcp는 호스트에서 실행)
    $mcpServices = @("mem0-store", "notion-mcp", "openmemory-mcp")
    $serviceArgs = $mcpServices -join " "
    
    Invoke-DockerCompose "up -d $serviceArgs"
    
    Write-Success "MCP services started successfully"
    Write-Info "Services are now running in the background"
    Write-Info "MCP services running:"
    Write-Info "  - Notion MCP: http://localhost:8930"
    Write-Info "  - OpenMemory MCP: http://localhost:8765"
    Write-Info "  - Qdrant (Mem0 Store): http://localhost:6333"
    Write-Info "  - Playwright MCP: 호스트에서 'npx @playwright/mcp@latest --port 8931'로 실행"
    Write-Info "You can check logs with: .\run-docker.ps1 logs"
    Write-Info "You can check status with: .\run-docker.ps1 status"
}

# Function to stop services
function Stop-Services {
    Write-Info "Stopping all services..."
    
    Invoke-DockerCompose "down"
    
    Write-Success "All services stopped successfully"
}

# Function to restart services
function Restart-Services {
    Write-Info "Restarting all services..."
    Stop-Services
    Start-Services
}

# Function to show logs
function Show-Logs {
    Write-Info "Showing logs from all services..."
    Write-Info "Press Ctrl+C to exit logs"
    
    Invoke-DockerCompose "logs -f" -Interactive
}

# Function to show status
function Show-Status {
    Write-Info "Showing status of all services..."
    
    Invoke-DockerCompose "ps"
}

# Function to clean up everything
function Clear-Services {
    Write-Warning "This will stop and remove all containers, networks, and volumes"
    $confirmation = Read-Host "Are you sure? (y/N)"
    
    if ($confirmation -match "^[Yy]$") {
        Write-Info "Cleaning up all services and data..."
        
        Invoke-DockerCompose "down -v --remove-orphans"
        
        # Remove any dangling volumes
        try {
            docker volume prune -f 2>$null | Out-Null
        }
        catch {
            Write-Warning "Failed to prune dangling volumes"
        }
        
        Write-Success "Cleanup completed"
    }
    else {
        Write-Info "Cleanup cancelled"
    }
}

# Function to build services
function Build-Services {
    Write-Info "Building all services..."
    
    Invoke-DockerCompose "build"
    
    Write-Success "All services built successfully"
}

# Main execution function
function Main {
    param([string]$CommandName)
    
    # Handle help command
    if ($CommandName -eq "help") {
        Show-Usage
        return
    }
    
    # Pre-flight checks
    Test-Docker
    Test-ComposeFile
    Initialize-EnvFile
    
    # Validate environment for start/restart/mcp-only commands
    if ($CommandName -in @("start", "restart", "mcp-only")) {
        if (-not (Test-EnvironmentVariables)) {
            Write-Error "Environment validation failed. Please fix the issues above."
            exit 1
        }
    }
    
    # Execute the requested command
    switch ($CommandName) {
        "start" {
            Start-Services
        }
        "stop" {
            Stop-Services
        }
        "restart" {
            Restart-Services
        }
        "logs" {
            Show-Logs
        }
        "status" {
            Show-Status
        }
        "clean" {
            Clear-Services
        }
        "build" {
            Build-Services
        }
        "mcp-only" {
            Start-McpServices
        }
        default {
            Write-Error "Unknown command: $CommandName"
            Show-Usage
            exit 1
        }
    }
}

# Script execution starts here
try {
    # Set execution policy for current session if needed
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force -ErrorAction SilentlyContinue
    
    # Execute main function
    Main -CommandName $Command
}
catch {
    Write-Error "An unexpected error occurred: $_"
    exit 1
}