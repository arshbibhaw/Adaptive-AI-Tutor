"""
Health check script.

Verifies that all components of the AI Teacher system are accessible.
"""

import os
import sys
import importlib


def check(name: str, condition: bool):
    status = "✓" if condition else "✗"
    print(f"  {status} {name}")
    return condition


def main():
    print("=== AI Teacher Health Check ===\n")
    all_ok = True

    # Check environment
    print("Environment:")
    all_ok &= check(".env exists", os.path.exists(".env"))
    all_ok &= check("DATABASE_URL set", bool(os.environ.get("DATABASE_URL", "")))

    # Check Python packages
    print("\nPython Packages:")
    for pkg in ["fastapi", "sqlalchemy", "pydantic", "PyPDF2", "docx", "pptx"]:
        try:
            importlib.import_module(pkg)
            all_ok &= check(pkg, True)
        except ImportError:
            all_ok &= check(f"{pkg} (MISSING)", False)

    # Check directories
    print("\nDirectories:")
    for d in ["data/uploads", "data/processed", "backend/app", "apps/web"]:
        all_ok &= check(d, os.path.isdir(d))

    # Check placeholder status
    print("\nAPI Configuration:")
    all_ok &= check("LLM_API_KEY", bool(os.environ.get("LLM_API_KEY", "")))
    check("TTS_API_KEY (optional)", bool(os.environ.get("TTS_API_KEY", "")))
    check("AVATAR_API_KEY (optional)", bool(os.environ.get("AVATAR_API_KEY", "")))

    print(f"\n{'=== ALL CHECKS PASSED ===' if all_ok else '=== SOME CHECKS FAILED ==='}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
