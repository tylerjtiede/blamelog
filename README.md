# blamelog

> `git blame` tells you *who*. `blamelog` tells you *so what*.

`blamelog` is a command-line tool that layers analysis on top of raw git blame data to surface actionable intelligence about your codebase — identifying high-churn files, detecting test gaps, and flagging hotspots before they become problems.

---

## Features

- **Churn detection** — identifies files that are being modified repeatedly over a configurable time window
- **Test gap detection** — uses AST analysis to determine which source files lack test coverage based on actual imports, not just filename conventions
- **Hotspot reporting** — surfaces the most at-risk files across your entire repo in a single scan
- **Structured output** — JSON output for piping into other tools, Markdown for dropping into PRs or wikis, rich terminal output for humans
- **Smart caching** — incremental AST cache invalidation using git history so repeated runs stay fast

---

## Installation

```bash
pip install blamelog
```

Or install from source:

```bash
git clone https://github.com/tylerjtiede/blamelog.git
cd blamelog
pip install -e .
```

---

## Usage

### Analyze a single file

```bash
blamelog report src/auth.py
```

### Look back further than the default 30 days

```bash
blamelog report src/auth.py --days 60
```

### Scan the entire repo and surface the top hotspots

```bash
blamelog scan --top 10
```

### Output as JSON

```bash
blamelog report src/auth.py --format json
```

---

## How it works

### Churn scoring

blamelog walks your git commit history for a given file and counts how many times it was modified in the specified window. This raw count is normalized to a 0–10 scale for readability.

### Test gap detection

Rather than relying on filename conventions (which break down in real codebases), blamelog parses the AST of every test file in your repo and builds an import map — a record of which source modules each test file actually imports from. This map is used to determine whether a source file has meaningful test coverage, and is cached intelligently so only files changed since the last run are re-parsed.

### Caching

On first run, blamelog builds a full import map and writes it to `.blamelog/cache.json` alongside the current HEAD SHA. On subsequent runs, it uses git history to identify only the files that changed since the last run and re-parses those — leaving everything else untouched.

---

## Output example

```
 blamelog — src/auth.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Churn Score      ████████░░  8.2 / 10   (47 changes in 30 days)
  Test Gap         ⚠ YES       No test files import from this module
  Top Authors      Tyler Smith (61%)  Sarah Jones (28%)  Dan K. (11%)
  Last Changed     2 days ago — "fix token expiry edge case" (a3f2c1d)

  Hotspot Lines
  ┌──────┬──────────────────────────────────┬─────────────┬────────────┐
  │ Line │ Content                          │ Author      │ Age        │
  ├──────┼──────────────────────────────────┼─────────────┼────────────┤
  │  42  │ def validate_token(self, tok):   │ Tyler Smith │ 2 days ago │
  │  91  │ if user.role not in ROLES:       │ Sarah Jones │ 9 days ago │
  │ 134  │ return refresh_token(session)    │ Tyler Smith │ 2 days ago │
  └──────┴──────────────────────────────────┴─────────────┴────────────┘

⚠  High churn + test gap detected. Consider reviewing test coverage.
```

---

## Project structure

```
blamelog/
├── src/
│   └── blamelog/
│       ├── cli.py          # Entry point and argument parsing
│       ├── gitops.py       # Git interaction (blame, log, diff)
│       ├── analysis.py     # Churn scoring and test gap detection
│       ├── formatters.py   # Output formatting (text, JSON, Markdown)
│       └── models.py       # Core dataclasses
├── tests/
├── pyproject.toml
└── .github/workflows/ci.yml
```

---

## Development

```bash
git clone https://github.com/tylerjtiede/blamelog.git
cd blamelog
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

---

## Roadmap

- [ ] `blamelog scan` — repo-wide hotspot report
- [ ] Markdown and JSON output formats
- [ ] AST-based test gap detection with incremental caching
- [ ] Author attribution and contribution breakdown
- [ ] CI-friendly exit codes

---

## License

MIT
