import streamlit as st
from utils.gemini_client import generate_text, GeminiConfigError, GeminiAPIError

st.set_page_config(page_title="文章要約", page_icon="📝")
st.title("📝 文章要約")

text_to_summarize = st.text_area("要約したい文章", height=250, key="text_input")
length = st.radio(
    "要約の長さ",
    ["短め（1〜2文）", "普通（3〜5文）", "詳しめ（箇条書き）"],
    key="length",
)
style = st.selectbox("出力スタイル", ["文章形式", "箇条書き"], key="style")

if st.button("生成する", type="primary", key="generate_button"):
    if not text_to_summarize.strip():
        st.warning("要約したい文章を入力してください。")
    else:
        with st.spinner("生成中..."):
            try:
                system_instruction = (
                    "あなたは要約の専門家です。"
                    "元の文章にない情報を追加せず、"
                    "指定された長さとスタイルを厳守して要約してください。"
                )
                user_prompt = f"""元の文章:
{text_to_summarize}

希望の長さ: {length}
希望のスタイル: {style}

上記の文章を要約してください。"""

                result = generate_text(
                    user_prompt=user_prompt,
                    system_instruction=system_instruction,
                )
                st.session_state["summary_result"] = result

            except GeminiConfigError as e:
                st.error(f"設定エラー: {e}")
            except GeminiAPIError as e:
                st.error(f"Gemini APIエラー: {e}")
            except Exception as e:
                st.error(f"予期しないエラーが発生しました: {e}")

if "summary_result" in st.session_state:
    st.markdown("### 要約結果")
    st.markdown(st.session_state["summary_result"])
