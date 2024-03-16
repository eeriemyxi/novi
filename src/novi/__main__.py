import argparse
import importlib.metadata

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="Enable debug logs.", action="store_true")
parser.add_argument(
    "-V",
    "--version",
    help="Show program version.",
    action="version",
    version=importlib.metadata.version("novi"),
)
parser.add_argument(
    "words",
    help=(
        "Words to search. "
        "You can specify multiple words by splitting them by whitespace."
    ),
    nargs="*",
)

cli_args = parser.parse_args()

import logging  # noqa: E402
import logging.config  # noqa: E402

import httpx  # noqa: E402
import rich  # noqa: E402
from rich.logging import RichHandler  # noqa: E402

logging.getLogger("httpx").setLevel(
    logging.WARNING if not cli_args.debug else logging.DEBUG
)
logging.basicConfig(
    format="%(message)s",
    datefmt="[%X]",
    level=logging.DEBUG if cli_args.debug else logging.INFO,
    handlers=[RichHandler()],
)


from novi import constants, http, parser, util  # noqa: E402

log = logging.getLogger(__name__)


def exit_gracefully(httpx_client: httpx.Client, code: int) -> None:
    httpx_client.close()
    exit(code)


def handle_word(console: rich.console.Console, client: httpx.Client, word: str) -> int:
    util.inform_searching_word(console, word)

    word_html = http.get_word_file(client, constants.LANGUAGE, word)
    if not word_html:
        util.inform_invalid_word(console, word)
        return 1

    util.inform_found_word(console, word)

    word_defs = parser.cambridge.parse_definitions(word_html)
    if not word_defs:
        log.debug(f"Could not parse word definitions for {word=}")
        return 1

    for df in word_defs:
        if not df.def_texts:
            continue
        util.output_word(console, word, "")
        if df.word_class:
            util.output_word_class(console, df.word_class, "")
        for dt in df.def_texts:
            util.output_word_def(console, dt.text, 4)
            for exm in dt.examples:
                util.output_def_example(console, exm, 8)

    return 0


def main() -> tuple[int, httpx.Client]:
    client = httpx.Client(
        base_url=constants.BASE_URL, headers={"user-agent": constants.USER_AGENT}
    )
    console = rich.console.Console(theme=constants.RICH_THEME)

    words = cli_args.words

    for word in words:
        code = handle_word(console, client, word)
        log.debug(f"Returned {code=} for `handle_word` of {word=}")

    return 0, client


def _main() -> None:
    """Run main and exit gracefully."""
    # NOTE: this exists because rye prints the return value of `main`
    # so I had to create a silent one. If you know a better way,
    # feel free to send a pull request.
    code, client = main()
    exit_gracefully(client, code)


if __name__ == "__main__":
    _main()
