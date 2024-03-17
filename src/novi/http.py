import logging

from requests.sessions import Session

from novi import constants, struct

log = logging.getLogger(__name__)


def get_word_file(
    session: Session, language: struct.SupportedLanguage, word: str
) -> str | None:
    base_url = f"{constants.BASE_URL}/dictionary/{language.value}"
    log.debug(f"{base_url=}")
    resp = session.get(f"{base_url}/{word}", allow_redirects=False)
    log.debug(f"{resp=}")

    if resp.status_code == 302:
        location = resp.headers.get("location", "")
        log.debug(f"{location=}")

        if location == base_url + "/":
            log.debug("Could not find word file for %s.", repr(word))
            return None

        log.debug(f"Redirecting to {location=}")
        resp = session.get(location, allow_redirects=True)

    if resp.status_code == 200:
        return resp.content.decode()

    return None
