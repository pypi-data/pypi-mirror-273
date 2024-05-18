import re
import json
import os
import structlog

logger = structlog.getLogger(__name__)

import hashlib
from translation_readers.reader import Reader
from languages.languages import detect_language_code, ISO_639_2
from translate.storage.tmx import tmxfile


class TmxReader(Reader):

    def __init__(self, input_path, src_lang, tgt_lang, **kwargs):
        super().__init__(input_path, src_lang, tgt_lang, **kwargs)
        self.switch_lang = False
        self.parse_data()

    def parse_data(self):
        try:
            with open(self.input_path, 'r', encoding='utf-16') as reader:
                self.tmx_file = tmxfile(reader, self.src_lang, self.tgt_lang)
        except:
            with open(self.input_path, 'rb') as reader:
                self.tmx_file = tmxfile(reader, self.src_lang, self.tgt_lang)
        factor = 0.01
        patience = int(factor * len(self.tmx_file.units))
        patience = patience if len(self.tmx_file.units) <= 1000 else 100
        for node in self.tmx_file.unit_iter():
            src_tmp = detect_language_code(node.source, iso=ISO_639_2)
            tgt_tmp = detect_language_code(node.target, iso=ISO_639_2)
            if src_tmp == self.src_lang and \
                    tgt_tmp == self.tgt_lang:
                break
            if src_tmp == self.tgt_lang and \
                    tgt_tmp == self.src_lang:
                self.switch_lang = True
                break
            patience -= 1
            if patience <= 0:
                raise Exception("Please review the pair of languages")

    def get_data(self):
        for node in self.tmx_file.unit_iter():
            src_text = node.source
            tgt_text = node.target
            yield (src_text, tgt_text) if not self.switch_lang else (tgt_text, src_text)


__all__ = ["TmxReader"]
