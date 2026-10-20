# tracked-ignored

Find files that are tracked by git but match ignore rules or look like secrets/build artifacts, so you can stop committing things that should never be in history.

## Features

- Lists git-tracked files that `.gitignore` would ignore (the classic "committed but ignored" mistake).
- Flags obviously sensitive tracked files (`.env`, `*.pem`, `*.key`, SSH private keys, keystores).
- Flags tracked build/dependency artifacts (`node_modules`, `dist`, `build`, `*.log`, caches).
- Zero dependencies, pure Python 3.9+, works on any repo.
- Exit code non-zero when problems are found, so it can gate CI.

## Install

```sh
pip install tracked-ignored
```

Or run from source:

```sh
python -m tracked_ignored --help
```

## Usage

```sh
tracked-ignored [path] [--json]
```

Examples:

```sh
tracked-ignored .
tracked-ignored /path/to/repo --json
```

## License

MIT