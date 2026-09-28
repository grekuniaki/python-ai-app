import streamlit as st

st.set_page_config(
    page_title="AI文章作成アシスタント",
    page_icon="✍️",
    layout="centered",
)

st.title("✍️ AI文章作成アシスタント")

st.markdown("""
Gemini API を搭載した個人用ライティングツール。
7つの便利なAI機能であなたの執筆をサポートします。
""")

st.markdown("## 📚 機能一覧")

features = [
    ("📧", "メール返信文生成", "受信メールに対する返信文をAIが生成"),
    ("📝", "文章要約", "長い文章を指定した長さで要約"),
    ("✍️", "ブログ記事執筆", "テーマからブログ記事を執筆"),
    ("📱", "SNS投稿生成", "プラットフォーム最適化で投稿を生成"),
    ("🔄", "トーン・スタイル変換", "同じ内容を異なる文体で書き換え"),
    ("✅", "文章校正", "誤字脱字・文法を修正・改善"),
    ("🌐", "翻訳", "複数言語への自動翻訳"),
]

cols = st.columns(2)
for idx, (icon, title, desc) in enumerate(features):
    with cols[idx % 2]:
        st.markdown(f"### {icon} {title}")
        st.markdown(f"{desc}")

st.markdown("---")
st.markdown("""
### 🚀 使い方
左側のサイドバーから使いたい機能を選び、入力内容を入力して「生成する」をクリック。
数秒でAIが処理を行い、結果が表示されます。

### ⚙️ セットアップ
このアプリを使用するには、`.env` ファイルに Gemini API キーを設定する必要があります。
詳細は README.md をご覧ください。
""")
