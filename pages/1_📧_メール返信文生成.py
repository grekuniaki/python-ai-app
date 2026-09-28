import streamlit as st
from utils.gemini_client import generate_text, GeminiConfigError, GeminiAPIError

st.set_page_config(page_title="メール返信文生成", page_icon="📧")
st.title("📧 メール返信文生成")

received_email = st.text_area("受信したメール本文", height=200, key="received_email")
key_points = st.text_area("盛り込みたいポイント（箇条書きでOK）", height=100, key="key_points")
tone = st.selectbox(
    "返信のトーン",
    ["丁寧・フォーマル", "丁寧・柔らかい", "カジュアル", "ビジネスライク"],
    key="tone",
)
signature = st.text_input("差出人名（署名, 任意）", key="signature")

if st.button("生成する", type="primary", key="generate_button"):
    if not received_email.strip() or not key_points.strip():
        st.warning("メール本文と盛り込みたいポイントを入力してください。")
    else:
        with st.spinner("生成中..."):
            try:
                system_instruction = (
                    "あなたはビジネスメール返信の専門家です。"
                    "受け取ったメールに対して、指定されたトーンで、"
                    "提示されたポイントを盛り込んだ返信文を生成してください。"
                    "返信本文のみを出力し、件名や『以下、返信文です』などの前置きは付けないでください。"
                )
                user_prompt = f"""受信したメール:
{received_email}

盛り込みたいポイント:
{key_points}

希望するトーン: {tone}

差出人名: {signature if signature else '（なし）'}

上記のメールに対する返信文を生成してください。"""

                result = generate_text(
                    user_prompt=user_prompt,
                    system_instruction=system_instruction,
                )
                st.session_state["reply_result"] = result

            except GeminiConfigError as e:
                st.error(f"設定エラー: {e}")
            except GeminiAPIError as e:
                st.error(f"Gemini APIエラー: {e}")
            except Exception as e:
                st.error(f"予期しないエラーが発生しました: {e}")

if "reply_result" in st.session_state:
    st.markdown("### 生成された返信文")
    st.text_area("", value=st.session_state["reply_result"], height=300, disabled=True)
