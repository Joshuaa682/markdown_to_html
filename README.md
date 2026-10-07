# Markdown to HTML

A small learning project with a Python web backend. Type Markdown into the
browser, send it to Python, and see the generated HTML plus a preview.

## Run it on Windows

First, make sure PowerShell is in the project folder (the folder containing
`app.py` and `requirements.txt`). In VS Code, you can right-click the project
folder in Explorer and choose **Open in Integrated Terminal**. Or change to
the folder with `Set-Location`, replacing the example path with your project
path:

```powershell
Set-Location "C:\path\to\markdown_to_html"
```

Replace the example path with the location where you saved this project.

Then create the virtual environment, install the libraries, and start the app:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open <http://127.0.0.1:5000> in your browser. Stop the local server with
**Ctrl+C** in PowerShell.

These commands use the virtual environment's Python directly, so you do not
need to activate it or change PowerShell's script execution policy.

## How the pieces fit together

1. `templates/index.html` creates the page: a Markdown editor, HTML output,
   preview, a Convert button, and a Download HTML button.
2. `static/app.js` listens for the button, sends the editor text as JSON to
   `POST /api/convert`, puts the response on the page, and lets you download
   the latest successful conversion as `converted.html`. Edit the Markdown and
   convert it again before downloading an updated file.
3. `app.py` is the backend. Flask serves the page and receives the API request.
   The route validates and size-limits the request, converts the Markdown, then
   sanitizes the HTML before returning it.
4. `static/style.css` controls the page layout and appearance.
5. `tests/test_app.py` checks that the page loads, common Markdown features
   convert, and invalid API requests are rejected.

The path for one conversion is:

```text
Markdown editor
  -> JavaScript fetch()
  -> Flask POST /api/convert
  -> Python Markdown parser
  -> JSON response containing HTML
  -> HTML source, preview, and downloadable file in the browser
```

## Try the API directly

With the server running, this PowerShell command sends Markdown to the backend:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/convert `
  -Method Post -ContentType "application/json" `
  -Body '{"content":"# Hello`n`nThis is **bold**."}'
```

The response is JSON with an `html` field.

## Run the tests

After installing the requirements, run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Learn by changing it

- In `app.py`, add or remove a Markdown extension such as `tables`.
- In `tests/test_app.py`, add an example and assert the HTML it should produce.
- In `templates/index.html` and `static/style.css`, change the interface.
- In `static/app.js`, inspect how the browser sends a request and handles errors.

## Safety notes

- The backend sanitizes generated HTML before it reaches either the preview or
  the downloaded file. It allows common Markdown elements, links, images,
  tables, and language classes on code blocks; it removes scripts, event
  handler attributes, styles, and unsafe URL schemes.
- The preview also runs inside a sandboxed iframe.
- Requests are limited to 1 MiB, and Markdown input is limited to 100,000
  characters. The API returns a JSON error when a limit is exceeded.
- Flask debug mode is off by default. The built-in server is still only for
  local development; do not expose it directly to the internet.

These protections reduce common risks but do not by themselves make the app
production-ready. Before serving the public, use a production WSGI server behind
a properly configured HTTPS reverse proxy, add rate limiting and monitoring,
and keep Flask and its dependencies updated. Remote images and links can still
contact third-party sites when someone views or clicks them.
