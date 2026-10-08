import json
import pathlib
import re
import subprocess

root = pathlib.Path(__file__).resolve().parent
report = (root / "TASK-261002-36s1fj_panel-verdict.md").read_text()
blocks = re.findall(r"^```verdict-findings\n(.*?)\n```$", report, re.M | re.S)
assert len(blocks) == 1
packet = json.loads(blocks[0])
assert set(packet) == {"findings", "notes", "surface_results", "free_hunt"}
assert len(packet["surface_results"]) == 1
assert packet["surface_results"][0]["row"] == "goal activity publisher"
assert packet["surface_results"][0]["result"] == "broken"
assert packet["free_hunt"] == []
assert report.splitlines()[2] == "changes_requested"
for finding in packet["findings"]:
    assert set(finding) == {
        "id", "row", "invariant", "mechanism", "reproductions", "severity", "repeat-of",
    }
    assert finding["severity"] in {"bypass", "regression", "robustness", "note"}
    assert finding["repeat-of"] == "none"
    assert finding["row"] == "goal activity publisher"
    assert finding["reproductions"]
    for reproduction in finding["reproductions"]:
        assert all(reproduction[key] for key in (
            "test_file", "command", "expected_failure", "pinned_blobs",
        ))
        assert (root / reproduction["test_file"]).is_file()

expected_tree = "4d289590739432aa55c2a3868c2b4a5472b07c92"
actual_tree = subprocess.check_output(
    ["git", "rev-parse", "016a4248cf1984b97e786ce8573ad40c9438dfbf^{tree}"],
    text=True,
).strip()
assert actual_tree == expected_tree
identity = json.loads((root / "TASK-261002-36s1fj_ci-identity.json").read_text())
assert identity["source_tree"] == expected_tree
assert set(identity["jobs"]) == {"lint", "small", "core", "app-server"}
assert all(result == "success" for result in identity["jobs"].values())
print("PASS: one valid verdict-findings block; 1/1 surface row; pinned source identity; four successful hosted lane statuses.")
print("Expected-red static path witness is not represented as a passing runtime test.")
