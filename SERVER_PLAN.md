# Server Implementation Plan

## Overview

This document outlines the implementation of a REST API and MCP server for the git-fork-recon tool. The server will provide asynchronous processing of repository analysis with caching and support for multiple output formats.

## Dependencies

### Optional Dependencies to Add to pyproject.toml

```toml
[project.optional-dependencies]
server = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0"
]
mcp = [
    "fastmcp>=0.10.0"
]
dev = ["pytest>=7.0.0", "black>=24.0.0", "mypy>=1.8.0", "ruff>=0.2.0"]
```

## REST API Design

### Endpoints

#### POST /analyze

**Request Body:**
```json
{
    "repo_url": "https://github.com/owner/repo",
    "model": "deepseek/deepseek-chat-v3-0324:free",  // optional
    "nocache": false,                              // optional
    "github_token": "ghp_xxx",                    // optional
    "format": "markdown"                           // optional (markdown, json, html, pdf)
}
```

**Response (when generating):**
```json
{
    "status": "generating",
    "retry-after": "Wed, 21 Oct 2025 07:28:00 GMT"
}
```

**Response (when available):**
```json
{
    "status": "available",
    "link": "/cache/owner/repo/2025-10-04T12-34-56Z/report.md",
    "last-updated": "Wed, 21 Oct 2025 07:28:00 GMT"
}
```

#### GET /report/{owner}/{repo}/{timestamp}/report.{format}

Returns the generated report in the specified format.

#### GET /health

Health check endpoint. Returns 200 if service is healthy.

#### GET /health/ready

Readiness check endpoint. Returns 200 if service is ready to accept requests.

## Caching System

### Cache Structure
```
cache_dir/
├── owner/
│   └── repo/
│       ├── 2025-10-04T12-34-56Z/
│       │   ├── report.md
│       │   ├── report.json (future)
│       │   ├── report.html (future)
│       │   ├── report.pdf (future)
│       │   └── metadata.json
│       └── latest -> 2025-10-04T12-34-56Z (symlink)
```

### Metadata Format
```json
{
    "generated_date": "2025-10-04T12:34:56Z",
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "repo_url": "https://github.com/owner/repo",
    "format": "markdown",
    "github_token_available": true
}
```

### Cache Behavior

- If `nocache=false` and cache exists → Return cached version immediately
- If `nocache=true` or no cache exists → Start new analysis
- Each analysis gets a timestamped folder
- `latest` symlink always points to most recent analysis
- Cache includes metadata for tracking

## Environment Variables

Add to existing .env.example:
```
# Server configuration
ALLOWED_MODELS=deepseek/deepseek-chat-v3-0324:free,gpt-4,claude-3.5-sonnet
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
SERVER_CACHE_DIR=/var/cache/git-fork-recon
DISABLE_AUTH=0
AUTH_BEARER_TOKEN=your-secret-token-here
PARALLEL_TASKS=2
```

## Implementation Steps

### 1. Refactor Core Module
- Extract existing `analyze()` function to return results instead of writing to files
- Create clean module API for server use
- Separate output generation from analysis logic

### 2. Create Server Module (`git_fork_recon_server`)
- FastAPI application with async endpoints
- Background task management with configurable concurrency via PARALLEL_TASKS (default: 2)
- Rate limiting with exponential backoff (max 8 retries) and Retry-After header respect for GitHub API
- Cache management utilities
- Response models with Pydantic validation
- Authentication middleware with Bearer token support
- Health check endpoints (/health and /health/ready)
- Configurable cache directory support

### 3. Caching System
- Versioned cache directories with timestamp naming
- Metadata tracking for each analysis
- Symlink management for 'latest' version
- Configurable cache directory via SERVER_CACHE_DIR
- Retain all versions (no automatic expiry - future enhancement)

### 4. CLI Command
- New `git-fork-recon-server` command
- Wrapper around uvicorn with configurable host/port
- Server lifecycle management

### 5. Template Updates
- Add `{{ generated_date }}` variable to markdown template
- Ensure template can be used by both CLI and server

## Key Technical Decisions

### Asynchronous Processing
- Multiple concurrent analyses using FastAPI BackgroundTasks
- Configurable concurrency limit via PARALLEL_TASKS environment variable (default: 2)
- Architecture designed to be extensible to Celery for production scalability
- Immediate response with `Retry-After` header
- Client polls for completion

### Authentication
- Bearer token authentication by default
- DISABLE_AUTH=1 environment variable to disable authentication for development
- Configurable via AUTH_BEARER_TOKEN environment variable

### Model Validation
- Server validates model against `ALLOWED_MODELS` env var
- Prevents use of unauthorised models

### Cache Strategy
- Preserves analysis history with timestamped versions
- `latest` symlink for easy access to newest result
- Metadata for tracking analysis parameters
- Configurable cache directory via SERVER_CACHE_DIR
- Retain all versions (no automatic expiry - future enhancement)

### Error Handling
- Graceful handling of invalid repository URLs
- GitHub API rate limiting with exponential backoff (max 8 retries) and Retry-After header respect
- Concurrent task limiting to prevent resource exhaustion
- Model availability checking

## Future Extensions

### MCP Server
- FastMCP integration for tool use
- Structured output based on Pydantic schemas
- AI agent compatibility

### Additional Formats
- JSON output with structured data
- HTML rendering with styling
- PDF generation (requires additional dependencies)

### Cache Management
- Automatic cleanup of old versions
- Configurable retention policies
- Cache size limits

## Security Considerations

- GitHub token validation and secure handling
- Model usage restrictions via ALLOWED_MODELS
- Cache directory permissions
- API rate limiting protection

## Questions for Clarification

All requirements have been clarified. Ready for implementation.