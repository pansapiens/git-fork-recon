# Git fork recon

Analyse the network of forked git repositories, summarise changes and innovations in forked repositories.

## Features

- Intelligent analysis of fork networks using LLM-powered summaries
- Filters and prioritizes forks based on:
  - Number of commits ahead of parent
  - Number of stars
  - Recent activity
  - Associated pull requests
- Efficient local git analysis using remotes
- Detailed Markdown reports with:
  - Repository overview
  - Analysis of significant forks
  - Commit details and statistics
  - Links to GitHub commits and repositories

## Configuration

The following environment variables are required (can be provided via `.env` file):

- `GITHUB_TOKEN`: GitHub API token for repository access
- `OPENROUTER_API_KEY`: OpenRouter API key for LLM analysis
- `CACHE_DIR` (optional): Directory for caching repository data (defaults to `~/.cache/git-fork-recon`)

## Input

- A starting Github repository

## Output

- A Markdown document summarising the changes and innovations from each of the the forked repositories, focusing on those with the most significant changes.

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

This will:
- Run as your user to ensure correct file permissions
- Mount the current directory to `/app` to use the latest code and output the report
- Mount a cache directory to store cloned repositories between runs
- Load environment variables from `.env`
- Output a markdown report named `{username}-{repo}-forks.md`

Options:
- Use `-v` for verbose output: add it after `git-fork-recon`
- Specify custom output file: add `-o myreport.md` after the URL
- Print to stdout instead of file: add `-o -` after the URL
