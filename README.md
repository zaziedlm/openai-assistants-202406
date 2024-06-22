# プロジェクト名
Assistants API file-search 検証 

https://platform.openai.com/docs/assistants/tools/file-search
https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/file-search?tabs=python

## 概要

このプロジェクトは、OpenAI API , Azure OpenAI API を使用して、Assistants API file-search v2 での問い合わせを実行するものです。具体的には、ユーザーからの質問に対して、指定フォルダの下のPDFファイルを元に、回答を生成します。

## 機能

- ユーザーからの質問に対して、指定フィルダー下のファイルを使って回答する

## 確認している必要条件

- Python 3.11 以上
- OpenAI API アクセス情報
- Azure OpenAI API アクセス情報

## インストール方法

1. このリポジトリをクローンまたはダウンロードします。
2. 必要なライブラリをインストールします。

    ```bash
    pip install -r requirements.txt
    ```
or poetryを導入している場合

    ```bash
    poetry poetry install --no-root
    ```

## 使用方法

1. `.env-template` ファイルを元にして、`.env`ファイルを配置します。
2. 必要に応じて、OpenAI, Azure OpenAIのアクセス情報を設定します。
3. スクリプトを実行します。

    ```bash
    python assistants_openai.py
    ```

## 注意事項

2024/6/22現在、Azure OpenAI us-east1 での、Assistants API の実行はエラーとなっています。

## Notes

As of June 22, 2024, executing Assistants API on Azure OpenAI us-east1 results in an error.