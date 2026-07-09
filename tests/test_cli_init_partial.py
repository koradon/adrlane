from __future__ import annotations

from pathlib import Path

from helpers import invoke_cli, plain_output


def test_init_does_not_overwrite_existing_bootstrap_version(runner, repo: Path) -> None:
    marker_dir = repo / ".adrlane"
    marker_dir.mkdir()
    marker_file = marker_dir / "bootstrap-version"
    marker_file.write_text("9.9.9\n", encoding="utf-8")

    result = invoke_cli(runner, ["init", "--path", str(repo)])

    assert result.exit_code == 0
    assert marker_file.read_text(encoding="utf-8") == "9.9.9\n"
    assert "already exists, skipped" in plain_output(result)


def test_init_partial_structure_creates_remaining_docs(runner, repo: Path) -> None:
    (repo / "docs" / "plans").mkdir(parents=True)
    (repo / "docs" / "llm" / "TEMPLATES.md").parent.mkdir(parents=True)
    (repo / "docs" / "llm" / "TEMPLATES.md").write_text("CUSTOM\n", encoding="utf-8")

    result = invoke_cli(runner, ["init", "--path", str(repo)])

    assert result.exit_code == 0
    assert (repo / "docs" / "llm" / "TEMPLATES.md").read_text(encoding="utf-8") == "CUSTOM\n"
    assert (repo / "docs" / "llm" / "AGENT_PROTOCOL.md").is_file()
    assert "already exists, skipped" in plain_output(result)
    assert "  + " in plain_output(result)
