# CLAUDE.md

このファイルは、Claude Code（claude.ai/code）がこのリポジトリのコードを操作する際のガイダンスを提供します。

## プロジェクト概要

Google Gemini APIを利用したAI搭載執筆補助のための個人用Streamlitアプリケーション。7つの独立した執筆ツール（メール返信文生成、テキスト要約、ブログ執筆、SNS投稿生成、トーン変換、校正、翻訳）が個別のStreamlitページとして実装されており、データベース、認証、ログインは不要です。

## 開発コマンド

### 環境セットアップ
```bash
# 仮想環境を作成
python -m venv venv

# アクティベート（Windows）
.\venv\Scripts\Activate.ps1

# アクティベート（macOS/Linux）
source venv/bin/activate

# 依存関係をインストール
pip install -r requirements.txt
```

### アプリを実行
```bash
# 標準起動（ポート8501）
streamlit run app.py

# カスタムポート（例：8502）
streamlit run app.py --server.port 8502

# デバッグモード
streamlit run app.py --logger.level=debug

# 非対話型モード
$env:STREAMLIT_SERVER_HEADLESS = "true"
streamlit run app.py
```

### 設定
- **必須**: `.env` ファイルで `GEMINI_API_KEY` を設定（https://aistudio.google.com/apikey から取得）
- **任意**: `.env` で `GEMINI_MODEL` をオーバーライド（デフォルト: `gemini-2.5-flash`）
- **重要**: `.env` 変更後は Streamlit を完全に再起動（Ctrl+C → 再実行）してください。ブラウザリフレッシュでは不十分です

## アーキテクチャ

### Streamlit マルチページ構造
- **`app.py`** — ホーム/ランディングページ（機能一覧とリンク）
- **`pages/`** — 各ページが1つの執筆ツールを実装
  - ファイル命名: `{number}_{emoji}_{title}.py`（順序とサイドバーアイコンは自動決定）
  - サイドバーはマルチページディレクトリから自動生成、設定不要

### 共有 Gemini クライアント（`utils/gemini_client.py`）
すべての API インタラクションの単一の情報源:
- `generate_text(user_prompt, system_instruction=None, temperature=0.7)` — コア関数、文字列応答を返す
- `get_model_name()` — `GEMINI_MODEL` 環境変数から設定されたモデル名を返す
- 2つのカスタム例外:
  - `GeminiConfigError` — `GEMINI_API_KEY` が不足/無効な場合に発生（ユーザーフレンドリーなメッセージング用に個別に処理）
  - `GeminiAPIError` — API呼び出しが失敗した場合に発生（ネットワーク、クォータ、安全フィルタ、空の応答）
- `@st.cache_resource` でクライアントをキャッシュ（再実行とページ間で効率化）
- `load_dotenv()` はモジュールインポート時に呼ばれ、`.env` をプロセスごとに1回読む

### 共通 UI/エラーハンドリングパターン
7つのページすべてが同じ構造に従います:
```python
with st.spinner("生成中..."):
    try:
        result = generate_text(user_prompt=..., system_instruction=...)
        st.session_state["<page_key>_result"] = result
    except GeminiConfigError as e:
        st.error(f"設定エラー: {e}")
    except GeminiAPIError as e:
        st.error(f"Gemini APIエラー: {e}")
    except Exception as e:
        st.error(f"予期しないエラーが発生しました: {e}")

if "<page_key>_result" in st.session_state:
    # 結果を表示
```
- 結果は `st.session_state` に保存され、再実行時に永続化します（重要：これがないと、ウィジェット操作時に結果が消えます）
- 各ページで f-string プロンプトを独立構築。共有プロンプトテンプレートの抽象化はなし（ページ構造が異なるため、共通抽象化は過度なエンジニアリング）

### 特別な処理: SNS投稿ページ（`pages/4_📱_SNS投稿生成.py`）
応答解析を行う唯一のページ:
- モデルは固定の2セクション形式を出力するよう指示（投稿テキスト + `---HASHTAGS---` セパレータ + ハッシュタグ）
- Python側で応答を分割して投稿とハッシュタグを抽出
- 文字数を計算で算出（LLMの数え方を信用しない）して X/Twitter の280文字制限をチェック
- プラットフォーム固有のガイダンスはページファイルのローカル辞書に保存（共有なし、機能固有）

### セッション状態の使用
- 各ページは `st.session_state` に `<page_key>_result` を保持して、再実行時に生成された出力を保存
- トーン変換ページはトーンごとに結果の辞書を保存（キーはトーン名）
- 現在のブラウザセッションを超えて永続化なし（個人ツールとしての設計上の選択）

## 新しい執筆ツールの追加方法

1. **ファイルを作成** — `pages/{number}_{emoji}_{title}.py`
2. **入力ウィジェット** — 必要に応じて `st.text_area`、`st.selectbox`、`st.radio`、`st.multiselect`、`st.slider`、`st.text_input`、`st.checkbox` を使用
3. **プロンプトを構築** — ページで f-string として `system_instruction` と `user_prompt` を構築
4. **API を呼び出し** — `utils.gemini_client` から `generate_text(user_prompt=..., system_instruction=..., temperature=...)` を使用
5. **結果を保存** — `st.session_state["{page_key}_result"]` に保存
6. **出力を表示** — 出力タイプに応じて `st.text_area`（コピー可能なプレーンテキスト）、`st.markdown`（フォーマット）、`st.tabs`（複数のバリアント）など を使用
7. **ホームページを更新** — `app.py` の機能リストとサイドバーナビゲーションにエントリを追加

## プロンプト設計ガイドライン

- **システム指示** — ロール、制約、出力形式を設定（例：「校正者です。タイプミスと文法を修正してください。セクションには ## 見出しを使用したマークダウンで出力」）
- **ユーザープロンプト — ラベル付きセクション付きの構造化入力を提供（例：`元の文章:\n{text}`、`希望するトーン: {tone}`）
- **明確さ** — モデルに*のみ*結果を出力するよう指示（「Here is your...」のような前置きなし）。コピー可能な出力の不要なプレフィックスを防止
- **構造** — 複数セクションの出力については、モデルに Markdown 見出しの使用を指示して、Python が解析不要に。`st.markdown` でそのまま表示
- **解析** — 下流ロジックに必要な場合以外は解析を避ける（例：SNS ページの280文字チェック）。過度な解析は出力を脆弱にする

## 環境変数

**.env ファイル（セットアップ後に必須）**
```
GEMINI_API_KEY=your_actual_key_here
GEMINI_MODEL=gemini-2.5-flash
```

- `GEMINI_API_KEY` — 必ず設定。未設定の場合はアプリが「設定エラー」を表示
- `GEMINI_MODEL` — 任意。省略時はデフォルト `gemini-2.5-flash`。`gemini-1.5-flash` は廃止済みで 404 になる
- 両方とも `utils/gemini_client.py` の `load_dotenv()` でプロセス開始時に1回読み込まれる

## キーファイル

- `utils/gemini_client.py` — すべての Gemini API 呼び出しがこのモジュール経由
- `app.py` — ホームページ、機能一覧、ナビゲーション
- `pages/1_📧_メール返信文生成.py` 〜 `pages/7_🌐_翻訳.py` — 執筆ツール
- `requirements.txt` — streamlit、google-genai、python-dotenv
- `.env.example` — テンプレート（リポジトリにコミット。ユーザーが `.env` にコピーしてキーを入力）
- `README.md` — ユーザー向けのセットアップと使用ガイド

## 今後の作業に向けたノート

- 自動テストなし。検証は README のトラブルシューティングセクションごとに手動
- データ永続化なし。結果は現在のブラウザセッションのみに存在
- 単一ユーザーの個人ツール。マルチユーザー、認証、データベースの考慮なし
- SDK の選択: `google-genai`（新しい統一 SDK）。レガシーな `google-generativeai`（メンテナンスモード）ではない
