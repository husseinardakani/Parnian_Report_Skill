"""Check Codex app-server discovery from independent project directories."""
import argparse
import json
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--with-upstream", action="store_true")
args = parser.parse_args()
expected = {"parnian-enterprise-reporting"}
if args.with_upstream:
    expected.update(("semantic-model-authoring", "powerbi-report-cli"))

with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
    processes = subprocess.Popen(
        ["codex", "app-server"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL, text=True,
    )
    try:
        def send(message):
            processes.stdin.write(json.dumps(message) + "\n")
            processes.stdin.flush()

        def result_for(request_id):
            for line in processes.stdout:
                reply = json.loads(line)
                if reply.get("id") == request_id:
                    if "error" in reply:
                        raise RuntimeError(reply["error"])
                    return reply["result"]
            raise RuntimeError("Codex app-server exited before replying")

        send({"id": 1, "method": "initialize",
              "params": {"clientInfo": {"name": "parnian-validation", "version": "1"}}})
        result_for(1)
        send({"method": "initialized"})
        send({"id": 2, "method": "skills/list",
              "params": {"cwds": [first, second], "forceReload": True}})
        results = result_for(2)["data"]
        assert len(results) == 2, results
        for project in results:
            names = {skill["name"] for skill in project["skills"] if skill.get("enabled", True)}
            assert expected <= names, (project["cwd"], expected - names, project.get("errors"))
            print(project["cwd"], sorted(expected))
    finally:
        processes.terminate()
        processes.wait(timeout=10)
