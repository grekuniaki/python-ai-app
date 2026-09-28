# 変更履歴

すべての重要な変更をこのファイルに記録します。

## [1.0.0] - 2026-09-27

### 追加
- 🎉 初版リリース
- 7つの執筆ツール機能を実装
  - 📧 メール返信文生成
  - 📝 文章要約
  - ✍️ ブログ記事執筆
  - 📱 SNS投稿生成（プラットフォーム最適化、ハッシュタグ抽出）
  - 🔄 トーン・スタイル変換
  - ✅ 文章校正
  - 🌐 翻訳
- Google Gemini API 統合
- Streamlit マルチページ構造
- 環境変数設定（`.env`）
- エラーハンドリング（GeminiConfigError、GeminiAPIError）
- セッション状態による結果永続化
- `.streamlit/config.toml` 設定ファイル
- 開発向けドキュメント（`DEVELOPMENT.md`、`PROJECT_STRUCTURE.md`）
- 日本語ドキュメント（`CLAUDE.md` を日本語化）

### 技術仕様
- Python 3.10+
- Streamlit（マルチページ）
- Google Gemini API（google-genai SDK）
- python-dotenv（環境変数管理）

---

## フォーマット説明

変更履歴は [Keep a Changelog](https://keepachangelog.com/ja/) の形式に従っています。

### セクション
- **Added**: 新機能
- **Changed**: 変更・改善
- **Deprecated**: 廃止予定
- **Removed**: 削除
- **Fixed**: バグ修正
- **Security**: セキュリティ修正

### バージョニング
[Semantic Versioning](https://semver.org/lang/ja/) に従っています：
- `MAJOR.MINOR.PATCH`
- MAJOR: 後方互換性を破る変更
- MINOR: 後方互換性を保つ新機能
- PATCH: バグ修正
