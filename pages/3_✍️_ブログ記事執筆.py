import streamlit as st
from utils.gemini_client import generate_text, GeminiConfigError, GeminiAPIError

st.set_page_config(page_title="ブログ記事執筆", page_icon="✍️")
st.title("✍️ ブログ記事執筆")

topic = st.text_input("トピック・キーワード", key="topic")
target_audience = st.text_input("ターゲット読者", key="audience")
tone = st.selectbox(
    "トーン",
    ["専門的", "親しみやすい", "カジュアル", "情熱的"],
    key="tone",
)
word_count = st.slider("おおよその文字数", 300, 3000, 800, step=100, key="word_count")
outline = st.text_area("含めたい要点・アウトライン（任意）", height=100, key="outline")

if st.button("生成する", type="primary", key="generate_button"):
    if not topic.strip():
        st.warning("トピック・キーワードを入力してください。")
    else:
        with st.spinner("生成中..."):
            try:
                system_instruction = (
                    "あなたはプロのブログライターです。"
                    "MarkdownフォーマットでHTMLの ## 見出しを使用した"
                    "ブログ記事を執筆してください。"
                    "指定された文字数に近い記事を作成し、"
                    "ターゲット読者と希望するトーンに合わせてください。"
                )
                outline_section = f"\n含めたい要点:\n{outline}" if outline.strip() else ""
                user_prompt = f"""トピック: {topic}
ターゲット読者: {target_audience}
トーン: {tone}
目安文字数: {word_count}文字{outline_section}

上記の条件でブログ記事を執筆してください。"""

                result = generate_text(
                    user_prompt=user_prompt,
                    system_instruction=system_instruction,
                )
                st.session_state["blog_result"] = result

            except GeminiConfigError as e:
                st.error(f"設定エラー: {e}")
            except GeminiAPIError as e:
                st.error(f"Gemini APIエラー: {e}")
            except Exception as e:
                st.error(f"予期しないエラーが発生しました: {e}")

if "blog_result" in st.session_state:
    st.markdown("### 生成されたブログ記事")
    st.markdown(st.session_state["blog_result"])

    with st.expander("Markdownソースを表示（コピー用）"):
        st.text_area(
            "",
            value=st.session_state["blog_result"],
            height=300,
            disabled=True,
        )
