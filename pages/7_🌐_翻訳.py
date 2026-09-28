import streamlit as st
from utils.gemini_client import generate_text, GeminiConfigError, GeminiAPIError

st.set_page_config(page_title="翻訳", page_icon="🌐")
st.title("🌐 翻訳")

text_to_translate = st.text_area("翻訳したい文章", height=250, key="text_input")

predefined_languages = [
    "日本語",
    "英語",
    "中国語（簡体字）",
    "韓国語",
    "フランス語",
    "スペイン語",
    "ドイツ語",
    "その他（下に入力）",
]
language_choice = st.selectbox("翻訳先言語", predefined_languages, key="language_choice")

if language_choice == "その他（下に入力）":
    target_language = st.text_input("翻訳先言語を入力", key="custom_language")
else:
    target_language = language_choice

style = st.selectbox(
    "文体",
    ["自動判定に任せる", "フォーマル", "カジュアル"],
    key="style",
)

if st.button("生成する", type="primary", key="generate_button"):
    if not text_to_translate.strip():
        st.warning("翻訳したい文章を入力してください。")
    elif language_choice == "その他（下に入力）" and not target_language.strip():
        st.warning("翻訳先言語を入力してください。")
    else:
        with st.spinner("翻訳中..."):
            try:
                if style == "自動判定に任せる":
                    style_instruction = ""
                else:
                    style_instruction = f"翻訳の文体は「{style}」としてください。"

                system_instruction = (
                    "あなたは翻訳の専門家です。"
                    "入力文の言語を自動検出し、指定された言語に翻訳してください。"
                    f"{style_instruction}"
                    "翻訳文のみを出力し、説明や注釈、『以下が翻訳です』などの前置きは付けないでください。"
                )
                user_prompt = f"""翻訳対象の文章:
{text_to_translate}

翻訳先言語: {target_language}

上記の文章を翻訳してください。"""

                result = generate_text(
                    user_prompt=user_prompt,
                    system_instruction=system_instruction,
                )
                st.session_state["translation_result"] = result

            except GeminiConfigError as e:
                st.error(f"設定エラー: {e}")
            except GeminiAPIError as e:
                st.error(f"Gemini APIエラー: {e}")
            except Exception as e:
                st.error(f"予期しないエラーが発生しました: {e}")

if "translation_result" in st.session_state:
    st.markdown(f"### {target_language}への翻訳結果")
    st.text_area(
        "",
        value=st.session_state["translation_result"],
        height=250,
        disabled=True,
    )
