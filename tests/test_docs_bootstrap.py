from __future__ import annotations

from pathlib import Path

from helpers import invoke_cli, plain_output


def test_init_creates_docs_contract(runner, in_repo: Path) -> None:
    result = invoke_cli(runner, ["init"])

    assert result.exit_code == 0
    assert "Bootstrap complete." in plain_output(result)
    assert (in_repo / "docs" / "llm" / "AGENT_PROTOCOL.md").is_file()
    assert (in_repo / "docs" / "llm" / "templates" / "spec.md").is_file()
    assert (in_repo / "docs" / "llm" / "templates" / "acceptance.feature").is_file()
    assert (in_repo / "docs" / "ideas" / "README.md").is_file()
    assert (in_repo / "docs" / "roadmap" / "README.md").is_file()
    assert (in_repo / "docs" / "specs").is_dir()
    assert (in_repo / "docs" / "plans").is_dir()
    assert (in_repo / "docs" / "adr").is_dir()
    assert (in_repo / "docs" / "ideas").is_dir()
    assert (in_repo / "docs" / "roadmap").is_dir()
    assert not (in_repo / "docs" / "changelog").exists()


def test_init_does_not_overwrite_existing_docs(runner, in_repo: Path) -> None:
    docs_readme = in_repo / "docs" / "README.md"
    docs_readme.parent.mkdir(parents=True)
    docs_readme.write_text("custom docs\n", encoding="utf-8")

    result = invoke_cli(runner, ["init"])

    assert result.exit_code == 0
    assert docs_readme.read_text(encoding="utf-8") == "custom docs\n"
    assert "already exists, skipped" in plain_output(result)


def test_init_creates_ideas_and_roadmap_readmes_with_expected_topics(runner, in_repo: Path) -> None:
    invoke_cli(runner, ["init"])

    ideas_readme = (in_repo / "docs" / "ideas" / "README.md").read_text(encoding="utf-8")
    roadmap_readme = (in_repo / "docs" / "roadmap" / "README.md").read_text(encoding="utf-8")

    assert "Ideas are early" in ideas_readme
    assert "Now / Next / Later" in roadmap_readme


def test_init_workspace_creates_workspace_config(runner, in_repo: Path) -> None:
    result = invoke_cli(runner, ["init", "--workspace"])

    assert result.exit_code == 0
    workspace_config = in_repo / ".adrlane" / "workspace.yaml"
    assert workspace_config.is_file()
    content = workspace_config.read_text(encoding="utf-8")
    assert "project_docs: docs" in content
    assert "repo_roots" in content


def test_init_without_workspace_flag_does_not_create_workspace_config(
    runner, in_repo: Path
) -> None:
    invoke_cli(runner, ["init"])

    assert not (in_repo / ".adrlane" / "workspace.yaml").exists()
