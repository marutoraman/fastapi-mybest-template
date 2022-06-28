from sudachipy import tokenizer
from core.language_analyer import tokenize, SudachiDictType


def test_tokenize():
    res = tokenize("関西国際空港", tokenizer.Tokenizer.SplitMode.C)
    print(res)

    assert res

    res = tokenize("関西国際空港", tokenizer.Tokenizer.SplitMode.B)
    print(res)

    assert res

    res = tokenize("関西国際空港", tokenizer.Tokenizer.SplitMode.A)
    print(res)

    assert res


def test_tokenize_ditc_type():
    res = tokenize("関西国際空港", tokenizer.Tokenizer.SplitMode.C, SudachiDictType.CORE)
    print(res)

    assert res

    res = tokenize("関西国際空港", tokenizer.Tokenizer.SplitMode.C, SudachiDictType.FULL)
    print(res)

    assert res

    res = tokenize("関西国際空港", tokenizer.Tokenizer.SplitMode.C, SudachiDictType.SMALL)
    print(res)

    assert res
