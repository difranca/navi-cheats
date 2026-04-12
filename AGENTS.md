# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A collection of cheatsheets for [navi](https://github.com/denisidoro/navi), an interactive CLI cheatsheet tool. Cheats are organized by topic in directories (e.g., `DevSecOps/`, `Kubernetes/`) as `.cheat` files following navi's syntax.

A Python parser (`.parser/navi2md.py`) converts `.cheat` files into Markdown for publishing to a Docusaurus docs site. A GitHub Actions workflow (`.github/workflows/cheat2md.yaml`) runs this on push to `main` and pushes the generated MD to `difranca/difranca.github.io`.

## Navi Cheat File Syntax

`.cheat` files use this format:

- `% Topic > Subtopic` — topic header (hierarchical with `>`)
- `;; Description text` — description for the preceding topic
- `# Comment text` — description for the next command
- The line after `#` is the actual command
- `<variable>` — interactive variable placeholder in commands
- `$ variable: command` — variable definition (shell command that populates choices)
- `@ Topic` — dependency reference (imports variables from another topic)

The first `%` line defines the top-level cheat name. Subsequent `%` lines define subtopics.

## Directory Convention

Each top-level directory represents a category (e.g., `DevSecOps/`, `Kubernetes/`). Place new `.cheat` files in the matching category directory, creating a new one if needed. The directory name is used to derive the slug and keywords in the generated docs.

## Commands

### Run the cheat-to-markdown parser
```
python3 .parser/navi2md.py
```
This finds all `*.cheat` files recursively and generates corresponding `.md` files under a `cheats/` directory (gitignored, used by CI only).

### Validate cheat file syntax
```
python3 .parser/navi2md.py --check
```
Checks all `.cheat` files for common errors (missing topic headers, dangling command descriptions) without generating output.

### Test a cheat file locally with navi
```
navi --path <directory>
```

## Architecture

- `**/*.cheat` — navi cheatsheet source files, one per tool/topic
- `.parser/navi2md.py` — parser that reads `.cheat` files and produces Docusaurus-compatible MD
- `.parser/md.template` — Docusaurus page template (frontmatter, tabs, imports)
- `.parser/topic.template` — template for each topic section (table of command/description)
- `.github/workflows/cheat2md.yaml` — CI that parses cheats and pushes MD to the docs repo

The parser generates frontmatter with keywords and slugs derived from the file path, and renders commands in a tabbed view (table format + raw navi cheat).
