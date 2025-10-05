# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- REST API server with FastAPI for programmatic access
- Authentication middleware with Bearer token support
- Unified two-tier caching system with REPO_CACHE_DIR and REPORT_CACHE_DIR
- Versioned report caching with filesystem storage and metadata tracking
- Health check endpoints (/health and /health/ready)
- Concurrent task limiting via PARALLEL_TASKS environment variable
- Support for multiple output formats (markdown, json, html, pdf)
- Background task management for asynchronous analysis
- Git-fork-recon-server CLI command with configurable host/port
- AnalysisResult class for structured data return
- Module refactoring for better importability
- Generated date variable in report templates
- Model validation against ALLOWED_MODELS environment variable
- MCP server optional dependency (future implementation)
- Cross-platform cache directories using platformdirs
- uv sync instructions for modern dependency management

### Changed
- Refactored main.py to separate analysis logic from output generation
- Updated build configuration to include server module
- Enhanced error handling and status tracking
- Updated PyGithub to v2.8.1+ for rate limit API compatibility
- Fixed rate limit checking to use resources.core structure
- Migrated from single CACHE_DIR to separate REPO_CACHE_DIR and REPORT_CACHE_DIR
- Updated repository cache structure from dashes to {owner}/{repo} format

## [0.1.3]

### Fixed
- Don't attempt to summarize an empty list of forks to prevent hallucinations

## [0.1.2]

### Fixed
- Further fixes to .env file loading

## [0.1.1]

### Added
- Initial release with core functionality
- GitHub repository fork analysis
- LLM-powered summaries
- Caching system
- CLI interface
- Docker support