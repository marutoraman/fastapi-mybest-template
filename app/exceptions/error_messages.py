from typing import Any, Optional


class BaseMessage:
    """メッセージクラスのベース"""

    text: str

    def __init__(self, param: Optional[Any] = None) -> None:
        self.param = param

    def __str__(self) -> str:
        return self.__class__.__name__


class ErrorMessage:
    """エラーメッセージクラス

    Notes:
        BaseMessagを継承することで
        Class呼び出し時にClass名がエラーコードになり、.textでエラーメッセージも取得できるため
        エラーコードと、メッセージの管理が直感的に行える。

    """

    # 共通
    class INTERNAL_SERVER_ERROR(BaseMessage):
        text = "システムエラーが発生しました、管理者に問い合わせてください"

    class FAILURE_LOGIN(BaseMessage):
        text = "ログインが失敗しました"

    class NOT_FOUND(BaseMessage):
        text = "{}が見つかりません"

    class ID_NOT_FOUND(BaseMessage):
        text = "このidは見つかりません"

    class PARAM_IS_NOT_SET(BaseMessage):
        text = "{}がセットされていません"

    class ALREADY_DELETED(BaseMessage):
        text = "既に削除済です"

    class COLUMN_NOT_ALLOWED(BaseMessage):
        text = "このカラムは指定できません"

    # ユーザー
    class ALREADY_REGISTED_EMAIL(BaseMessage):
        text = "登録済のメールアドレスです"

    class INCORRECT_CURRENT_PASSWORD(BaseMessage):
        text = "現在のパスワードが間違っています"

    class INCORRECT_EMAIL_OR_PASSWORD(BaseMessage):
        text = "メールアドレスまたはパスワードが正しくありません"

    class PERMISSION_ERROR(BaseMessage):
        text = "実行権限がありません"

    class CouldNotValidateCredentials(BaseMessage):
        text = "認証エラー"
