import streamlit as st
from utils.gemini_client import generate_text, GeminiConfigError, GeminiAPIError

st.set_page_config(page_title="文章校正", page_icon="✅")
st.title("✅ 文章校正")

text_to_proofread = st.text_area("校正したい文章", height=250, key="text_input")
include_readability = st.checkbox(
    "読みやすさに関するフィードバックも表示する",
    value=True,
    key="readability",
)

if st.button("生成する", type="primary", key="generate_button"):
    if not text_to_proofread.strip():
        st.warning("校正したい文章を入力してください。")
    else:
        with st.spinner("校正中..."):
            try:
                if include_readability:
                    instruction_end = (
                        "必ず以下のMarkdown構成で出力してください:\n"
                        "## 修正後の文章\n\n"
                        "## 修正箇所の説明\n\n"
                        "## 読みやすさに関するフィードバック"
                    )
                else:
                    instruction_end = (
                        "必ず以下のMarkdown構成で出力してください:\n"
                        "## 修正後の文章\n\n"
                        "## 修正箇所の説明"
                    )

                system_instruction = (
                    "あなたは日本語の文章校正の専門家です。"
                    "誤字脱字、文法エラー、不自然な言い回しを修正してください。"
                    f"{instruction_end}"
                )
                user_prompt = f"""校正対象の文章:
{text_to_proofread}

上記の文章を校正してください。"""

                result = generate_text(
                    user_prompt=user_prompt,
                    system_instruction=system_instruction,
                )
                st.session_state["proofread_result"] = result

            except GeminiConfigError as e:
                st.error(f"設定エラー: {e}")
            except GeminiAPIError as e:
                st.error(f"Gemini APIエラー: {e}")
            except Exception as e:
                st.error(f"予期しないエラーが発生しました: {e}")

if "proofread_result" in st.session_state:
    st.markdown("### 校正結果")
    st.markdown(st.session_state["proofread_result"])
