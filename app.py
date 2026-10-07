from flask import Flask, jsonify, render_template, request
import markdown


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/api/convert")
    def convert_markdown():
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not isinstance(data.get("content"), str):
            return jsonify(error="Send a JSON object with a string 'content' field."), 400

        html = markdown.markdown(
            data["content"],
            extensions=["fenced_code", "tables"],
        )
        return jsonify(html=html)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
