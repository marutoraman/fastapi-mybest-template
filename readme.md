FastAPI-実用的テンプレート(FastAPI Template)
====
This is a practical template using FastAPI.   
It is dockerized including DB (MySQL) and uvicorn.  
Package management and task runner are implemented using poetry.  
We apologize for the inconvenience.   
The following text is in Japanese only.   
Please use automatic translation, etc.  
  
FastAPIを使用した実用的なテンプレートです。  
DB(MySQL)とuvicornを含めてdocker化しています。  
poetryを使用して、パッケージ管理およびタスクランナーを実装しています。


# デモ環境(heroku)
本リポジトリに、herokuにデプロイするための設定ファイルも含まれています。  
デプロイ済の環境は以下から参照できます。
```
https://fastapi-sample-tk.herokuapp.com/docs
```

DB定義(dbdocs)
```
https://dbdocs.io/marutoraman/fastapi-sample?table=jobs&schema=public&view=table_structure
```

# 機能(Features)
## パッケージ管理、タスクランナー管理
poetryおよびpoeを使用してパッケージやタスクランナーを管理しています。  
詳しい定義内容は、pyproject.tomlを参照してください。  
[tool.poe.tasks] セクションにタスクランナーを定義しています。

## DBレコードの作成・取得・更新・削除(CRUD)
crud/base.py にCRUDの共通Classを実装しています。  
個別のCRUD実装時は、この共通Classを継承して個別処理を実装してください。

## 論理削除のCRUD管理
DBレコード削除時に実際には削除せずdeleted_atに削除日付をセットすることで  
論理削除を実装しています。

以下のようにSQLAlchemyのevent機能を使用して、ORM実行後に自動的に論理削除レコードを除外するためのfilterを追加しています。  
これにより、個別のCRUDで論理削除を実装する必要がなくなります。  
include_deleted=Trueとすると、論理削除済レコードも取得できます。
```python
@event.listens_for(Session, "do_orm_execute")
def _add_filtering_deleted_at(execute_state):
    """
    論理削除用のfilterを自動的に適用する
    以下のようにすると、論理削除済のデータも含めて取得可能
    query(...).filter(...).execution_options(include_deleted=True)
    """
    logger.info(execute_state)
    if (
        not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(
                ModelBase,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )

```
## 権限(scopes)
特定のUserのみが実行できるAPIを作成する場合は、  
tableの user.scopes の値とrouterに指定したscopeを一致させてください。

```python
@router.get(
    "/{id}",
    response_model=schemas.UserResponse,
    dependencies=[Security(get_current_user, scopes=["admin"])],
)
```

## キャメルケースとスネークケースの相互変換
Pythonではスネークケースが標準ですが、Javascriptではキャメルケースが標準なため  
単純にpydanticでschemaを作成しただけでは、jsonレスポンスにスネークケースを使用せざるをえない問題があります。  

そこで、humpsをinstallして、自動的にスネークケースに変換するように  
以下のようなBaseSchemaを作成しています。  
このBaseSchemaを継承することで、簡単にキャメルケースとスネークケースの相互変換が実現できます。

```python
class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
```

## バッチ処理(batch)
サブディレクトリ配下のpyファイルから、別ディレクトリのファイルをimportする場合は  
その前に以下のコードを記述する必要があります。

```python
sys.path.append(str(Path(__file__).absolute().parent.parent))
```

batch/__set_base_path__.py に記述し、各ファイルの先頭でimportすることで  
より簡単にimportできるようにしています。


## Settings
core/config.py にて、BaseSettingsを継承して共通設定Classを定義しています。  
.envファイルから自動的に設定を読み込むことができる他、個別に設定を定義することもできます。

## ErrorException
exceptions/error_messages.py にエラーメッセージを定義しています。  
APIExceptionと併せて以下のように、呼び出すことで、任意のHTTPコードのエラーレスポンスを作成できます。
```python
raise APIException(ErrorMessage.ID_NOT_FOUND)
```

## logging
logger_config.yaml でlogging設定を管理しています。

## テスト
tests/ 配下に、テスト関連の処理を、まとめています。

テスト関数の実行毎にDBをクリーンするため、ステートレスなテストが実行できます。  
tests/test_data/ 配下でテスト用のデータを定義してください。

## ログの集中管理
.envファイルのSENTRY_SDK_DNSを設定すると、error以上のloggingが発生した場合に  
sentryに自動的にloggingされます。

## DBマイグレーション
alembic/versions.py にマイグレーション情報を記述すると、DBマイグレーション(移行)を実施することができます。  
以下を実行することで、modelsの定義と実際のDBとの差分から自動的にマイグレーションファイルを作成できます。
```bash
poe makemigrations
```

以下を実行することで、マイグレーションが実行できます。
```bash
poe migrate
```

## CI/CD
push時に、Github Actionsを使用して、ECSに自動デプロイを行うためのサンプルを記述しています。  
以下にAWSの設定情報等をセットします。  
.aws/ecs-task-definition.json  
.github/workflow/aws.yml

## Elasticsearch
実験的にElasticsearchのdocker-compose.ymlも定義しています。  
FastAPIとの連携は未対応のため、別途対応予定です。

# インストール&使い方(Installations & How to use)

## Dockerコンテナ内で開発(推奨)
ポート重複でコンテナが起動できない場合は、docker-compose.ymlを修正してください。

### VSCODEに「Remote Containers」をインストール
拡張機能「Remote Containers」をインストール

### コンテナを起動
コマンドパレットを開き、「reopen container」と入力して実行

### コンテナ内のコンソールログ確認方法
リモートエクスプローラー -> CONTAINERS -> {{ コンテナ名 }} -> Show Container Logs　

## ローカルで開発
ローカルで開発する場合
### Poetryのインストール
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

### 依存パッケージのインストール
```
poetry install
```

### dockerコンテナのビルド & 起動
```
docker-compose up --build
```

## API管理画面(OpenAPI)表示
ローカル環境
```
http://localhost:8888/docs
```

Debugモード(F5押下)で起動した場合  
※Debugモードの場合は、ブレークポイントでローカル変数を確認できます。
```
http://localhost:8889/docs
```

## poeタブ入力補完設定(completion)
※dockerコンテ内で開発する場合は、Dockerfileに組み込まれているため実行不要です  
bashを使用している場合は、以下のコマンドを実行する。  
これにより、タスクランナー実行時にタブで入力補完が可能になります。

```bash
 poe _bash_completion >> ~/.bashrc
```

次回bash起動時に有効化されるが、即時有効化するためには以下を実行します。
```
. ~/.bashrc
```

# デプロイ
heroku-cliを使用したherokuへのデプロイ方法を紹介します。  
githubからの自動デプロイはheroku側のセキュリティ問題により停止されているので、手動でherokuにpushします。

## heroku-cliのインストール
以下を参考にインストール<br>
https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli

## appの作成
APPNAMEは任意の名称を指定（全ユーザーでユニークである必要があります）
```
heroku create APPNAME
```

## gitにherokuのリモートリポジトリをセット
```
heroku git:remote --app APPNAME
```

## push
```
git push heroku master
```

## heroku-cliにheroku-configをインストール
本リポジトリでは、.envファイル経由で設定を読み込んでいるため  
herokuでも.envファイルを有効にする必要があります。
```bash
heroku plugins:install heroku-config
```

## .envファイルをpush
```bash
heroku config:push
```

## heroku再起動
```bash
heroku restart
```

# ライセンス(License)
https://choosealicense.com/licenses/mit/