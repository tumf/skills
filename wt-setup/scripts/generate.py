#!/usr/bin/env python3
"""
Generate a .wt/setup bootstrap script for git worktree environments.

Inspects the current directory (or a specified path) to detect the project type
and generates an appropriate .wt/setup script from templates in references/.

Usage:
    generate.py
    generate.py --type node
    generate.py --agents-md
    generate.py --dry-run
    generate.py --dir /path/to/project
"""

import argparse
import json
import os
import stat
import sys
from pathlib import Path


REFERENCES_DIR = Path(__file__).resolve().parent.parent / "references"

# Map project type to template filename in references/
TEMPLATE_FILES = {
    "make": "setup-make.sh",
    "node": "setup-node.sh",
    "python": "setup-python.sh",
    "rust": "setup-rust.sh",
    "multi": "setup-multi.sh",
}

AGENTS_MD_TEMPLATE_FILE = "AGENTS.md.template"

GITIGNORE_ENTRIES = [
    ".wt/setup.local",
    ".wt/worktrees/",
]


def load_template(name: str) -> str:
    """Load a template file from references/."""
    path = REFERENCES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text()


def detect_project_type(project_dir: Path) -> str:
    """Detect the project type based on files present in the directory."""
    # Check Makefile first (highest priority -- often wraps other tools)
    makefile = project_dir / "Makefile"
    if makefile.exists():
        content = makefile.read_text(errors="replace")
        if "setup:" in content or "setup :" in content:
            return "make"

    # Language-specific detection
    if (project_dir / "package.json").exists():
        return "node"
    if (project_dir / "pyproject.toml").exists():
        return "python"
    if (project_dir / "Cargo.toml").exists():
        return "rust"

    # Fallback: if Makefile exists without setup target, still use make
    if makefile.exists():
        return "make"

    return "make"  # Default fallback


def detect_package_manager(project_dir: Path) -> str:
    """Detect Node.js package manager."""
    if (project_dir / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (project_dir / "yarn.lock").exists():
        return "yarn"
    return "npm"


def update_gitignore(project_dir: Path, dry_run: bool) -> bool:
    """Add .wt/ entries to .gitignore if missing. Returns True if modified."""
    gitignore_path = project_dir / ".gitignore"
    existing_lines = []
    if gitignore_path.exists():
        existing_lines = gitignore_path.read_text().splitlines()

    missing = [e for e in GITIGNORE_ENTRIES if e not in existing_lines]
    if not missing:
        return False

    if dry_run:
        return True

    with open(gitignore_path, "a") as f:
        if existing_lines and existing_lines[-1].strip():
            f.write("\n")
        f.write("# wt worktree setup\n")
        for entry in missing:
            f.write(f"{entry}\n")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate .wt/setup bootstrap script for git worktree environments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --type node
  %(prog)s --agents-md --dry-run
  %(prog)s --dir /path/to/project
        """,
    )
    parser.add_argument(
        "--type",
        choices=list(TEMPLATE_FILES.keys()),
        default=None,
        help="Project type (default: auto-detect)",
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="Project directory (default: current directory)",
    )
    parser.add_argument(
        "--agents-md",
        action="store_true",
        help="Also generate .wt/AGENTS.md",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated files to stdout without writing",
    )

    args = parser.parse_args()
    project_dir = Path(args.dir).resolve()

    if not project_dir.is_dir():
        print(
            json.dumps(
                {
                    "success": False,
                    "error": f"Directory not found: {project_dir}",
                }
            )
        )
        sys.exit(1)

    try:
        # Detect or use specified type
        project_type = args.type or detect_project_type(project_dir)

        # Load template from references/
        template_file = TEMPLATE_FILES[project_type]
        setup_content = load_template(template_file)

        files_created = []
        files_modified = []

        if args.dry_run:
            files = {".wt/setup": setup_content}
            if args.agents_md:
                files[".wt/AGENTS.md"] = load_template(AGENTS_MD_TEMPLATE_FILE)

            print(
                json.dumps(
                    {
                        "success": True,
                        "data": {
                            "dry_run": True,
                            "detected_type": project_type,
                            "template_file": template_file,
                            "package_manager": (
                                detect_package_manager(project_dir)
                                if project_type == "node"
                                else None
                            ),
                            "files": files,
                            "gitignore_entries": GITIGNORE_ENTRIES,
                        },
                    },
                    indent=2,
                    default=str,
                )
            )
            return

        # Create .wt directory
        wt_dir = project_dir / ".wt"
        wt_dir.mkdir(exist_ok=True)

        # Write .wt/setup
        setup_path = wt_dir / "setup"
        setup_path.write_text(setup_content)
        setup_path.chmod(
            setup_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        )
        files_created.append(".wt/setup")

        # Write .wt/AGENTS.md if requested
        if args.agents_md:
            agents_path = wt_dir / "AGENTS.md"
            agents_path.write_text(load_template(AGENTS_MD_TEMPLATE_FILE))
            files_created.append(".wt/AGENTS.md")

        # Update .gitignore
        if update_gitignore(project_dir, dry_run=False):
            files_modified.append(".gitignore")

        print(
            json.dumps(
                {
                    "success": True,
                    "data": {
                        "detected_type": project_type,
                        "template_file": template_file,
                        "package_manager": (
                            detect_package_manager(project_dir)
                            if project_type == "node"
                            else None
                        ),
                        "files_created": files_created,
                        "files_modified": files_modified,
                    },
                },
                indent=2,
                default=str,
            )
        )

    except Exception as e:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": str(e),
                }
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
