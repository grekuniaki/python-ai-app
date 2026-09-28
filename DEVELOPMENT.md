# 開発ガイド

このドキュメントは、プロジェクトの開発者向けのセットアップと拡張方法を説明します。

## 🛠️ 開発環境のセットアップ

### 1. リポジトリをクローン（既にある場合はスキップ）

```bash
git clone <repository-url>
cd python-ai-app
```

### 2. 仮想環境を作成・有効化

```bash
# 仮想環境を作成
python -m venv venv

# Windows の場合
venv\Scripts\activate

# macOS/Linux の場合
source venv/bin/activate
```

### 3. 開発用依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 4. .env ファイルを設定

```bash
# .env.example をコピー
cp .env.example .env  # macOS/Linux
# または
copy .env.example .env  # Windows
```

`.env` ファイルを開いて、`GEMINI_API_KEY` を設定してください。

### 5. アプリを起動

```bash
streamlit run app.py
```

## 📝 新しい執筆ツールを追加する手順

### ステップ 1: ページファイルを作成

`pages/` ディレクトリに新しいファイルを作成します。ファイル名は以下の形式に従ってください：

```
pages/{number}_{emoji}_{title}.py
```

例: `pages/8_🎓_教育コンテンツ生成.py`

ページは自動的に番号の順序でサイドバーに表示されます。

### ステップ 2: ページの基本構造を実装

```python
import streamlit as st
from utils.gemini_client import generate_text, GeminiConfigError, GeminiAPIError

st.set_page_config(page_title="新機能のタイトル", page_icon="🎓")

st.title("🎓 新機能のタイトル")

# ユーザー入力を取得
input_text = st.text_area("入力内容:")
option = st.selectbox("オプション:", ["オプション1", "オプション2"])

# ボタンを押して生成
if st.button("生成する"):
    if not input_text.strip():
        st.warning("入力内容を入力してください")
    else:
        with st.spinner("生成中..."):
            try:
                # プロンプトを構築
                system_instruction = """
                あなたは教育コンテンツ作成者です。
                わかりやすく、興味深い内容を作成してください。
                """
                
                user_prompt = f"""
                テーマ: {input_text}
                オプション: {option}
                
                上記のテーマについての教育コンテンツを作成してください。
                """
                
                # API を呼び出し
                result = generate_text(
                    user_prompt=user_prompt,
                    system_instruction=system_instruction,
                    temperature=0.7
                )
                
                # セッション状態に保存（再実行時に結果を保持）
                st.session_state["new_feature_result"] = result
                
            except GeminiConfigError as e:
                st.error(f"設定エラー: {e}")
            except GeminiAPIError as e:
                st.error(f"Gemini APIエラー: {e}")
            except Exception as e:
                st.error(f"予期しないエラーが発生しました: {e}")

# 結果を表示
if "new_feature_result" in st.session_state:
    st.markdown("## 📋 生成された内容")
    st.markdown(st.session_state["new_feature_result"])
    
    # コピーボタン
    st.write("結果をコピーして他のアプリケーションで使用してください。")
```

### ステップ 3: ホームページ（app.py）を更新

新しい機能を `app.py` の機能リストに追加します。

```python
features = [
    ("📧", "メール返信文生成", "受信メールに対する返信文をAIが生成"),
    # ... 既存の機能 ...
    ("🎓", "教育コンテンツ生成", "テーマから教育コンテンツを生成"),  # <- 追加
]
```

### ステップ 4: README.md を更新

`README.md` の「機能一覧」セクションに新しい機能を追加してください。

## 🎨 プロンプト設計のベストプラクティス

### システム指示（System Instruction）の書き方

```python
system_instruction = """
あなたは{ロール}です。

制約事項:
- {制約1}
- {制約2}
- 出力は{形式}で行ってください

トーン: {トーン}
"""
```

### ユーザープロンプト（User Prompt）の書き方

```python
user_prompt = f"""
入力内容:
- テーマ/トピック: {theme}
- パラメータ: {parameter}

要件:
- {要件1}
- {要件2}

出力してください。
"""
```

### チェックリスト

- [ ] ユーザーに何を期待するかが明確か？
- [ ] 出力形式が明確に指示されているか？
- [ ] 不要な前置きがないか？（「Here is...」など）
- [ ] Markdown 形式の使用を指示しているか？（必要な場合）
- [ ] 温度（temperature）の値は適切か？
  - 0.3-0.5: 事実的・一貫性重視（翻訳、校正など）
  - 0.7: バランス型（デフォルト）
  - 0.9-1.0: 創造的・多様性重視（ブログ、SNS投稿など）

## 🧪 テスト

### 手動テスト

1. ページをローカルで起動
2. 複数の入力パターンをテスト
3. エラーハンドリングを確認
4. セッション状態の永続化を確認

### テストチェックリスト

- [ ] 空入力時のエラーハンドリング
- [ ] 最小限の入力での動作確認
- [ ] 最大限の入力での動作確認
- [ ] API エラー時の表示
- [ ] 設定エラー時の表示
- [ ] ブラウザの再読み込み後も結果が保持されるか

## 🔍 トラブルシューティング

### 変更が反映されない場合

Streamlit は `.env` の変更を反映させるのに完全な再起動が必要です。

```bash
# ターミナルで Ctrl+C を押す
# アプリを停止

# 再度起動
streamlit run app.py
```

### API が呼び出されない

1. `.env` ファイルが正しく設定されているか確認
2. Streamlit アプリをリスタートしたか確認
3. ブラウザのコンソール（F12）でエラーがないか確認

## 📚 コード規約

- 日本語でのコメントはコード内で説明が必要な部分のみ
- 関数名・変数名は英語で統一
- f-string を使用してプロンプトを構築
- session_state のキーは `{page_key}_result` 形式に統一

## 🚀 デプロイ

このアプリは個人用なため、セキュリティやスケーラビリティの考慮は不要です。
ローカル環境でのみ実行されることを想定しています。

---

質問や改善提案がある場合は、コードを確認して調整してください。
