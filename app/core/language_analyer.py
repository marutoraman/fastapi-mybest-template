from typing import Tuple, List
from enum import Enum
from sudachipy import tokenizer, dictionary, MorphemeList
from pydantic import BaseModel, Field
import time

import schemas


class SudachiDictType(Enum):
    SMALL: str = "small"
    CORE: str = "core"
    FULL: str = "full"


def tokenize(
    text: str,
    mode: tokenizer.Tokenizer.SplitMode = tokenizer.Tokenizer.SplitMode.C,
    dict_type: SudachiDictType = SudachiDictType.CORE,
    exclude_part_of_speech: list = ["助詞", "補助記号", "句点", "助動詞"],
) -> schemas.AnalyzedLanguage:
    """言語解析
    Args:
        - text: 入力テキスト
        - mode: 分割モード(Cが最もも複合語を考慮します)
        - dict_type: 辞書の種類(SMALL->CORE->FULLの順で対応する単語が多くなりますが、処理にかかる時間が増加します)
    Return:
        解析した言語情報を格納したAnalyzedLanguage形式で返します。
    """
    start = time.time()
    tokenizer_obj = dictionary.Dictionary(dict_type=dict_type.value).create()
    # mode = tokenizer.Tokenizer.SplitMode.C
    tokens: List[schemas.AnalyzedlanguageToken] = []
    excluded_tokens: List[schemas.AnalyzedlanguageToken] = []
    for tokenized_obj in tokenizer_obj.tokenize(text, mode):
        analyzed_token = schemas.AnalyzedlanguageToken(
            surface=tokenized_obj.surface(),
            dictionaly_form=tokenized_obj.dictionary_form(),
            reading_form=tokenized_obj.reading_form(),
            normalized_form=tokenized_obj.normalized_form(),
            part_of_speech=tokenized_obj.part_of_speech(),
            begin_pos=tokenized_obj.begin(),
            end_pos=tokenized_obj.end(),
        )
        if len(set(tokenized_obj.part_of_speech()) & set(exclude_part_of_speech)) != 0:
            excluded_tokens.append(analyzed_token)
        else:
            tokens.append(analyzed_token)

    return schemas.AnalyzedLanguage(
        raw_text=text,
        tokens=tokens,
        excluded_tokens=excluded_tokens,
        during_time=(time.time() - start),
    )
