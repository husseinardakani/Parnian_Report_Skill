"""Manage a user-scoped bundle without changing Codex configuration."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
NAME = "parnian-enterprise-reporting"
BUNDLE = "parnian-reporting"
MARKER = ".parnian-install.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def skill_name(path):
    header = path.read_text(encoding="utf-8").split("---", 2)[1]
    return re.search(r"^name: ([a-z0-9-]+)$", header, re.MULTILINE)[1]


def validate():
    skill = ROOT / ".agents" / "skills" / NAME
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    metadata = re.fullmatch(
        r"---\nname: ([a-z0-9]+(?:-[a-z0-9]+)*)\ndescription: ([^\n]+)\n---\n.+",
        text, re.DOTALL,
    )
    require(metadata and metadata[1] == NAME and len(NAME) <= 64
            and 0 < len(metadata[2]) <= 1024, "Invalid primary skill metadata")
    for doc in skill.rglob("*.md"):
        for link in re.findall(r"\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            if not link.startswith(("https://", "http://", "#")):
                target = (doc.parent / link.split("#")[0]).resolve()
                require(target.is_relative_to(skill) and target.is_file(),
                        f"Invalid reference in {doc.name}: {link}")
    for name in ("requirements", "kpi", "acceptance", "validation", "workflow"):
        require((skill / "assets" / f"{name}.md").is_file(), f"Missing {name} template")
    entries = json.loads((ROOT / "dependencies.json").read_text(encoding="utf-8"))["sources"]
    repos = set()
    for entry in entries:
        repo = entry["repository"]
        require(re.fullmatch(r"https://github\.com/[\w.-]+/[\w.-]+", repo)
                and repo not in repos, f"Invalid or duplicate repository: {repo}")
        repos.add(repo)
        require(re.fullmatch(r"[0-9a-f]{40}", entry["revision"])
                and entry["license"] and entry["requirements"]
                and entry["status"] in {"install", "skip", "separate-mcp"},
                f"Invalid manifest entry: {repo}")
        for path in entry["skills"] + entry.get("support", []):
            require(all(re.fullmatch(r"[a-zA-Z0-9_-][a-zA-Z0-9_.-]*", part)
                        for part in path.split("/")), f"Unsafe upstream path: {path}")
    return entries


def fileset(directory):
    items = {}
    for path in sorted(directory.rglob("*")):
        require(not path.is_symlink(), f"Unexpected symlink: {path}")
        if path.is_file() and path != directory / MARKER:
            items[path.relative_to(directory).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return items


def fetch(entry, destination, scratch, installed):
    checkout = scratch / "upstream"
    checkout.mkdir()
    subprocess.run(["git", "init", "-q", str(checkout)], check=True)
    git = ["git", "-C", str(checkout)]
    revision = entry["revision"]
    subprocess.run([*git, "fetch", "-q", "--depth=1", entry["repository"], revision], check=True)
    paths = entry["skills"] + entry["support"]
    tree = subprocess.check_output([*git, "ls-tree", "-rz", revision, "--", *paths])
    observed = set()
    for record in tree.decode("utf-8").rstrip("\0").split("\0"):
        meta, relative = record.split("\t", 1)
        mode, kind, blob = meta.split()
        require(mode in {"100644", "100755"} and kind == "blob", f"Unsupported Git entry: {relative}")
        require(all(re.fullmatch(r"[a-zA-Z0-9_.-]+", part) and part not in {".", ".."}
                    for part in relative.split("/")), f"Unsafe Git path: {relative}")
        if relative.endswith("/SKILL.md"):
            observed.add(relative.removesuffix("/SKILL.md"))
        if any(relative.startswith(f"{skill}/") and skill.split("/")[-1] in installed
               for skill in entry["skills"]):
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(subprocess.check_output([*git, "cat-file", "blob", blob]))
    require(observed == set(entry["skills"]), "Pinned skill registry does not match the manifest")
    for support in entry["support"]:
        require((destination / support).exists(), f"Missing pinned support path: {support}")


def manage(action, skills_root, with_upstream, entries):
    bundle = skills_root / BUNDLE
    present = os.path.lexists(bundle)
    if present:
        marker = bundle / MARKER
        require(not bundle.is_symlink() and marker.is_file() and not marker.is_symlink(),
                f"Refusing to modify an unmanaged directory: {bundle}")
        require(json.loads(marker.read_text(encoding="utf-8")) == fileset(bundle),
                f"Managed files have changed: {bundle}")
    if action == "status":
        require(present, f"No managed installation at {bundle}")
        print(bundle)
        for path in sorted(bundle.rglob("SKILL.md")):
            print(skill_name(path))
        return
    if action == "uninstall" and not present:
        return
    require(action != "install" or not present, "Already installed. Run status or update.")
    require(action != "update" or present, "Run install first.")
    skills_root.mkdir(parents=True, exist_ok=True)
    lock = skills_root / f".{BUNDLE}.lock"
    lock.mkdir()
    try:
        require(os.path.lexists(bundle) == present, "Installation changed concurrently. Retry.")
        if present:
            require(json.loads((bundle / MARKER).read_text(encoding="utf-8")) == fileset(bundle),
                    "Managed files changed during the operation.")
        with tempfile.TemporaryDirectory(prefix=f".{BUNDLE}-", dir=skills_root) as temporary:
            scratch = Path(temporary)
            original = scratch / "previous"
            if action == "uninstall":
                bundle.rename(original)
                return
            staged = scratch / "new"
            installed = set()
            for path in skills_root.rglob("SKILL.md"):
                if not path.is_relative_to(bundle):
                    try:
                        installed.add(skill_name(path))
                    except (IndexError, TypeError, UnicodeError):
                        installed.add(path.parent.name)
            installed.update(path.parent.name for path in skills_root.glob("*/SKILL.md"))
            require(NAME not in installed, f"Existing {NAME} outside the managed bundle")
            shutil.copytree(ROOT / ".agents" / "skills" / NAME, staged / NAME)
            if with_upstream:
                for entry in entries:
                    if entry["status"] == "install":
                        fetch(entry, staged / entry["repository"].rsplit("/", 1)[1],
                              scratch, installed)
            (staged / MARKER).write_text(json.dumps(fileset(staged), indent=2), encoding="utf-8")
            if present:
                bundle.rename(original)
            try:
                staged.rename(bundle)
            except OSError:
                if present:
                    original.rename(bundle)
                raise
    finally:
        lock.rmdir()
    print(bundle)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["validate", "install", "update", "status", "uninstall"])
    parser.add_argument("--skills-root", type=Path, default=Path.home() / ".agents" / "skills")
    parser.add_argument("--with-upstream", action="store_true")
    args = parser.parse_args()
    try:
        entries = validate()
        if args.action == "validate":
            print("Skill metadata, references and dependency manifest are valid.")
        else:
            manage(args.action, args.skills_root.resolve(), args.with_upstream, entries)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
