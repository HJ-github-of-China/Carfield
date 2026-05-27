from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from uuid import UUID, uuid4


class RunMode(str, Enum):
    interactive = "interactive"
    print = "print"


class PermissionMode(str, Enum):
    default = "default"
    plan = "plan"
    bypass = "bypass"


@dataclass(frozen=True)
class AppConfig:
    mode: RunMode
    cwd: Path
    model: str
    permission_mode: PermissionMode
    debug: bool = False
    config_file: Path | None = None
    prompt: str | None = None


@dataclass(frozen=True)
class RuntimeContext:
    config: AppConfig
    session_id: UUID
    config_dir: Path
    data_dir: Path
    log_dir: Path
    is_tty: bool


def resolve_cwd(raw_cwd: str | None) -> Path:
    cwd = Path(raw_cwd).expanduser() if raw_cwd else Path.cwd()
    resolved = cwd.resolve()
    if not resolved.exists():
        raise ValueError(f"Working directory does not exist: {resolved}")
    if not resolved.is_dir():
        raise ValueError(f"Working directory is not a directory: {resolved}")
    return resolved


def default_config_dir() -> Path:
    if os.name == "nt":
        base = os.environ.get("APPDATA")
        if base:
            return Path(base) / "carfield"
    return Path.home() / ".carfield"


def bootstrap_app(
    *,
    mode: RunMode,
    cwd: str | None,
    model: str,
    permission_mode: PermissionMode,
    debug: bool,
    config_file: str | None,
    prompt: str | None,
) -> RuntimeContext:
    resolved_cwd = resolve_cwd(cwd)
    config_path = Path(config_file).expanduser().resolve() if config_file else None
    config_dir = default_config_dir()
    data_dir = config_dir / "data"
    log_dir = config_dir / "logs"

    config_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    config = AppConfig(
        mode=mode,
        cwd=resolved_cwd,
        model=model,
        permission_mode=permission_mode,
        debug=debug,
        config_file=config_path,
        prompt=prompt,
    )

    return RuntimeContext(
        config=config,
        session_id=uuid4(),
        config_dir=config_dir,
        data_dir=data_dir,
        log_dir=log_dir,
        is_tty=sys.stdout.isatty(),
    )
