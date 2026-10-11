"""Exercise real subtree installation and updates using local Git fixtures."""

import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def init(repo):
    repo.mkdir()
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.name", "Installer test")
    git(repo, "config", "user.email", "installer@example.test")


with TemporaryDirectory(prefix="p3-install-") as directory:
    source = Path(directory) / "source"
    init(source)
    (source / "skills/unslop").mkdir(parents=True)
    skill = source / "skills/unslop/SKILL.md"
    skill.write_text("name: unslop\nfirst version\n")
    git(source, "add", ".")
    git(source, "commit", "-m", "feat: initial skill")

    project = Path(directory) / "project with spaces"
    init(project)
    (project / "personal.txt").write_text("keep personal content")
    git(project, "add", ".")
    git(project, "commit", "-m", "chore: initial project")
    env = dict(os.environ, P3_STACK_SOURCE=str(source))

    def install(*arguments):
        return subprocess.run(
            [str(ROOT / "install.sh"), *arguments], env=env,
            capture_output=True, text=True,
        )

    result = install("--project", str(project))
    assert result.returncode == 0, result.stdout + result.stderr
    installed = project / ".agents/skills/p3/skills/unslop/SKILL.md"
    assert installed.read_text() == skill.read_text()
    assert git(project, "ls-files", "--stage", ".agents/skills/p3/skills/unslop/SKILL.md").startswith("100644 ")
    assert not (project / ".agents/skills/p3/.git").exists()
    first_commit = git(project, "rev-parse", "HEAD")
    assert install("--project", str(project)).returncode == 0
    assert git(project, "rev-parse", "HEAD") == first_commit

    skill.write_text("name: unslop\nupdated version\n")
    git(source, "add", ".")
    git(source, "commit", "-m", "feat: update skill")
    assert install("--project", str(project)).returncode == 0
    assert installed.read_text() == skill.read_text()
    assert (project / "personal.txt").read_text() == "keep personal content"
    assert git(project, "status", "--porcelain") == ""

    installed.write_text("local unfinished edit")
    assert install("--project", str(project)).returncode != 0
    assert installed.read_text() == "local unfinished edit"
    assert install("--unknown").returncode == 2

print("Subtree install tracks real files, reruns are unchanged, and updates preserve personal content")
