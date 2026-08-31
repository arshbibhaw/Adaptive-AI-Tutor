"""
Setup script.

Initializes the development environment: creates directories,
copies .env, and verifies dependencies.
"""

import os
import shutil
import subprocess
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    print("=== AI Teacher Setup ===\n")

    # Create data directories
    for d in ["data/uploads", "data/processed", "data/embeddings", "data/demo"]:
        path = os.path.join(ROOT, d)
        os.makedirs(path, exist_ok=True)
        print(f"✓ Directory: {d}")

    # Copy .env.example to .env if not exists
    env_src = os.path.join(ROOT, ".env.example")
    env_dst = os.path.join(ROOT, ".env")
    if not os.path.exists(env_dst):
        shutil.copy(env_src, env_dst)
        print("✓ Created .env from .env.example")
    else:
        print("• .env already exists")

    # Install Python dependencies
    print("\nInstalling Python dependencies...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", os.path.join(ROOT, "requirements.txt")],
        check=True,
    )

    # Install frontend dependencies
    web_dir = os.path.join(ROOT, "apps", "web")
    if os.path.exists(os.path.join(web_dir, "package.json")):
        print("\nInstalling frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=web_dir, check=True)

    print("\n=== Setup Complete ===")
    print("Next steps:")
    print("  1. Edit .env with your API keys and database URL")
    print("  2. Run backend: uvicorn backend.app.main:app --reload")
    print("  3. Run frontend: cd apps/web && npm run dev")


if __name__ == "__main__":
    main()
