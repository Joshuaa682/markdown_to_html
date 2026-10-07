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
   The route checks that `content` is a string, then asks the Markdown library
   to turn it into HTML.
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

The preview uses a sandboxed iframe so scripts from Markdown input cannot run
inside the preview. The HTML output is still raw generated HTML: treat it as
untrusted, and do not deploy this learning app as a public service without
adding input limits, HTML sanitization, and production server configuration.
