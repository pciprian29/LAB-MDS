import json
import os

def build():
    with open("LAB8/data.json") as f:
        items = json.load(f)

    lines = []
    lines.append("<html><body>")
    lines.append("<h1>My Sci-Fi List</h1>")
    lines.append("<ul>")
    for item in items:
        lines.append(f"  <li><strong>{item['title']}</strong>: {item['description']}</li>")
    lines.append("</ul>")
    lines.append("</body></html>")

    os.makedirs("LAB8/site", exist_ok=True)
    with open("LAB8/site/index.html", "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    build()
