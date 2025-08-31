# Authentication Module

## Overview

This module provides comprehensive authentication and security mechanisms for the A2A protocol, ensuring secure communication between agents in the multi-agent system.

## Core Components

### Credential Services

- [**`credentials.py`**](./credentials.py) - Main credential management system
  - `SimpleCredentialService`: In-memory credential storage for development
  - `EnvCredentialService`: Environment variable-based credential management
  - `CompositeCredentialService`: Multiple credential source composition

## Authentication Methods

### Supported Authentication Types

- **Bearer Token Authentication**
  - JWT tokens for stateless authentication
  - Environment variable: `A2A_BEARER_TOKEN`
  - Automatic token validation and refresh

- **API Key Authentication**
  - Static API key validation
  - Environment variable: `A2A_API_KEY`
  - Simple key comparison for validation

- **OAuth 2.0 Integration**
  - Client ID/Secret authentication
  - Environment variables: `A2A_OAUTH2_CLIENT_ID`, `A2A_OAUTH2_CLIENT_SECRET`
  - Token exchange and validation

### Credential Service Architecture

```python
# Environment-based credential service
credential_service = EnvCredentialService(env_prefix='A2A')

# Simple in-memory credential service
simple_service = SimpleCredentialService()
simple_service.set_credential('bearer', 'your-token-here')

# Composite service for multiple sources
composite_service = CompositeCredentialService([env_service, simple_service])
```

## Security Features

### Request Security

- **Credential Validation**: Automatic validation of incoming credentials
- **Request Context**: Server call context preservation for auditing
- **Error Handling**: Secure error responses without credential leakage
- **Logging**: Structured logging of authentication events

### Transport Security

- **HTTPS Enforcement**: TLS encryption for all communications
- **Certificate Validation**: Server certificate verification
- **Secure Headers**: Security headers for HTTP responses

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `A2A_BEARER_TOKEN` | Bearer token for authentication | None |
| `A2A_API_KEY` | API key for authentication | None |
| `A2A_OAUTH2_CLIENT_ID` | OAuth2 client ID | None |
| `A2A_OAUTH2_CLIENT_SECRET` | OAuth2 client secret | None |
| `IS_DOCKER` | Docker environment flag | `false` |

### Service Configuration

```python
# Configure credential service
credential_service = EnvCredentialService(env_prefix='A2A')

# Use with A2A client
client_manager = A2AClientManager(
    base_url="http://agent-url:8000",
    credential_service=credential_service
)
```

## Usage Examples

### Basic Authentication Setup

```python
from src.a2a_integration.auth.credentials import EnvCredentialService

# Initialize credential service
credential_service = EnvCredentialService()

# Use in A2A client manager
client_manager = A2AClientManager(
    base_url="http://secure-agent:8000",
    credential_service=credential_service
)

# Initialize and send authenticated request
await client_manager.initialize()
response = await client_manager.send_query("secure task")
```

### Custom Credential Service

```python
from src.a2a_integration.auth.credentials import SimpleCredentialService

# Create custom credential service
credential_service = SimpleCredentialService()

# Set credentials for different schemes
credential_service.set_credential('bearer', 'eyJ0eXAi...')
credential_service.set_credential('api_key', 'sk-1234567890')

# Use in authentication
async def get_credentials(security_scheme, context):
    return await credential_service.get_credentials(security_scheme, context)
```

## Security Best Practices

### Development Environment

- Use `SimpleCredentialService` for local development
- Avoid committing credentials to version control
- Use environment variables for sensitive data
- Enable debug logging for troubleshooting

### Production Environment

- Always use `EnvCredentialService` for production
- Store credentials in secure key management systems
- Implement credential rotation policies
- Enable comprehensive audit logging
- Use HTTPS/TLS for all communications

### Key Management

- **Rotation**: Regularly rotate authentication keys
- **Storage**: Use secure key vaults or environment variables
- **Access Control**: Implement principle of least privilege
- **Monitoring**: Log all authentication attempts
- **Revocation**: Implement immediate credential revocation

## Error Handling

### Authentication Errors

- **Invalid Credentials**: Clear error messages without credential details
- **Expired Tokens**: Automatic token refresh where possible
- **Missing Credentials**: Graceful handling with appropriate error codes
- **Rate Limiting**: Protection against brute force attacks

### Security Events

```python
# Authentication failure logging
logger.warning(
    "Authentication failed",
    extra={
        "agent_id": context.agent_id,
        "security_scheme": security_scheme,
        "ip_address": context.client_ip,
        "timestamp": datetime.now().isoformat()
    }
)
```

## File Structure

```
src/a2a_integration/auth/
├── __init__.py                 # Package exports
├── credentials.py             # Credential service implementations
└── Agents.md                  # This documentation
```

## Integration with A2A Protocol

The authentication module integrates seamlessly with the A2A protocol:

1. **Client Authentication**: Automatic credential inclusion in A2A requests
2. **Server Validation**: Request validation using configured credential services
3. **Context Preservation**: Authentication context maintained throughout request lifecycle
4. **Error Propagation**: Structured error responses for authentication failures

-----

## Related Documentation

### Navigation

- [**Back to A2A Integration**](../AGENT.md) - Return to A2A integration documentation
- [**Source Architecture**](../../AGENT.md) - Return to source code documentation
- [**Main Architecture**](../../../AGENT.md) - Return to main documentation