import html2text
from rich.markdown import Markdown
from rich.padding import Padding
from . import console, con
from .queries.fetch_problem import fetch_problem_content

DIFF_COLOR = {"Easy": "green", "Medium": "yellow", "Hard": "red"}


def display_problem(id: int):
    def replaceSup(r: str) -> str:
        r = r.replace("<sup>", "^")
        r = r.replace("</sup>", "")
        return r

    res = con.execute(
        f"SELECT title, title_slug, difficulty FROM metadata WHERE frontend_id = {id}"
    )
    data = res.fetchone()
    title = data["title"]
    title_slug = data["title_slug"]
    content = fetch_problem_content(title_slug=title_slug)
    color = DIFF_COLOR[data["difficulty"]]

    res = con.execute(f"SELECT tags FROM tags WHERE frontend_id = {id}")
    data = res.fetchall()
    tags = ", ".join(d["tags"] for d in data)

    console.print(Padding(f"[b][[{color}]{id}[/{color}]] [u]{title}[/u][/b]", (1, 2)))

    html = "\n".join(map(str, content.split("\n")))
    html = replaceSup(html)
    h = html2text.HTML2Text()
    h.ignore_images = True
    h.ignore_emphasis = True
    md = h.handle(html)
    console.print(Padding(Markdown(markup=md), (0, 2)))

    console.print(Padding(f"Topics: {tags}", (1, 2)))
