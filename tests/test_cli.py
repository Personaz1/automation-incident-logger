import subprocess

def test_summary_smoke(tmp_path):
    subprocess.check_call(["python3", "-m", "ailogger.cli", "summary", "--out", str(tmp_path / "w.md")])
