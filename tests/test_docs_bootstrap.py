from __future__ import annotations

from pathlib import Path

from helpers import invoke_cli, plain_output


def test_init_creates_docs_contract(runner, repo: Path) -> None:
    result = invoke_cli(runner, ["init", "--path", str(repo)])

    assert result.exit_code == 0
    assert "Bootstrap complete." in plain_output(result)
    assert (repo / "docs" / "llm" / "AGENT_PROTOCOL.md").is_file()
    assert (repo / "docs" / "llm" / "templates" / "spec.md").is_file()
    assert (repo / "docs" / "llm" / "templates" / "acceptance.feature").is_file()
    assert (repo / "docs" / "ideas" / "README.md").is_file()
    assert (repo / "docs" / "roadmap" / "README.md").is_file()
    assert (repo / "docs" / "specs").is_dir()
    assert (repo / "docs" / "plans").is_dir()
    assert (repo / "docs" / "adr").is_dir()
    assert (repo / "docs" / "ideas").is_dir()
    assert (repo / "docs" / "roadmap").is_dir()
    assert not (repo / "docs" / "changelog").exists()


def test_init_does_not_overwrite_existing_docs(runner, repo: Path) -> None:
    docs_readme = repo / "docs" / "README.md"
    docs_readme.parent.mkdir(parents=True)
    docs_readme.write_text("custom docs\n", encoding="utf-8")

    result = invoke_cli(runner, ["init", "--path", str(repo)])

    assert result.exit_code == 0
    assert docs_readme.read_text(encoding="utf-8") == "custom docs\n"
    assert "already exists, skipped" in plain_output(result)


def test_init_creates_ideas_and_roadmap_readmes_with_expected_topics(runner, repo: Path) -> None:
    invoke_cli(runner, ["init", "--path", str(repo)])

    ideas_readme = (repo / "docs" / "ideas" / "README.md").read_text(encoding="utf-8")
    roadmap_readme = (repo / "docs" / "roadmap" / "README.md").read_text(encoding="utf-8")

    assert "Ideas are early" in ideas_readme
    assert "Now / Next / Later" in roadmap_readme
