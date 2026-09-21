import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE = Path("/data/work/render_avatar_iv_health_mental.py")


class RenderSafetyTest(unittest.TestCase):
    def test_default_invocation_never_submits_a_render(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            source = SOURCE.read_text()
            source = source.replace(
                'BASE = "https://openrouter.ai/api/v1"',
                'BASE = "http://127.0.0.1:1/api/v1"',
            )
            source = source.replace(
                '"/data/content/drafts/heygen/renders/2026-09-18-saude-mental-esporte-elite-avatar-iv-job.json"',
                repr(str(temporary / "job.json")),
            )
            source = source.replace(
                'for candidate in (pathlib.Path("/data/.env"), pathlib.Path("/data/.hermes/.env")):',
                'for candidate in ():',
            )
            script = temporary / "render.py"
            script.write_text(source)

            result = subprocess.run(
                [sys.executable, str(script)],
                env={**os.environ, "OPENROUTER_API_KEY": ""},
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "not_submitted")
        self.assertEqual(payload["reason"], "explicit_submit_required")

    def test_submit_is_blocked_until_voice_is_validated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            source = SOURCE.read_text()
            source = source.replace(
                'BASE = "https://openrouter.ai/api/v1"',
                'BASE = "http://127.0.0.1:1/api/v1"',
            )
            source = source.replace(
                '"/data/content/drafts/heygen/renders/2026-09-18-saude-mental-esporte-elite-avatar-iv-job.json"',
                repr(str(temporary / "job.json")),
            )
            script = temporary / "render.py"
            script.write_text(source)

            result = subprocess.run(
                [sys.executable, str(script), "--submit"],
                env={**os.environ, "OPENROUTER_API_KEY": "test-key"},
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

        self.assertEqual(result.returncode, 2, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["reason"], "voice_id_not_validated")


if __name__ == "__main__":
    unittest.main()
