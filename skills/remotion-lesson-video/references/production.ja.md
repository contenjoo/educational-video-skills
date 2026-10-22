# プロジェクトの準備とレンダリング

[한국어](production.md) · [English](production.en.md) · 日本語

## 環境

ターミナル、Node.js、パッケージ管理ツール、動作するレンダリング用ブラウザーを確認する。OS・Nodeの対応状況は[公式ドキュメント](https://www.remotion.dev/docs/)で確認する。既存のロックファイルを維持し、`remotion` とすべての `@remotion/*` を互換性のある同じ版にそろえる。理由なくグローバルインストールや既存プロジェクトの更新を行わない。

新規作成には、現在の仕様で対応していれば `npx create-video@latest` など公式ジェネレーターを使う。書き込み可能な新規フォルダーを選び、既存ファイルと質問項目を確認し、授業に必要なものだけを選ぶ。実行環境のネットワーク・実行規則に従う。[公式Remotionスキル](https://www.remotion.dev/docs/ai/skills)は補助として使えるが必須ではない。

## 構成と時間

```text
lesson-project/
  src/               compositions, scenes, subtitles and zoom
  public/media/      actual footage, audio and licensed visuals
  content/           objectives, script, timeline and provenance
  output/            final MP4 and SRT
  qa/                hashes, technical checks and playback records
```

原本素材を保全する。各録画の画面、日付、言語、実操作、使用範囲を記録し、署名付きURLや認証情報をソースに保存しない。

場面ID、元映像の範囲、開始・終了フレーム、音声ファイル、発話・字幕の時間、拡大、練習用の間を記録する。時間の単位とfps、トリミング開始位置の違いを明示する。音声の重複や場面末尾での発話切れを避ける。

## 実行

プロジェクトのスクリプトを優先する。次の例のエントリーポイントと構成IDは実際の値に置き換える。

```bash
npx remotion studio src/index.ts
npx remotion render src/index.ts Lesson output/lesson.mp4
```

引数とメディア部品を[公式仕様](https://www.remotion.dev/docs/)と照合し、実素材の短い区間を先にレンダリングする。実録画がなければ操作を捏造しない。

ログに基づいて原因を調べる。CPU・メモリー不足なら同時実行数を減らす。キャッシュ権限の問題は書き込み可能なプロジェクト内キャッシュや対応する無効化設定を調べる。保護の解除や権限変更を既定の解決策にしない。パッケージ版、実行コマンド、入出力パスを記録し、別の利用者が素材と音声を差し替えて再現できるようにする。
