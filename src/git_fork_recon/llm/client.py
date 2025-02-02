from typing import List, Optional
import logging
import json

import httpx

from ..git.repo import CommitInfo

logger = logging.getLogger(__name__)

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


class LLMClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/git-fork-recon",
            "Content-Type": "application/json",
        }

    def _make_request(self, messages: List[dict]) -> str:
        """Make a request to the OpenRouter API."""
        data = {
            "model": "deepseek/deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000,
        }

        try:
            response = httpx.post(
                OPENROUTER_API_URL, headers=self.headers, json=data, timeout=30.0
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error making LLM request: {e}")
            raise

    def summarize_changes(
        self, commits: List[CommitInfo], diff: Optional[str] = None
    ) -> str:
        """Generate a summary of changes from commits and optional diff."""
        # Create a structured summary of commits
        commit_summaries = []
        for commit in commits:
            summary = {
                "hash": commit.hash[:8],
                "message": commit.message,
                "author": commit.author,
                "date": commit.date,
                "stats": {
                    "files_changed": len(commit.files_changed),
                    "insertions": commit.insertions,
                    "deletions": commit.deletions,
                },
                "files": commit.files_changed,
            }
            commit_summaries.append(summary)

        # Create the prompt
        messages = [
            {
                "role": "system",
                "content": """You are an expert code reviewer analyzing changes made in a fork of a GitHub repository.
                Your task is to provide a clear, concise summary of the changes and innovations introduced in the fork.
                Focus on:
                1. The main themes or purposes of the changes
                2. Any significant new features or improvements
                3. Notable code refactoring or architectural changes
                4. Potential impact or value of the changes
                
                Be objective and technical, but make the summary accessible to developers.""",
            },
            {
                "role": "user",
                "content": f"""Please analyze these changes and provide a summary:
                
                Commits: {json.dumps(commit_summaries, indent=2)}
                
                {"Diff:" + diff if diff else ""}""",
            },
        ]

        return self._make_request(messages)
