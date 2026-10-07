import unittest

from app import create_app


class ConverterTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Markdown to HTML", response.data)

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


if __name__ == "__main__":
    unittest.main()
