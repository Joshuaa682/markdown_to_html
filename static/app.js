const form = document.querySelector("#converter-form");
const markdownInput = document.querySelector("#markdown-input");
const htmlOutput = document.querySelector("#html-output");
const preview = document.querySelector("#preview");
const status = document.querySelector("#status");
const downloadButton = document.querySelector("#download-button");

let convertedHtml = "";

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  status.textContent = "Converting…";
  downloadButton.disabled = true;

  try {
    const response = await fetch("/api/convert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: markdownInput.value }),
    });
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "The conversion request failed.");
    }

    htmlOutput.textContent = result.html;
    preview.srcdoc = result.html;
    convertedHtml = result.html;
    downloadButton.disabled = false;
    status.textContent = "Conversion complete.";
  } catch (error) {
    status.textContent = error.message;
  }
});

markdownInput.addEventListener("input", () => {
  downloadButton.disabled = true;
  status.textContent = "Markdown changed. Convert again before downloading.";
});

downloadButton.addEventListener("click", () => {
  const documentHtml = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Converted Markdown</title>
  </head>
  <body>
${convertedHtml}
  </body>
</html>`;
  const file = new Blob([documentHtml], { type: "text/html;charset=utf-8" });
  const url = URL.createObjectURL(file);
  const link = document.createElement("a");

  link.href = url;
  link.download = "converted.html";
  link.click();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
});
