from . import con, console
from .queries.fetch_all_problems import (
    fetch_all_problems_count,
    fetch_all_problems_metadata,
    fetch_all_problems_tags,
)


def update_cache():
    count = fetch_all_problems_count()

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS metadata")
    cur.execute(
        "CREATE TABLE metadata(frontend_id INTEGER PRIMARY KEY, "
        "id INTEGER, title TEXT, title_slug TEXT, difficulty TEXT, paid INTEGER)"
    )

    # cur.execute("DROP TABLE IF EXISTS content")
    # cur.execute("CREATE TABLE content(frontend_id INTEGER PRIMARY KEY, content TEXT)")

    cur.execute("DROP TABLE IF EXISTS tags")
    cur.execute(
        "CREATE TABLE tags(frontend_id INTEGER, tags TEXT, "
        "PRIMARY KEY (frontend_id, tags))"
    )

    with console.status(status="Fetching metadata...", spinner="monkey"):
        metadata = fetch_all_problems_metadata(count=count)

    for data in metadata:
        cur.execute(
            "INSERT INTO metadata VALUES (?, ?, ?, ?, ?, ?)", list(data.values())
        )

    # with console.status(status="Fetching problem statements...", spinner="monkey"):
    #     content = fetch_all_problems_content(count=count)

    # for data in content:
    #     cur.execute("INSERT INTO content VALUES(?, ?)", list(data.values()))

    with console.status(status="Fetching tags...", spinner="monkey"):
        tags = fetch_all_problems_tags(count=count)

    for data in tags:
        tag_list = []
        for tag_map in data["topicTags"]:
            tag_list.append(tag_map["name"])

        for tag in tag_list:
            cur.execute(
                "INSERT INTO tags VALUES(?, ?)", [data["questionFrontendId"], tag]
            )

    con.commit()
