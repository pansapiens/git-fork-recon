# Git fork recon

Analyse the network of forked git repositories, summarise changes and innovations in forked repositories.

## Features

- Intelligent analysis of fork networks using LLM-powered summaries
- Filters and prioritizes forks based on number of commits ahead of parent, starts, recent activity, PRs. Ignores forks with no changes.
- Local caching of git repositories and forks as remotes
- Detailed Markdown reports with:
  - Repository overview
  - Analysis of significant forks
  - Commit details and statistics
  - Links to GitHub commits and repositories
  - Overall summary of changes and innovations highlighting the most interesting forks
- **REST API server** for programmatic access with:
  - Asynchronous analysis with background processing
  - Versioned caching with filesystem storage
  - Authentication support with Bearer tokens
  - Health check endpoints
  - Configurable concurrency and rate limiting

# Installation

```bash
pip install git-fork-recon

# For server functionality
pip install 'git-fork-recon[server]'

# For MCP server functionality (future)
pip install 'git-fork-recon[mcp]'
```

## Installation (development)

Using `uv` (recommended):
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate a new virtual environment (optional but recommended)
uv venv
source .venv/bin/activate

# Install the package in editable mode
uv pip install -e .

# Install server dependencies
uv pip install -e '.[server]'

# Install MCP server dependencies (future)
uv pip install -e '.[mcp]'

# Install development dependencies
uv pip install -e '.[dev]'
```

Alternatively, using `uv sync` (modern dependency management):
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync with base dependencies
uv sync

# Sync with server dependencies
uv sync --extra server

# Sync with MCP server dependencies (future)
uv sync --extra mcp

# Sync with development dependencies
uv sync --extra dev

# Sync with all extras
uv sync --all-extras
```

> **Note**: The first time you run `uv sync`, it will create a `uv.lock` file for reproducible builds. This file should be committed to version control to ensure all developers use the exact same dependency versions.

## Configuration

The following environment variables are required (can be provided via `.env` file):

- `GITHUB_TOKEN`: GitHub API token for (public read-only) repository metadata access
- `OPENROUTER_API_KEY` or `OPENAI_API_KEY`: API key for an OpenAI-compatible LLM provider
- `REPO_CACHE_DIR` (optional): Directory for caching cloned repositories (defaults to `~/.cache/git-fork-recon/repos` using platformdirs)

## Server Configuration

For the REST API server, additional environment variables are available:

- `ALLOWED_MODELS`: Comma-separated list of allowed LLM models (default: unrestricted)
- `SERVER_HOST`: Host to bind the server to (default: 127.0.0.1)
- `SERVER_PORT`: Port to bind the server to (default: 8000)
- `REPORT_CACHE_DIR`: Directory for server report cache (defaults to `~/.cache/git-fork-recon/reports` using platformdirs)
- `DISABLE_AUTH`: Set to `1` to disable authentication (default: enabled)
- `AUTH_BEARER_TOKEN`: Bearer token for API authentication
- `PARALLEL_TASKS`: Maximum concurrent analysis tasks (default: 2)
- `DISABLE_UI`: Set to `1` to disable the web UI at `/ui` endpoint (default: enabled)

## Running

```bash
# Using installed package
git-fork-recon https://github.com/martinpacesa/BindCraft

# Using uv run (recommended for development - automatically uses virtual environment)
uv run git-fork-recon https://github.com/martinpacesa/BindCraft
```

> **Note**: This project requires PyGithub v2.8.1+ for GitHub API rate limit handling. The dependency is automatically managed when using `uv sync` or `pip install`.

## REST API Server

Start the server:

```bash
# Using installed package
git-fork-recon-server --host 127.0.0.1 --port 8000

# Using uv run (recommended for development)
uv run git-fork-recon-server --host 127.0.0.1 --port 8000
```

Go to http://localhost:8000/ui to see the web UI.

### API Endpoints

- `POST /analyze` - Start repository analysis
- `GET /report/{owner}/{repo}/{timestamp}/report.{format}` - Get cached report
- `GET /report/{owner}/{repo}/latest/report.{format}` - Get latest cached report
- `GET /report/{owner}/{repo}/{timestamp}/status` - Get status for specific report version
- `GET /report/{owner}/{repo}/latest/status` - Get status for latest report
- `GET /metadata/{owner}/{repo}/{timestamp}` - Get metadata for specific report version
- `GET /metadata/{owner}/{repo}/latest` - Get metadata for latest report
- `GET /health` - Health check endpoint
- `GET /health/ready` - Readiness check endpoint
- `GET /ui` - Web UI for repository analysis (unless disabled with `DISABLE_UI=1`)

### Example Request

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/martinpacesa/BindCraft",
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "format": "markdown"
  }'
```

### Example Response

```json
{
  "status": "generating",
  "retry-after": "2025-10-04T12:35:00Z"
}
```

When analysis is complete:

```json
{
  "status": "available",
  "link": "/report/martinpacesa/BindCraft/latest/report.md",
  "last-updated": "2025-10-04T12:34:56Z"
}
```

### Retrieving the Generated Report

Once the analysis is complete, you can retrieve the report using the provided link:

```bash
# Get the latest report
curl -X GET "http://localhost:8000/report/martinpacesa/BindCraft/latest/report.md" \
  -H "Authorization: Bearer your-token" \
  -o martinpacesa-BindCraft-forks.md

# Or get a specific version by timestamp
curl -X GET "http://localhost:8000/report/martinpacesa/BindCraft/2025-10-04T12-34-56Z/report.md" \
  -H "Authorization: Bearer your-token" \
  -o martinpacesa-BindCraft-forks-v2025-10-04.md

# Get report in different formats (markdown, json, html, pdf)
curl -X GET "http://localhost:8000/report/martinpacesa/BindCraft/latest/report.json" \
  -H "Authorization: Bearer your-token" \
  -o martinpacesa-BindCraft-forks.json
```

### Checking Analysis Status

If you request a report while it's still being generated, you'll receive a `202 Accepted` response with a `Retry-After` header:

```bash
curl -X GET "http://localhost:8000/report/martinpacesa/BindCraft/latest/report.md" \
  -H "Authorization: Bearer your-token"
```

Response (while generating):
```json
{
  "status": "generating",
  "retry-after": "Wed, 05 Oct 2025 12:35:00 GMT"
}
```

Output is generated as `{username}-{repo}-forks.md` by default (use `-o` to specify a different file name, `-o -` to print to stdout).

## Options

```bash
$ git-fork-recon --help

 Usage: git-fork-recon [OPTIONS] [REPO_URL]

 Analyze a GitHub repository's fork network and generate a summary report.


╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   repo_url      [REPO_URL]  URL of the GitHub repository to analyze          │
│                             [default: None]                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --output              -o      PATH     Output file path (defaults to         │
│                                        {repo_name}-forks.md)                 │
│                                        [default: None]                       │
│ --active-within               TEXT     Only consider forks with activity     │
│                                        within this time period (e.g. '1      │
│                                        hour', '2 days', '6 months', '1       │
│                                        year')                                │
│                                        [default: None]                       │
│ --env-file                    PATH     Path to .env file [default: None]     │
│ --model                       TEXT     OpenRouter model to use (overrides    │
│                                        MODEL env var)                        │
│                                        [default: None]                       │
│ --context-length              INTEGER  Override model context length         │
│                                        (overrides CONTEXT_LENGTH env var)    │
│                                        [default: None]                       │
│ --api-base-url                TEXT     OpenAI-compatible API base URL        │
│                                        [default: None]                       │
│ --api-key-env-var             TEXT     Environment variable containing the   │
│                                        API key                               │
│                                        [default: None]                       │
│ --parallel            -p      INTEGER  Number of parallel requests           │
│                                        [default: 5]                          │
│ --verbose             -v               Enable verbose logging                │
│ --clear-cache                          Clear cached repository data before   │
│                                        analysis                              │
│ --force                                Force overwrite existing output file  │
│ --max-forks                   INTEGER  Maximum number of forks to analyze    │
│                                        (default: no limit)                   │
│                                        [default: None]                       │
│ --output-formats              TEXT     Comma-separated list of additional    │
│                                        formats to generate (html,pdf)        │
│                                        [default: None]                       │
│ --install-completion                   Install completion for the current    │
│                                        shell.                                │
│ --show-completion                      Show completion for the current       │
│                                        shell, to copy it or customize the    │
│                                        installation.                         │
│ --help                                 Show this message and exit.           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Running with Docker

Build the image:
```bash
docker build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -t git-fork-recon .
```

Run the analysis (replace the repository URL with your target):
```bash
# Create cache directory with correct permissions
mkdir -p "${HOME}/.cache/git-fork-recon"

docker run --rm \
  -v "$(pwd):/app" \
  -v "${HOME}/.cache/git-fork-recon:/app/.cache" \
  --env-file .env \
  --user "$(id -u):$(id -g)" \
  git-fork-recon \
  "https://github.com/martinpacesa/BindCraft"
```

## See also

- [Useful forks](https://useful-forks.github.io/)
- [frogmouth](https://github.com/Textualize/frogmouth) - a quick viewer for the generated Markdown
