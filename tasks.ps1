<#
.SYNOPSIS
    Task runner for pyfilechoose (Windows / PowerShell).

.DESCRIPTION
    Convenience wrapper around the common project commands.

.EXAMPLE
    .\tasks.ps1 docs-serve     # live preview of the docs at http://127.0.0.1:8000
    .\tasks.ps1 docs-build     # build the static site into ./site
    .\tasks.ps1 docs-deploy    # publish the docs to GitHub Pages
    .\tasks.ps1 test           # run the test suite
    .\tasks.ps1 build          # build the wheel and sdist into ./dist
#>

param(
    [Parameter(Position = 0)]
    [ValidateSet("help", "install", "docs", "docs-serve", "docs-build",
                 "docs-deploy", "test", "build", "clean")]
    [string]$Task = "help"
)

$ErrorActionPreference = "Stop"

switch ($Task) {
    "install" {
        # Install the package with dev and docs extras into the current env.
        python -m pip install -e ".[dev,docs]"
    }
    { $_ -in "docs", "docs-serve" } {
        # Live-reload preview while you edit the docs.
        python -m mkdocs serve
    }
    "docs-build" {
        # Build the static site; fail on any broken link.
        python -m mkdocs build --strict
    }
    "docs-deploy" {
        # Push the built site to the gh-pages branch (manual deploy).
        python -m mkdocs gh-deploy --force
    }
    "test" {
        python -m pytest
    }
    "build" {
        # Clean previous artifacts, then build wheel + sdist and validate them.
        Remove-Item -Recurse -Force dist, build, src\pyfilechoose.egg-info -ErrorAction SilentlyContinue
        python -m build
        python -m twine check dist/*
    }
    "clean" {
        Remove-Item -Recurse -Force dist, build, site, src\pyfilechoose.egg-info -ErrorAction SilentlyContinue
        Write-Host "Cleaned build artifacts."
    }
    default {
        Write-Host "Usage: .\tasks.ps1 <task>"
        Write-Host ""
        Write-Host "Tasks:"
        Write-Host "  install       Install the package with dev + docs extras"
        Write-Host "  docs-serve    Live preview of the docs (http://127.0.0.1:8000)"
        Write-Host "  docs-build    Build the static site into ./site"
        Write-Host "  docs-deploy   Publish the docs to GitHub Pages"
        Write-Host "  test          Run the test suite"
        Write-Host "  build         Build wheel + sdist into ./dist"
        Write-Host "  clean         Remove build artifacts"
    }
}
