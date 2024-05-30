import html2text
from rich.markdown import Markdown
from rich.padding import Padding
from . import console
from .queries.fetch_question import fetch_daily, fetch_question

DIFF_COLOR = {"Easy": "green", "Medium": "yellow", "Hard": "red"}


def display_question(title_slug: str):
    def replaceSup(r: str) -> str:
        r = r.replace("<sup>", "^")
        r = r.replace("</sup>", "")
        return r

    if title_slug == "daily":
        title_slug = fetch_daily()

    question = fetch_question(title_slug=title_slug)

    diff = question["difficulty"]
    question_id = question["questionFrontendId"]
    title = question["title"]
    color = DIFF_COLOR[diff]

    console.print(
        Padding(f"[b][[{color}]{question_id}[/{color}]] [u]{title}[/u][/b]", (1, 2))
    )

    html = "\n".join(map(str, question["content"].split("\n")))
    html = replaceSup(html)
    h = html2text.HTML2Text()
    h.ignore_images = True
    h.ignore_emphasis = True
    md = h.handle(html)
    console.print(Padding(Markdown(markup=md), (1, 2)))
