import http.client
import json
import threading
import unittest

from ais.app import create_server


class AppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        connection.request(method, path, body, headers or {})
        response = connection.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        connection.close()
        return result

    def test_page_and_assets_are_served_without_exposing_repository_files(self):
        for path in ["/", "/app.js", "/reader.mjs", "/app.css", "/icon.svg"]:
            status, headers, body = self.request("GET", path)
            self.assertEqual(status, 200)
            self.assertTrue(body)
            self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
        for path in [
            "/../data/episodes.jsonl",
            "/.git/config",
            "/README.md",
            "/data/collection/cases.jsonl",
            "/data/collection/m007/cases.jsonl",
            "/sources/report.pdf",
        ]:
            self.assertEqual(self.request("GET", path)[0], 404)

    def test_catalog_and_real_search_round_trip(self):
        status, _, body = self.request("GET", "/api/catalog")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["total"], 17)
        payload = json.dumps(dict(text="packaging logistics", cutoff="2023-01-27"))
        status, _, body = self.request(
            "POST", "/api/search", payload, {"Content-Type": "application/json"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["status"], "candidates")

    def test_bad_json_invalid_dates_and_unknown_source_return_actionable_errors(self):
        for payload in [
            "{",
            "[]",
            json.dumps(dict(text="packaging", cutoff="bad")),
            json.dumps(dict(text="packaging", cutoff="2023-01-27", source_id="missing")),
        ]:
            status, _, body = self.request(
                "POST", "/api/search", payload, {"Content-Type": "application/json"}
            )
            self.assertEqual(status, 400)
            self.assertIn("error", json.loads(body))
            self.assertNotIn("Traceback", body.decode())

    def test_validation_error_names_the_field_for_accessible_recovery(self):
        payload = json.dumps(
            dict(text="packaging", cutoff="2023-01-27", before_period_end="2024-01-01")
        )
        status, _, body = self.request(
            "POST", "/api/search", payload, {"Content-Type": "application/json"}
        )
        self.assertEqual(status, 400)
        error = json.loads(body)
        self.assertEqual(error["field"], "before_period_end")
        self.assertIn("earlier end date", error["error"])

    def test_cross_origin_wrong_media_type_and_oversize_requests_are_rejected(self):
        self.assertEqual(self.request("GET", "/", headers={"Host": "evil.example"})[0], 403)
        self.assertEqual(
            self.request("GET", "/api/catalog", headers={"Origin": "https://evil.example"})[0], 403
        )
        self.assertEqual(self.request("POST", "/api/search", "{}")[0], 415)
        self.assertEqual(
            self.request("POST", "/api/search", "x" * 20000, {"Content-Type": "application/json"})[
                0
            ],
            413,
        )


if __name__ == "__main__":
    unittest.main()
