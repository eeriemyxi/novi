import logging
import pathlib
import re

from novi import struct

log = logging.getLogger(__name__)

BASE_URL = "https://dictionary.cambridge.org"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/74.0.3729.169 Safari/537.36"
)
CODES_LINK = "https://dictionary.cambridge.org/help/codes.html"
SCRIPT_DIR = pathlib.Path(__file__).parent
WORD_CLASS_RE = re.compile(r"\W*(?P<word>\w*)\W*?(?:\[?\W*?(?P<code>\w)\W*?\])?")
LANGUAGE = struct.SupportedLanguage.ENGLISH

log.debug(f"{LANGUAGE=}")
