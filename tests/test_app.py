import unittest

from app import create_app


class ConverterTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Markdown to HTML", response.data)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["Referrer-Policy"], "no-referrer")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")

    def test_converts_markdown_with_tables_and_fenced_code(self):
        response = self.client.post(
            "/api/convert",
            json={
                "content": (
                    "# Hello\n\n"
                    "| Name | Value |\n| --- | --- |\n| answer | 42 |\n\n"
                    "```python\nprint('hi')\n```"
                )
            },
        )

        self.assertEqual(response.status_code, 200)
        html = response.get_json()["html"]
        self.assertIn("<h1>Hello</h1>", html)
        self.assertIn("<table>", html)
        self.assertIn('<code class="language-python">', html)

    def test_rejects_missing_or_non_string_content(self):
        for payload in ({}, {"content": None}, {"content": 42}):
            with self.subTest(payload=payload):
                response = self.client.post("/api/convert", json=payload)

                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())

    def test_removes_unsafe_html_and_link_attributes(self):
        response = self.client.post(
            "/api/convert",
            json={
                "content": (
                    '<script>alert("bad")</script>\n\n'
                    '[click](javascript:alert("bad"))\n\n'
                    '<img src="photo.png" onerror="alert(1)">'
                )
            },
        )

        self.assertEqual(response.status_code, 200)
        html = response.get_json()["html"]
        self.assertNotIn("<script", html)
        self.assertNotIn("javascript:", html)
        self.assertNotIn("onerror", html)
        self.assertIn("<img src=\"photo.png\">", html)

    def test_rejects_markdown_over_character_limit(self):
        response = self.client.post(
            "/api/convert",
            json={"content": "a" * 100_001},
        )

        self.assertEqual(response.status_code, 413)
        self.assertIn("error", response.get_json())

    def test_rejects_request_over_byte_limit_with_json_error(self):
        response = self.client.post(
            "/api/convert",
            data=b"x" * (1_048_576 + 1),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.get_json(), {"error": "The request is too large."})


if __name__ == "__main__":
    unittest.main()
