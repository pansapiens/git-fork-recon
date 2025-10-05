"""FastAPI application for git-fork-recon server."""

import logging
from datetime import datetime, timezone
from typing import Optional
import os

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware

from .models import AnalysisRequest, AnalysisResponse, HealthResponse
from .cache import CacheManager
from .analysis import AnalysisManager
from .auth import AuthMiddleware


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Git Fork Recon Server",
        description="REST API for analyzing GitHub repository fork networks",
        version="0.1.0",
    )

    # Initialize components
    cache_manager = CacheManager()
    analysis_manager = AnalysisManager(cache_manager)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add authentication middleware
    app.add_middleware(AuthMiddleware)

    @app.get("/health")
    async def health_check() -> HealthResponse:
        """Basic health check endpoint."""
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now(timezone.utc),
            version="0.1.0",
            checks={
                "cache": {"status": "ok", "path": str(cache_manager.cache_dir)},
                "auth": {"disabled": os.getenv("DISABLE_AUTH", "0") == "1"},
                "concurrent_jobs": analysis_manager.get_job_count(),
                "max_concurrent": analysis_manager.max_concurrent,
            }
        )

    @app.get("/health/ready")
    async def readiness_check() -> HealthResponse:
        """Readiness check endpoint."""
        # Check if we can accept new jobs
        can_accept = analysis_manager.get_job_count() < analysis_manager.max_concurrent

        return HealthResponse(
            status="ready" if can_accept else "busy",
            timestamp=datetime.now(timezone.utc),
            version="0.1.0",
            checks={
                "cache": {"status": "ok", "path": str(cache_manager.cache_dir)},
                "auth": {"disabled": os.getenv("DISABLE_AUTH", "0") == "1"},
                "concurrent_jobs": analysis_manager.get_job_count(),
                "max_concurrent": analysis_manager.max_concurrent,
                "can_accept_new_jobs": can_accept,
            }
        )

    @app.post("/analyze", response_model=AnalysisResponse)
    async def analyze_repository(
        request: AnalysisRequest,
        background_tasks: BackgroundTasks,
    ) -> AnalysisResponse:
        """Start repository analysis."""
        # Convert to dict and remove None values
        kwargs = {
            "repo_url": str(request.repo_url),
            "model": request.model,
            "github_token": request.github_token,
            "format": request.format,
            "nocache": request.nocache,
        }
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        # Get analysis response
        response = await analysis_manager.analyze_repository(**kwargs)

        # If analysis needs to be started, add background task
        if response.status == "generating":
            task_kwargs = {
                "repo_url": str(request.repo_url),
                "model": request.model,
                "github_token": request.github_token,
                "format": request.format,
            }
            task_kwargs = {k: v for k, v in task_kwargs.items() if v is not None}

            background_tasks.add_task(
                analysis_manager.run_analysis_task,
                **task_kwargs
            )

        return response

    @app.get("/report/{owner}/{repo}/{timestamp}/report.{format}")
    async def get_report(
        owner: str,
        repo: str,
        timestamp: str,
        format: str,
    ):
        """Get a cached report."""
        # Map URL format to API format
        url_to_api_format = {
            "md": "markdown",
            "markdown": "markdown",  # for backward compatibility
            "json": "json",
            "html": "html",
            "pdf": "pdf",
        }

        api_format = url_to_api_format.get(format)
        if api_format is None:
            raise HTTPException(status_code=400, detail=f"Invalid format. Allowed: {list(url_to_api_format.keys())}")

        # Check if this analysis is currently running
        repo_url = f"https://github.com/{owner}/{repo}"
        model_part = "default"  # Since we don't have model info in GET request
        job_key = f"{repo_url}::{model_part}"
        if job_key in analysis_manager.active_jobs:
            retry_after = analysis_manager.get_retry_after()
            return JSONResponse(
                status_code=202,
                content={
                    "status": "generating",
                    "retry-after": retry_after.strftime("%a, %d %b %Y %H:%M:%S GMT")
                },
                headers={"Retry-After": retry_after.strftime("%a, %d %b %Y %H:%M:%S GMT")}
            )

        # Get cached result
        result = cache_manager.get_result(owner, repo, timestamp, requested_format=api_format)
        if not result:
            raise HTTPException(status_code=404, detail="Report not found")

        content, metadata = result

        # Return content directly
        return Response(
            content=content,
            media_type=_get_media_type(api_format),
            headers={"Content-Disposition": f"attachment; filename={owner}-{repo}-forks.{format}"}
        )

    @app.get("/report/{owner}/{repo}/latest/report.{format}")
    async def get_latest_report(
        owner: str,
        repo: str,
        format: str,
    ):
        """Get the latest cached report."""
        # Map URL format to API format
        url_to_api_format = {
            "md": "markdown",
            "markdown": "markdown",  # for backward compatibility
            "json": "json",
            "html": "html",
            "pdf": "pdf",
        }

        api_format = url_to_api_format.get(format)
        if api_format is None:
            raise HTTPException(status_code=400, detail=f"Invalid format. Allowed: {list(url_to_api_format.keys())}")

        # Check if this analysis is currently running
        repo_url = f"https://github.com/{owner}/{repo}"
        model_part = "default"  # Since we don't have model info in GET request
        job_key = f"{repo_url}::{model_part}"
        if job_key in analysis_manager.active_jobs:
            retry_after = analysis_manager.get_retry_after()
            return JSONResponse(
                status_code=202,
                content={
                    "status": "generating",
                    "retry-after": retry_after.strftime("%a, %d %b %Y %H:%M:%S GMT")
                },
                headers={"Retry-After": retry_after.strftime("%a, %d %b %Y %H:%M:%S GMT")}
            )

        # Get latest version
        latest = cache_manager.get_latest_version(owner, repo)
        if not latest:
            raise HTTPException(status_code=404, detail="No reports found for this repository")

        # Get cached result
        result = cache_manager.get_result(owner, repo, latest, requested_format=api_format)
        if not result:
            raise HTTPException(status_code=404, detail="Report not found")

        content, metadata = result

        # Return content directly
        return Response(
            content=content,
            media_type=_get_media_type(api_format),
            headers={"Content-Disposition": f"attachment; filename={owner}-{repo}-forks.{format}"}
        )

    def _get_media_type(format: str) -> str:
        """Get the appropriate media type for a format."""
        media_types = {
            "markdown": "text/markdown",
            "json": "application/json",
            "html": "text/html",
            "pdf": "application/pdf",
        }
        return media_types.get(format, "text/plain")

    return app


# Create the application instance
app = create_app()