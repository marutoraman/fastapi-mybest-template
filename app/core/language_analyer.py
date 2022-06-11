from typing import Tuple, List
from enum import Enum
from sudachipy import tokenizer, dictionary, MorphemeList
from pydantic import BaseModel, Field
import time


class AnalyzedlanguageToken(BaseModel):
    surface: str = Field(..., description="表層形式(入力文字のまま)")
    dictionaly_form: str = Field(..., description="辞書形式")
    reading_form: str = Field(..., description="読みカナ")
    normalized_form: str = Field(..., description="正規化済の形式")
    part_of_speech: Tuple = Field(..., description="品詞")


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
    tokens: List[AnalyzedlanguageToken] = []
    for tokenized_obj in tokenizer_obj.tokenize(text, mode):
        tokens.append(
            AnalyzedlanguageToken(
                surface=tokenized_obj.surface(),
                dictionaly_form=tokenized_obj.dictionary_form(),
                reading_form=tokenized_obj.reading_form(),
                normalized_form=tokenized_obj.normalized_form(),
                part_of_speech=tokenized_obj.part_of_speech(),
            )
        )

    return AnalyzedLanguage(
        raw_text=text, tokens=tokens, during_time=(time.time() - start)
    )
