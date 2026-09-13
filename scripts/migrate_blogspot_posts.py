import json
import re
import html
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
POSTS_ROOT = ROOT / "src" / "content" / "posts"

FEED_URL = "https://rumirifai.blogspot.com/feeds/posts/default?alt=json&max-results=150"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "post"


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def html_to_markdown(raw: str) -> str:
    text = html.unescape(raw)
    text = text.replace("<br>", "\n\n")
    text = text.replace("<br/>", "\n\n")
    text = text.replace("<br />", "\n\n")
    text = text.replace("</p>", "\n\n")
    text = text.replace("</div>", "\n\n")
    text = text.replace("</h1>", "\n\n")
    text = text.replace("</h2>", "\n\n")
    text = text.replace("</h3>", "\n\n")
    text = re.sub(r"<h([1-6])[^>]*>(.*?)</h\1>", lambda m: f"\n\n{'#' * int(m.group(1))} {re.sub(r'<.*?>', '', m.group(2))}\n\n", text, flags=re.S)
    text = re.sub(r"<li[^>]*>(.*?)</li>", r"- \1\n", text, flags=re.S)
    text = re.sub(r"<p[^>]*>(.*?)</p>", r"\n\n\1\n\n", text, flags=re.S)
    text = re.sub(r"<a[^>]+href=\"([^\"]+)\"[^>]*>(.*?)</a>", r"[\2](\1)", text, flags=re.S)
    text = re.sub(r"<img[^>]+src=\"([^\"]+)\"[^>]*>", r"![image](\1)", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&nbsp;", " ")
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.rstrip() for line in text.splitlines()]
    result = []
    for line in lines:
        if line.strip():
            result.append(line.strip())
    return "\n\n".join(result).strip()


def write_post(entry: dict) -> None:
    title = entry["title"]["$t"].strip()
    published = entry.get("published", {}).get("$t") or "2024-01-01T00:00:00.000Z"
    alt_link = next((l["href"] for l in entry.get("link", []) if l.get("rel") == "alternate"), "")
    raw_content = entry.get("content", {}).get("$t", "")
    clean_content = html_to_markdown(raw_content)
    if not clean_content:
        clean_content = title

    parsed = urlparse(alt_link)
    path_parts = [p for p in parsed.path.split("/") if p]
    if len(path_parts) >= 3:
        year = path_parts[0]
        month = path_parts[1]
    else:
        year = published[:4]
        month = published[5:7]

    target_dir = POSTS_ROOT / year / month
    target_dir.mkdir(parents=True, exist_ok=True)

    slug = slugify(title)
    file_path = target_dir / f"{slug}.md"
    if file_path.exists():
        return

    categories = []
    for cat in entry.get("category", []):
        term = cat.get("term")
        if term:
            categories.append(term)
    if not categories:
        categories = ["blog"]

    short_text = re.sub(r"\s+", " ", clean_content)
    description = short_text[:180].strip()
    if len(description) == 180:
        description = description[:-1].rstrip() + "…"

    frontmatter = "---\n"
    frontmatter += f"title: \"{title.replace(chr(34), '\\\"')}\"\n"
    frontmatter += f"author: Rumi Rifai\n"
    frontmatter += f"pubDatetime: {published}\n"
    frontmatter += f"description: \"{description.replace(chr(34), '\\\"')}\"\n"
    frontmatter += "tags:\n"
    for tag in categories[:5]:
        frontmatter += f"  - {tag}\n"
    if not any(tag.lower() == "blog" for tag in categories):
        frontmatter += "  - blog\n"
    frontmatter += "draft: false\n"
    if alt_link:
        frontmatter += f"canonicalURL: {alt_link}\n"
    frontmatter += "---\n\n"

    content = frontmatter + clean_content + "\n"
    file_path.write_text(content, encoding="utf-8")
    print(f"created: {file_path.relative_to(ROOT)}")


def main() -> None:
    with urlopen(FEED_URL, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))

    entries = payload.get("feed", {}).get("entry", [])
    if not entries:
        raise RuntimeError("No Blogspot entries found.")

    for entry in entries:
        write_post(entry)

    print(f"Migrated {len(entries)} Blogspot posts.")


if __name__ == "__main__":
    main()
