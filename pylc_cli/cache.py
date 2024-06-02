import sqlite3
from . import BASE_DIR
from .queries.fetch_all_problems import (
    fetch_all_problems_count,
    fetch_all_problems_metadata,
    fetch_all_problems_content,
)


def update_cache():
    con = sqlite3.connect(f"{BASE_DIR}/cache.sqlite")
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS metadata")
    cur.execute(
        "CREATE TABLE metadata(frontend_id INTEGER PRIMARY KEY, "
        "id INTEGER, title TEXT, difficulty TEXT, paid INTEGER)"
    )

    cur.execute("DROP TABLE IF EXISTS content")
    cur.execute(
        "CREATE TABLE content(frontend_id INTEGER PRIMARY KEY, content TEXT, tags TEXT)"
    )

    count = fetch_all_problems_count()

    metadata = fetch_all_problems_metadata(count=count)
    content = fetch_all_problems_content(count=count)

    for data in metadata:
        cur.execute("INSERT INTO metadata VALUES (?, ?, ?, ?, ?)", list(data.values()))

    for data in content:
        tag_list = []
        for tag_map in data["topicTags"]:
            tag_list.append(tag_map["name"])

        tag_str = ", ".join(tag_list)
        data["topicTags"] = tag_str

        cur.execute("INSERT INTO content VALUES(?, ?, ?)", list(data.values()))

    con.commit()
