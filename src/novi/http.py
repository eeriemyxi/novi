import logging

import httpx

from novi import constants, struct

log = logging.getLogger(__name__)


def get_word_file(
    client: httpx.Client, language: struct.SupportedLanguage, word: str
) -> str | None:
    base_url = f"{constants.BASE_URL}/dictionary/{language.value}"
    log.debug(f"{base_url=}")
    resp = client.get(f"{base_url}/{word}")
    log.debug(f"{resp=}")

    if resp.status_code == 302:
        location = resp.headers.get("location")
        log.debug(f"{location=}")

        if location == base_url + "/":
            log.debug("Could not find word file for %s.", repr(word))
            return None

        log.debug(f"Redirecting to {location=}")
        resp = client.get(location)

    if resp.status_code == 200:
        return resp.content.decode()

    return None
