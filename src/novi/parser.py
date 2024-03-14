import io
import logging
import typing

import selectolax

from novi import constants, struct

log = logging.getLogger(__name__)


def parse_word_class(cls_text: str) -> struct.WordClass | None:
    match = constants.WORD_CLASS_RE.match(cls_text)
    if not match:
        return None

    groups = match.groups()
    if not groups:
        return None

    cls, code = groups

    log.debug(f"For {cls_text=} found {cls=} {code=}")

    return struct.WordClass(cls, code)


def parse_a_tag(base_url: str, n: selectolax.parser.Node) -> str | None:
    parsed_txt = io.StringIO()

    url = n.attributes.get("href")
    if url and "http" not in url:
        url = base_url + url[1:]

    parsed_txt.write(f"[link={url}]")
    parsed_txt.write(n.text(strip=True))
    parsed_txt.write("[/link]")
    parsed_txt.seek(0)

    return parsed_txt.read()


def parse_strong_tag(n: selectolax.parser.Node) -> str | None:
    parsed_txt = io.StringIO()

    parsed_txt.write("[bold]")
    parsed_txt.write(n.text())
    parsed_txt.write("[/bold]")
    parsed_txt.seek(0)

    return parsed_txt.read()


def parse_word_def(node: selectolax.parser.Node) -> str:
    parsed_txt = io.StringIO()

    for n in node.iter(include_text=True):
        if n.tag == "-text":
            t = n.text_content
            if t and "\n" not in t:
                parsed_txt.write(t)
            else:
                log.debug(f"Ignoring {t=} because it failed to meet the conditions")
        elif n.tag == "a":
            parsed_txt.write(parse_a_tag(constants.BASE_URL, n) or "")
        elif n.tag == "strong":
            parsed_txt.write(parse_strong_tag(n) or "")
        elif n.tag == "span":
            if n.attributes.get("class") == "b db":
                parsed_txt.write(parse_strong_tag(n) or "")
            else:
                parsed_txt.write(parse_word_def(n))

    parsed_txt.seek(0)

    return parsed_txt.read().rstrip(" :")


def parse_def_text(
    word_body: selectolax.parser.Node,
) -> typing.Iterator[struct.WordDefinition]:
    defs = word_body.css(".ddef_block")

    for df in defs:
        stripped_df = df.css_first(".ddef_d")

        log.debug(f"For {df=} found {stripped_df=}")

        if not stripped_df:
            continue

        text = parse_word_def(stripped_df)
        exm_texts = list(parse_example_text(df))

        if not text:
            continue

        yield struct.WordDefinition(text, exm_texts)


def parse_example_text(word_body: selectolax.parser.Node) -> typing.Iterator[str]:
    examps = word_body.css(".examp")

    for exm in examps:
        stripped_eg = exm.css_first(".eg")
        log.debug(f"For {exm=} found {stripped_eg=}")

        if not stripped_eg:
            continue

        text = parse_word_def(stripped_eg)

        if not text:
            continue

        yield text


def parse_definitions(html: str) -> list[struct.WordDefinition] | None:
    word_defs = []
    tree = selectolax.parser.HTMLParser(html)

    title_nodes = tree.css(".di-title")
    if not title_nodes:
        return None

    for title_node in title_nodes:
        word_name = title_node.text(strip=True)

        word_class_node = title_node.next
        word_class = (
            parse_word_class(word_class_node.text()) if word_class_node else None
        )

        title_parent = title_node.parent
        if not title_parent:
            log.debug(f"Ignoring {title_node=} because it does not have a parent.")
            continue

        word_body = title_parent.next
        if not word_body:
            log.debug(f"Ignoring {title_node=} because it does not have a body.")
            continue

        def_texts = list(parse_def_text(word_body))

        log.debug(
            f"Found word body: {word_name=} {word_class=} {word_body=} " f"{def_texts=}"
        )

        word_defs.append(
            struct.WordBody(word=word_name, word_class=word_class, def_texts=def_texts)
        )

    return word_defs
