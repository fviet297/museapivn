"""Offline regressions for MUSE page readiness and video delivery waits."""
import ast
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("muse_engine_candidate", ROOT / "engine.py")
engine_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine_module)

tree = ast.parse((ROOT / "engine.py").read_text(encoding="utf-8"))
method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "_wait_ws_ready")
expression = next(n.args[0].value for n in ast.walk(method)
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "js")

for name, connecting, hydrated, disabled, expected in (
        ("empty_connected", False, True, False, "ready"),
        ("connecting", True, True, False, "connecting"),
        ("hydrating", False, False, False, "hydrating"),
        ("disabled_input", False, True, True, "input-disabled")):
    script = """const c=%s;const ta={disabled:c.disabled};const document={readyState:'complete',body:{innerText:c.connecting?'Connecting...':''},querySelector:s=>s==='textarea'?ta:s==='[data-hatch-shell-hydration-state]'?{getAttribute:()=>c.hydrated?'hydrated':'server'}:null};console.log(%s);""" % (
        json.dumps(dict(connecting=connecting, hydrated=hydrated, disabled=disabled)), expression)
    result = subprocess.check_output(["node", "-e", script], text=True).strip()
    assert result == expected, (name, result, expected)

with tempfile.TemporaryDirectory() as profile:
    engine = engine_module.MuseEngine(SimpleNamespace(profile_dir=profile, login_wait=2))
    clock = [0.0]
    engine_module.time = SimpleNamespace(time=lambda: clock[0], sleep=lambda n: clock.__setitem__(0, clock[0] + n))
    engine.page = SimpleNamespace(js=lambda _: json.dumps({
        "cnt": 0, "txt": "", "stop": True, "tail": "Still sending"}))
    engine.attachments = lambda: []
    try:
        engine._wait_attachment("", 60, "video")
    except engine_module.MuseGenerationError as exc:
        assert "chưa được gửi thành công" in str(exc)
        assert clock[0] < 32, clock[0]
    else:
        raise AssertionError("undelivered video request waited for the full timeout")

print("PASS: composer readiness and undelivered video fast-fail")
