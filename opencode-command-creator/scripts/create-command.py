#!/usr/bin/env python3
"""
Create OpenCode custom command files.

This script generates OpenCode command markdown files with proper structure
and frontmatter configuration.

Usage:
    ./create-command.py <command-name> [options]

Examples:
    ./create-command.py test --description "Run tests" --global
    ./create-command.py component --agent code --template "Create component $ARGUMENTS"
    ./create-command.py review --subtask --model "anthropic/claude-sonnet-4-5"
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional


def create_command_file(
    name: str,
    template: str,
    description: Optional[str] = None,
    agent: Optional[str] = None,
    model: Optional[str] = None,
    subtask: bool = False,
    global_cmd: bool = False,
    output_dir: Optional[str] = None,
) -> Path:
    """
    Create OpenCode command markdown file.

    Args:
        name: Command name (without leading /)
        template: Command template/prompt content
        description: Brief description for TUI
        agent: Agent to execute command
        model: Model override
        subtask: Force subagent invocation
        global_cmd: Create in global config directory
        output_dir: Custom output directory

    Returns:
        Path to created file

    Raises:
        FileNotFoundError: If output directory doesn't exist
        PermissionError: If cannot write to directory
    """
    # Determine output directory
    if output_dir:
        base_dir = Path(output_dir)
    elif global_cmd:
        base_dir = Path.home() / ".config" / "opencode" / "commands"
    else:
        base_dir = Path(".opencode") / "commands"

    # Create directory if it doesn't exist
    base_dir.mkdir(parents=True, exist_ok=True)

    # Build frontmatter
    frontmatter = {}
    if description:
        frontmatter["description"] = description
    if agent:
        frontmatter["agent"] = agent
    if model:
        frontmatter["model"] = model
    if subtask:
        frontmatter["subtask"] = subtask

    # Build file content
    content_parts = ["---"]

    if frontmatter:
        for key, value in frontmatter.items():
            if isinstance(value, bool):
                content_parts.append(f"{key}: {str(value).lower()}")
            else:
                content_parts.append(f"{key}: {value}")

    content_parts.extend(["---", "", template, ""])

    content = "\n".join(content_parts)

    # Write file
    file_path = base_dir / f"{name}.md"
    file_path.write_text(content, encoding="utf-8")

    return file_path


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create OpenCode custom command files",
        epilog="""
Examples:
  %(prog)s test --description "Run tests" --global
  %(prog)s component --agent code --template "Create component $ARGUMENTS"
  %(prog)s review --subtask --model "anthropic/claude-sonnet-4-5"
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "name",
        help="Command name (without leading /)",
    )

    parser.add_argument(
        "-t",
        "--template",
        help="Command template/prompt (default: placeholder)",
        default="TODO: Add command template here.\n\nUse $ARGUMENTS for user input.",
    )

    parser.add_argument(
        "-d",
        "--description",
        help="Brief description shown in TUI",
    )

    parser.add_argument(
        "-a",
        "--agent",
        help="Agent to execute command",
    )

    parser.add_argument(
        "-m",
        "--model",
        help="Model override (e.g., anthropic/claude-sonnet-4-5)",
    )

    parser.add_argument(
        "-s",
        "--subtask",
        action="store_true",
        help="Force subagent invocation",
    )

    parser.add_argument(
        "-g",
        "--global",
        action="store_true",
        dest="global_cmd",
        help="Create in global config (~/.config/opencode/commands/)",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Custom output directory",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON config instead of markdown file",
    )

    args = parser.parse_args()

    try:
        if args.json:
            # Generate JSON config
            config = {
                "command": {
                    args.name: {
                        "template": args.template,
                    }
                }
            }

            if args.description:
                config["command"][args.name]["description"] = args.description
            if args.agent:
                config["command"][args.name]["agent"] = args.agent
            if args.model:
                config["command"][args.name]["model"] = args.model
            if args.subtask:
                config["command"][args.name]["subtask"] = True

            print(json.dumps(config, indent=2))
            return 0

        # Create markdown file
        file_path = create_command_file(
            name=args.name,
            template=args.template,
            description=args.description,
            agent=args.agent,
            model=args.model,
            subtask=args.subtask,
            global_cmd=args.global_cmd,
            output_dir=args.output,
        )

        print(
            json.dumps(
                {
                    "status": "success",
                    "file": str(file_path),
                    "command": f"/{args.name}",
                    "message": f"Created command file: {file_path}",
                }
            )
        )
        return 0

    except Exception as e:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": str(e),
                    "type": type(e).__name__,
                }
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
