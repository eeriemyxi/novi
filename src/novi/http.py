import logging

import httpx

from novi.struct import SupportedLanguage

log = logging.getLogger(__name__)


def get_word_file(
    client: httpx.Client, language: SupportedLanguage, word: str
) -> str | None:
    resp = client.get(f"dictionary/{language.value}/{word}")
    log.debug(f"{resp=}")
    if resp.status_code != 200:
        log.debug("Could not find word file for %s.", repr(word))
        return None
    return resp.content.decode()
