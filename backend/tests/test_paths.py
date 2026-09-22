"""File routes must never serve anything outside the frontend build or a run's own folder."""

import unittest

from fastapi.testclient import TestClient

from deskapp.api import app

SPA_MARKER = '<div id="root">'


class PathContainment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ctx = TestClient(app)
        cls.client = cls.ctx.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.__exit__(None, None, None)

    def test_spa_routes_serve_index(self):
        for path in ("/", "/runs", "/runs/some-id"):
            res = self.client.get(path)
            self.assertEqual(res.status_code, 200)
            self.assertIn(SPA_MARKER, res.text)

    def test_spa_traversal_falls_back_to_index(self):
        for path in ("/..%2f..%2fbackend%2fdeskapp%2fsettings.py", "/%2e%2e/%2e%2e/.gitignore", "/..\\..\\README.md"):
            res = self.client.get(path)
            self.assertNotIn("KEYS_FILE", res.text)
            self.assertNotIn(".venv/", res.text)
            if res.status_code == 200:
                self.assertIn(SPA_MARKER, res.text)

    def test_run_files_traversal_blocked(self):
        runs = self.client.get("/api/runs").json()["runs"]
        if not runs:
            self.skipTest("no runs recorded yet")
        run_id = runs[0]["id"]
        for path in ("..%2f..%2fdesk.db", "../../desk.db", "..%5c..%5cdesk.db"):
            res = self.client.get(f"/api/runs/{run_id}/files/{path}")
            self.assertIn(res.status_code, (404, 400))


if __name__ == "__main__":
    unittest.main()
