import streamlit as st
from utils.gemini_client import generate_text, GeminiConfigError, GeminiAPIError

st.set_page_config(page_title="SNS投稿生成", page_icon="📱")
st.title("📱 SNS投稿生成")

PLATFORM_GUIDES = {
    "X (Twitter)": "X (旧Twitter) 向け。280文字以内を厳守し、簡潔でインパクトのある文章にする。",
    "Instagram": "Instagram向け。ビジュアルを想起させる説明的な文章、読みやすい改行を使う。",
    "LinkedIn": "LinkedIn向け。プロフェッショナルなトーンで、ビジネス上の学びや価値を伝える。",
}

content = st.text_area("投稿したい内容・メッセージ", height=150, key="content")
platform = st.selectbox(
    "プラットフォーム",
    list(PLATFORM_GUIDES.keys()),
    key="platform",
)
tone = st.selectbox(
    "トーン",
    ["カジュアル", "フォーマル", "ユーモラス", "感動的"],
    key="tone",
)
include_hashtags = st.checkbox("ハッシュタグ候補を含める", value=True, key="hashtags")

if st.button("生成する", type="primary", key="generate_button"):
    if not content.strip():
        st.warning("投稿したい内容を入力してください。")
    else:
        with st.spinner("生成中..."):
            try:
                platform_guide = PLATFORM_GUIDES[platform]

                if include_hashtags:
                    instruction_end = """必ず次の形式で出力してください:
投稿文をそのまま出力
---HASHTAGS---
#タグ1 #タグ2 #タグ3..."""
                else:
                    instruction_end = "投稿文のみを出力し、説明や前置きは付けないでください。"

                system_instruction = f"""あなたは SNS コンテンツの専門家です。
{platform_guide}
トーンは「{tone}」で統一してください。
{instruction_end}"""

                user_prompt = f"""投稿内容: {content}"""

                result = generate_text(
                    user_prompt=user_prompt,
                    system_instruction=system_instruction,
                )

                if include_hashtags and "---HASHTAGS---" in result:
                    post_text, _, hashtags = result.partition("---HASHTAGS---")
                    st.session_state["post_text"] = post_text.strip()
                    st.session_state["hashtags"] = hashtags.strip()
                else:
                    st.session_state["post_text"] = result.strip()
                    st.session_state["hashtags"] = ""

            except GeminiConfigError as e:
                st.error(f"設定エラー: {e}")
            except GeminiAPIError as e:
                st.error(f"Gemini APIエラー: {e}")
            except Exception as e:
                st.error(f"予期しないエラーが発生しました: {e}")

if "post_text" in st.session_state:
    st.markdown("### 生成された投稿文")
    st.text_area(
        "投稿文",
        value=st.session_state["post_text"],
        height=150,
        disabled=True,
    )

    char_count = len(st.session_state["post_text"])
    st.metric("文字数", char_count)

    if platform == "X (Twitter)":
        if char_count > 280:
            st.warning(f"⚠️ 280文字を超えています（{char_count}文字）")
        else:
            st.success(f"✅ 280文字以内です")

    if st.session_state.get("hashtags"):
        st.markdown("### ハッシュタグ候補")
        st.write(st.session_state["hashtags"])
