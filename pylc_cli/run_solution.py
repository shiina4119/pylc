from pathlib import Path
from rich.padding import Padding
from . import BASE_DIR, console, EXT_MAP, con
from .queries.judge import send_judge
from .queries.status import get_status


def stringify_code(file_path: str) -> str:
    if not Path(file_path).is_file():
        # TODO: handle code file generation
        raise FileNotFoundError

    with open(file_path, "r") as f:
        lines = f.readlines()

    return "".join(lines)


def run(id: int, lang: str, test: bool):
    res = con.execute(
        f"SELECT id, title_slug FROM metadata WHERE frontend_id = {id}"
    )
    data = res.fetchone()
    title_slug = data["title_slug"]
    ext = EXT_MAP[lang]

    file_path = f"{BASE_DIR}/code/{id}.{title_slug}.{lang}.{ext}"
    if not Path(file_path).is_file():
        raise FileNotFoundError

    typed_code = stringify_code(file_path=file_path)

    with console.status(status="Sending code to server...", spinner="monkey"):
        run_id = send_judge(
            title_slug=title_slug,
            id=data["id"],
            lang=lang,
            typed_code=typed_code,
            test=test
        )
        status = get_status(title_slug=title_slug, id=run_id, test=test)

    if test:
        if status["status_msg"] == "Accepted":
            if status["correct_answer"]:
                console.print(Padding("Accepted", (1, 2), style="bold green"))
            else:
                console.print(Padding("Wrong Answer", (1, 2), style="bold red"))

            console.print(Padding(
                f"Expected answer: {status["expected_code_answer"]}\n"
                f"Your answer: {status["code_answer"]}\n"
                f"stdout: {status["code_output"]}",
                (0, 2, 1, 2)
            ))

        elif status["status_msg"] == "Runtime Error":
            console.print(Padding("Runtime Error", (1, 2), style="bold red"))
            console.print(Padding(status["runtime_error"], (0, 2, 1, 2)))
        
        elif status["status_msg"] == "Compile Error":
            console.print(Padding("Compile Error", (1, 2), style="bold red"))
            console.print(Padding(status["compile_error"], (0, 2, 1, 2)))            

    else:
        if status["status_msg"] == "Accepted":
            console.print(Padding(status["status_msg"], (1, 2), style="bold green"))
            console.print(Padding(
                f"Runtime: {status["status_runtime"]} "
                f"beats {round(status["runtime_percentile"], 2)}% of users "
                f"using {status["pretty_lang"]}.\n"
                f"Memory: {status["status_memory"]} "
                f"beats {round(status["memory_percentile"], 2)}% of users "
                f"using {status["pretty_lang"]}.",
                (0, 2, 1, 2)
            ))

        else:
            console.print(
                Padding(status["status_msg"], (1, 2), style="bold red")
            )
            if status["status_msg"] == "Wrong Answer":
                console.print(Padding(
                    f"Last testcase: {status["input_formatted"]}\n"
                    f"Expected Answer: {status["expected_output"]}\n"
                    f"Your Answer: {status["code_output"]}",
                    (0, 2, 1, 2)
                ))

            elif status["status_msg"] == "Runtime Error":
                console.print(Padding(status["full_runtime_error"], (1, 2)))

            elif status["status_msg"] == "Compile Error":
                console.print(Padding(status["full_compile_error"], (1, 2)))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("id", type=int)
    parser.add_argument("lang", choices=EXT_MAP.keys())
    parser.add_argument("test", type=bool)
    args = parser.parse_args()

    run(args.titleslug, args.lang, args.test)
