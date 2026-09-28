# プロジェクト構成

```
python-ai-app/
│
├── app.py                           # ホームページ・メインエントリーポイント
│
├── pages/                           # Streamlit マルチページ（各ページが自動的にサイドバーに表示）
│   ├── 1_📧_メール返信文生成.py
│   ├── 2_📝_文章要約.py
│   ├── 3_✍️_ブログ記事執筆.py
│   ├── 4_📱_SNS投稿生成.py
│   ├── 5_🔄_トーン・スタイル変換.py
│   ├── 6_✅_文章校正.py
│   └── 7_🌐_翻訳.py
│
├── utils/                           # ユーティリティモジュール
│   ├── __init__.py
│   └── gemini_client.py             # Gemini API クライアント（共通）
│
├── .streamlit/                      # Streamlit 設定ディレクトリ
│   └── config.toml                  # テーマ・レイアウト設定
│
├── .env.example                     # 環境変数テンプレート（.env にコピーして使用）
├── .env                             # 環境変数（.gitignore に含まれるため git に上がらない）
├── .gitignore                       # Git 無視ファイル設定
│
├── requirements.txt                 # Python 依存パッケージ
│
├── CLAUDE.md                        # Claude Code（claude.ai/code）向けガイダンス
├── README.md                        # ユーザー向けセットアップガイド
├── DEVELOPMENT.md                   # 開発者向けセットアップ・拡張ガイド
├── PROJECT_STRUCTURE.md             # このファイル（プロジェクト構成説明）
├── CHANGELOG.md                     # 変更履歴
│
└── venv/                            # Python 仮想環境（.gitignore に含まれるため git に上がらない）
    ├── Scripts/                     # Windows 用実行ファイル
    ├── Lib/                         # Python パッケージ
    └── pyvenv.cfg                   # 仮想環境設定
```

## ファイル説明

### コアファイル

| ファイル | 説明 | 管理者 |
|---------|------|--------|
| `app.py` | Streamlit ホームページ。機能一覧の表示とナビゲーション | ユーザー |
| `pages/*.py` | 各執筆ツールを実装したページ。Streamlit がファイル名から自動生成 | ユーザー |
| `utils/gemini_client.py` | Gemini API のラッパー。すべてのページから使用 | 開発者 |

### 設定ファイル

| ファイル | 説明 | 編集 |
|---------|------|------|
| `.env` | API キー等の環境変数（リポジトリに上げない） | ユーザー |
| `.env.example` | `.env` のテンプレート（リポジトリに上げる） | 開発者 |
| `.streamlit/config.toml` | Streamlit のテーマ・UI設定 | 開発者 |
| `requirements.txt` | Python パッケージの依存関係 | 開発者 |

### ドキュメント

| ファイル | 対象者 | 内容 |
|---------|--------|------|
| `README.md` | ユーザー | セットアップ方法、使い方、トラブルシューティング |
| `DEVELOPMENT.md` | 開発者 | 開発環境セットアップ、新機能追加手順、プロンプト設計 |
| `CLAUDE.md` | Claude（AI） | Claude Code 用の指示とプロジェクト情報 |
| `PROJECT_STRUCTURE.md` | 開発者 | このファイル。プロジェクト全体の構成 |
| `CHANGELOG.md` | 開発者・ユーザー | 変更履歴とリリースノート |

## アーキテクチャの特徴

### 1. Streamlit マルチページ

- ファイル名から自動的にサイドバーナビゲーションが生成される
- ファイル名形式: `{number}_{emoji}_{title}.py`
- 順序は番号で自動決定

### 2. 共有 Gemini クライアント

- `utils/gemini_client.py` が単一の情報源（Single Source of Truth）
- すべてのページから同じインターフェースで API 呼び出し
- エラーハンドリングを一元化

### 3. セッション状態による結果永続化

```python
st.session_state["page_key_result"] = result
```

- 結果をセッション状態に保存
- ページ内のウィジェット操作による再実行時も結果が消えない
- ページ更新（F5）で消える（ブラウザセッション内のみ）

### 4. 日本語対応

- ページタイトル、メッセージ、エラー表示はすべて日本語
- プロンプトも日本語で構築

## データフロー

```
ユーザー入力
    ↓
ページファイル（pages/*.py）
    ├─ ユーザー入力をプロンプトに構築
    ├─ utils.gemini_client.generate_text() を呼び出し
    └─ セッション状態に結果を保存
    ↓
utils/gemini_client.py
    ├─ Gemini API キー取得
    ├─ Google Gemini API に送信
    └─ 応答を返す
    ↓
Google Gemini API
    ├─ プロンプト処理
    └─ 生成テキストを返す
    ↓
ページファイル
    └─ 結果を画面に表示
```

## 依存関係

### Python パッケージ

| パッケージ | 用途 |
|-----------|------|
| `streamlit` | Web UI フレームワーク |
| `google-genai` | Google Gemini API クライアント（新統一 SDK） |
| `python-dotenv` | `.env` ファイルの読み込み |

詳細は `requirements.txt` を参照。

## 拡張ポイント

### 新しい執筆ツールの追加

1. `pages/` に新しい `.py` ファイルを作成
2. `app.py` の機能一覧に追加
3. `README.md` に説明を追加
4. 詳細は `DEVELOPMENT.md` を参照

### Gemini クライアントの改善

- `utils/gemini_client.py` を編集
- キャッシング、リトライロジック、ロギングなど
- すべてのページに自動的に反映される

### UI/テーマの変更

- `.streamlit/config.toml` を編集
- すべてのページに一貫性を持って適用される

## 注意事項

- **API キーの管理**: `.env` は絶対にリポジトリに上げない。`.gitignore` に設定済み
- **セッション有効期限**: ブラウザリフレッシュで結果が消える（設計）
- **シングルユーザー**: 複数ユーザーでの同時使用は想定していない
- **ログ保存なし**: 生成結果はセッション内に留まり、サーバーに保存されない

---

詳細はそれぞれのドキュメントを参照：
- 使い方 → `README.md`
- 開発方法 → `DEVELOPMENT.md`
- Claude Code 用 → `CLAUDE.md`
