from __future__ import annotations

from pathlib import Path

from bootstrap_expectations import EXPECTED_DOC_FILES

from adrlane.bootstrap.templates_loader import iter_template_files, template_bootstrap_actions

_TEMPLATE_DOCS_ROOT = Path(__file__).resolve().parents[1] / "src/adrlane/bootstrap/templates/docs"


def test_iter_template_files_returns_sorted_packaged_templates() -> None:
    files = iter_template_files(_TEMPLATE_DOCS_ROOT)
    relative_paths = [str(path) for path, _content in files]

    assert relative_paths == sorted(relative_paths)
    assert "README.md" in relative_paths
    assert "llm/templates/acceptance.feature" in relative_paths


def test_iter_template_files_reads_non_empty_content() -> None:
    files = iter_template_files(_TEMPLATE_DOCS_ROOT)

    for _path, content in files:
        assert content.strip()


def test_template_bootstrap_actions_maps_templates_to_target_root(repo: Path) -> None:
    actions = template_bootstrap_actions(repo)

    assert len(actions) == len(EXPECTED_DOC_FILES)
    assert all(action.kind == "file" for action in actions)

    for relative_path in EXPECTED_DOC_FILES:
        assert any(action.path == repo / relative_path for action in actions)


def test_template_bootstrap_actions_preserves_template_content(repo: Path) -> None:
    source_by_relative = {
        str(relative): content for relative, content in iter_template_files(_TEMPLATE_DOCS_ROOT)
    }
    actions = template_bootstrap_actions(repo)

    for action in actions:
        relative = action.path.relative_to(repo).as_posix()
        docs_relative = relative.removeprefix("docs/")
        assert action.content == source_by_relative[docs_relative]
