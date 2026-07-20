from __future__ import annotations

from pathlib import Path, PurePosixPath

from adrlane.bootstrap.actions import BootstrapAction

_FRAMEWORK_PREFIX = "llm/"


def template_bootstrap_actions(target: Path) -> list[BootstrapAction]:
    """Build bootstrap actions from packaged documentation template files."""
    actions: list[BootstrapAction] = []
    template_root = Path(__file__).resolve().parent / "templates" / "docs"

    for relative_path, content in iter_template_files(template_root):
        actions.append(
            BootstrapAction(
                path=target / "docs" / relative_path,
                kind="file",
                content=content,
            )
        )

    return actions


def framework_bootstrap_actions(target: Path) -> list[BootstrapAction]:
    """Build bootstrap actions for the packaged docs/llm/* contract files.

    Unlike template_bootstrap_actions, this excludes user-owned scaffold seeds
    (docs/README.md, docs/ideas/README.md, docs/roadmap/README.md) so callers
    can safely overwrite the result on upgrade.
    """
    actions: list[BootstrapAction] = []
    template_root = Path(__file__).resolve().parent / "templates" / "docs"

    for relative_path, content in iter_template_files(template_root):
        if not str(relative_path).startswith(_FRAMEWORK_PREFIX):
            continue
        actions.append(
            BootstrapAction(
                path=target / "docs" / relative_path,
                kind="file",
                content=content,
            )
        )

    return actions


def iter_template_files(root: Path) -> list[tuple[PurePosixPath, str]]:
    files_found: list[tuple[PurePosixPath, str]] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = PurePosixPath(path.relative_to(root).as_posix())
        files_found.append((relative, path.read_text(encoding="utf-8")))

    return files_found
