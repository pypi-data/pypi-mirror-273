from languages.languages import is_a_valid_language,get_language_code,ISO_639_2

from abc import (
    ABC,
    abstractmethod,
    abstractproperty
)


class Reader(ABC):

    def __init__(self, input_path, src_lang, tgt_lang, **kwargs):
        self.input_path = input_path
        if is_a_valid_language(src_lang):
            self.src_lang = get_language_code(src_lang,iso=ISO_639_2)
        if is_a_valid_language(tgt_lang):
            self.tgt_lang = get_language_code(tgt_lang,iso=ISO_639_2)

    @abstractmethod
    def get_data(self):
        pass

__all__ = ["Reader"]
