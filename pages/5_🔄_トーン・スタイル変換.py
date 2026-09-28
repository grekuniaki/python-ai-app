import streamlit as st
from utils.gemini_client import generate_text, GeminiConfigError, GeminiAPIError

st.set_page_config(page_title="トーン・スタイル変換", page_icon="🔄")
st.title("🔄 トーン・スタイル変換")

text_input = st.text_area("変換したい文章", height=200, key="text_input")
tones = st.multiselect(
    "変換先のトーン（複数選択可）",
    ["フォーマル", "カジュアル", "敬語（丁寧語）", "ビジネスメール調", "フレンドリー", "学術的"],
    key="tones",
)

if st.button("生成する", type="primary", key="generate_button"):
    if not text_input.strip():
        st.warning("変換したい文章を入力してください。")
    elif not tones:
        st.warning("少なくとも1つのトーンを選択してください。")
    else:
        with st.spinner("変換中..."):
            try:
                results = {}
                for tone in tones:
                    system_instruction = (
                        f"あなたは文章編集の専門家です。"
                        f"入力された文章の意味を変えずに、「{tone}」のトーンに書き換えてください。"
                        f"書き換えた文章のみを出力し、説明や前置きは付けないでください。"
                    )
                    user_prompt = f"""元の文章:
{text_input}

上記の文章を「{tone}」のトーンに変換してください。"""

                    result = generate_text(
                        user_prompt=user_prompt,
                        system_instruction=system_instruction,
                    )
                    results[tone] = result

                st.session_state["converted_results"] = results

            except GeminiConfigError as e:
                st.error(f"設定エラー: {e}")
            except GeminiAPIError as e:
                st.error(f"Gemini APIエラー: {e}")
            except Exception as e:
                st.error(f"予期しないエラーが発生しました: {e}")

if "converted_results" in st.session_state:
    st.markdown("### 変換結果")

    if len(st.session_state["converted_results"]) == 1:
        tone = list(st.session_state["converted_results"].keys())[0]
        st.markdown(f"**{tone}**")
        st.text_area(
            "",
            value=st.session_state["converted_results"][tone],
            height=200,
            disabled=True,
        )
    else:
        tab_list = list(st.session_state["converted_results"].keys())
        tabs = st.tabs(tab_list)
        for tab, tone in zip(tabs, tab_list):
            with tab:
                st.text_area(
                    "",
                    value=st.session_state["converted_results"][tone],
                    height=200,
                    disabled=True,
                )
