from __future__ import annotations

from pathlib import Path, PurePosixPath

from adrlane.bootstrap.actions import BootstrapAction


def template_bootstrap_actions(target: Path) -> list[BootstrapAction]:
    """Build bootstrap actions from packaged template files."""
    actions: list[BootstrapAction] = []
    template_root = Path(__file__).resolve().parent / "templates"

    for relative_path, content in _iter_template_files(template_root):
        actions.append(
            BootstrapAction(
                path=target / relative_path,
                kind="file",
                content=content,
            )
        )

    return actions


def _iter_template_files(root: Path) -> list[tuple[PurePosixPath, str]]:
    files_found: list[tuple[PurePosixPath, str]] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = PurePosixPath(path.relative_to(root).as_posix())
        files_found.append((relative, path.read_text(encoding="utf-8")))

    return files_found
