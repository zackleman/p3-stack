"""Exercise installation and reruns without changing the user's skill library."""

from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
SKILLS = {path.name: path for path in (ROOT / "skills").iterdir() if path.is_dir()}

with TemporaryDirectory(prefix="p3-install-") as directory:
    project = Path(directory) / "project with spaces"
    target = project / ".agents/skills"
    target.mkdir(parents=True)
    (target / "architect").mkdir()
    (target / "architect/keep.txt").write_text("keep directory")
    (target / "how").write_text("keep file")
    (target / "ketchup").symlink_to(ROOT / "skills/p3-bro")
    (target / "why").symlink_to(project / "missing-skill")
    preserved = {"architect", "how", "ketchup", "why"}

    def install():
        return subprocess.run(
            [str(ROOT / "install.sh"), "--project", str(project)],
            check=True, capture_output=True, text=True,
        ).stdout

    first = install()
    inodes = {name: (target / name).lstat().st_ino for name in SKILLS}
    second = install()
    assert inodes == {name: (target / name).lstat().st_ino for name in SKILLS}
    assert (target / "architect/keep.txt").read_text() == "keep directory"
    assert (target / "how").read_text() == "keep file"
    assert (target / "ketchup").readlink() == ROOT / "skills/p3-bro"
    assert (target / "why").readlink() == project / "missing-skill"
    for name, source in SKILLS.items():
        if name not in preserved:
            assert (target / name).resolve() == source
    for output in (first, second):
        assert f"linked {len(SKILLS) - len(preserved)} skills" in output
        assert "(4 skipped)" in output

    invalid = subprocess.run(
        [str(ROOT / "install.sh"), "--unknown"], capture_output=True, text=True,
    )
    assert invalid.returncode == 2

print("Installer preserves existing files and links; reruns keep every link intact")
