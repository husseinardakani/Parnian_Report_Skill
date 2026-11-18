"""Exercise the native installer wrappers with isolated user skill roots."""
from pathlib import Path
import subprocess
import sys
import tempfile

scripts = Path(__file__).resolve().parent
wrapper = (
    ["pwsh", "-NoProfile", "-File", str(scripts / "install.ps1")]
    if sys.platform == "win32"
    else ["bash", str(scripts / "install.sh")]
)
if sys.platform != "win32":
    subprocess.run(["bash", "-n", str(scripts / "install.sh")], check=True)
subprocess.run([*wrapper, "validate"], check=True)

with tempfile.TemporaryDirectory(prefix="parnian clean ") as tmp:
    root = Path(tmp) / "skills"
    existing = root / "ui-ux-pro-max" / "SKILL.md"
    existing.parent.mkdir(parents=True)
    original = "---\nname: ui-ux-pro-max\ndescription: Test fixture\n---\n"
    existing.write_text(original, encoding="utf-8")

    def run(action, *options, success=True):
        result = subprocess.run([*wrapper, action, "--skills-root", str(root), *options])
        assert (result.returncode == 0) == success, (action, result.returncode)
        assert existing.read_text(encoding="utf-8") == original

    run("install", "--with-upstream")
    bundle = root / "parnian-reporting"
    assert len(list(bundle.rglob("SKILL.md"))) == 3
    run("status")
    run("install", success=False)
    run("update", "--with-upstream")
    skill_doc = bundle / "parnian-enterprise-reporting" / "SKILL.md"
    original_doc = skill_doc.read_bytes()
    skill_doc.write_bytes(original_doc + b"\nLocal edit\n")
    run("uninstall", success=False)
    assert skill_doc.read_bytes().endswith(b"Local edit\n")
    skill_doc.write_bytes(original_doc)
    run("uninstall")
    assert not bundle.exists()
    other = bundle / "notes.txt"
    other.parent.mkdir()
    other.write_text("Unmanaged", encoding="utf-8")
    run("install", success=False)
    assert other.read_text(encoding="utf-8") == "Unmanaged"
