from flask import Flask, jsonify, render_template, request
import bleach
import markdown


MAX_MARKDOWN_LENGTH = 100_000
MAX_REQUEST_BYTES = 1_048_576
ALLOWED_TAGS = {
    "a", "blockquote", "br", "code", "del", "em", "h1", "h2", "h3",
    "h4", "h5", "h6", "hr", "img", "li", "ol", "p", "pre", "strong",
    "table", "tbody", "td", "th", "thead", "tr", "ul",
}


def allowed_html_attribute(tag, name, value):
    if tag == "a" and name in {"href", "title"}:
        return True
    if tag == "img" and name in {"src", "alt", "title"}:
        return True
    if tag == "code" and name == "class":
        return value.startswith("language-") and value[9:].replace(
            "_", ""
        ).replace("-", "").replace("+", "").isalnum()
    return False


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = MAX_REQUEST_BYTES

    @app.errorhandler(413)
    def request_too_large(_error):
        return jsonify(error="The request is too large."), 413

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/api/convert")
    def convert_markdown():
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not isinstance(data.get("content"), str):
            return jsonify(error="Send a JSON object with a string 'content' field."), 400

        if len(data["content"]) > MAX_MARKDOWN_LENGTH:
            return jsonify(error="Markdown must be 100,000 characters or fewer."), 413

        html = markdown.markdown(
            data["content"],
            extensions=["fenced_code", "tables"],
        )
        html = bleach.clean(
            html,
            tags=ALLOWED_TAGS,
            attributes=allowed_html_attribute,
            protocols={"http", "https", "mailto"},
            strip=True,
            strip_comments=True,
        )
        return jsonify(html=html)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=False)
