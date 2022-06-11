from typing import Tuple, List
from enum import Enum
from sudachipy import tokenizer, dictionary, MorphemeList
from pydantic import BaseModel
import time


class AnalyzedlanguageToken(BaseModel):
    surface: str
    dictionaly_form: str
    reading_form: str
    part_of_speech: Tuple


class AnalyzedLanguage(BaseModel):
    raw_text: str
    tokens: List[AnalyzedlanguageToken] = []
    during_time: float


class SudachiDictType(Enum):
    SMALL: str = "small"
    CORE: str = "core"
    FULL: str = "full"


def tokenize(
    text: str,
    mode: tokenizer.Tokenizer.SplitMode = tokenizer.Tokenizer.SplitMode.C,
    dict_type: SudachiDictType = SudachiDictType.CORE,
) -> AnalyzedLanguage:
    start = time.time()
    tokenizer_obj = dictionary.Dictionary(dict_type=dict_type.value).create()
    # mode = tokenizer.Tokenizer.SplitMode.C
    tokens: List[AnalyzedlanguageToken] = []
    for tokenized_obj in tokenizer_obj.tokenize(text, mode):
        tokens.append(
            AnalyzedlanguageToken(
                surface=tokenized_obj.surface(),
                dictionaly_form=tokenized_obj.dictionary_form(),
                reading_form=tokenized_obj.reading_form(),
                part_of_speech=tokenized_obj.part_of_speech(),
            )
        )

    return AnalyzedLanguage(
        raw_text=text, tokens=tokens, during_time=(time.time() - start)
    )
