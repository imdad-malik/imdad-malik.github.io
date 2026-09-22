from pathlib import Path
from urllib.parse import quote
from datetime import datetime, timezone

BASE_URL = "https://imdad-malik.github.io"

ROOT = Path(".")
EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".vscode",
    "node_modules",
    "_site",
}

EXCLUDED_FILES = {
    "404.html",
}

urls = []

for path in ROOT.rglob("*.html"):
    # Skip excluded directories
    if any(part in EXCLUDED_DIRS for part in path.parts):
        continue

    # Skip excluded files
    if path.name in EXCLUDED_FILES:
        continue

    # Convert Windows/Linux path to URL path
    relative_path = path.as_posix()

    # Homepage
    if relative_path == "index.html":
        url = f"{BASE_URL}/"
    else:
        url = f"{BASE_URL}/{quote(relative_path)}"

    urls.append(url)

# Remove duplicates and sort
urls = sorted(set(urls))

lastmod = datetime.now(timezone.utc).strftime("%Y-%m-%d")

sitemap = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for url in urls:
    priority = "1.0" if url == f"{BASE_URL}/" else "0.8"

    sitemap.append("  <url>")
    sitemap.append(f"    <loc>{url}</loc>")
    sitemap.append(f"    <lastmod>{lastmod}</lastmod>")
    sitemap.append(f"    <priority>{priority}</priority>")
    sitemap.append("  </url>")

sitemap.append("</urlset>")

Path("sitemap.xml").write_text(
    "\n".join(sitemap) + "\n",
    encoding="utf-8"
)

print(f"Sitemap generated successfully with {len(urls)} URLs.")
