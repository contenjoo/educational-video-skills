# 教育動画制作スキル

**[한국어](README.md) · [English](README.en.md) · [日本語](README.ja.md)**

ClaudeとCodexで、実際の画面・台本・音声から教育動画を作る二つのスキルです。韓国語・英語・日本語の指示と参考文書を同梱しています。

| スキル | 用途 | 成果物 |
| --- | --- | --- |
| [Remotion教育動画](skills/remotion-lesson-video/SKILL.ja.md) | 実操作の録画編集、拡大・動き、複数授業・多言語制作 | MP4・SRT・台本・編集ソース・確認記録 |
| [キャプチャ教育動画](skills/canva-video-maker/SKILL.ja.md) | 実際の画面キャプチャ、強調表示、場面別音声による説明 | MP4・SRT・台本・入力素材・レンダリング記録 |

MITライセンスで使用・修正・再配布できます。個人アカウント、APIキー、専用音声、既存の講座原本は含みません。

## 言語の使い方

一つのZIPに韓国語・英語・日本語の指示がすべて入っています。言語ごとにインストールし直す必要はありません。指定した言語を優先し、指定がなければ依頼文の言語で案内します。案内の言語と動画・音声・字幕の言語は別々に指定できます。

例：「日本語で手順を説明し、韓国語の音声と字幕付き動画を作ってください。」

動画の対象言語に対応したフォントと音声を用意してください。文字化け・改行・読み方は実際の出力で確認します。スキルの導入だけで、ツール、アカウント権限、有料音声が利用可能になるわけではありません。

## 必要な環境

- 共通：実際の画面素材、本人の録音または利用可能なTTS、必要なファイル・ターミナル・ブラウザーツール。
- Remotion：Node.js・npm、動作するレンダリング用ブラウザー、FFmpeg/FFprobe。
- キャプチャ：Python 3.9以上、Pillow、FFmpeg/FFprobe、対象言語対応フォント。

サービス、素材、フォント、音声の利用条件と費用は各提供元で確認してください。ターミナルが使えないアプリでは台本・場面表の準備などに範囲が限られ、レンダリング完了とは扱いません。

## Claude Code・Codexへのインストール

Python 3.9以上とGitを使います。既存の同名スキルは標準では上書きしません。

```bash
git clone https://github.com/contenjoo/educational-video-skills.git
cd educational-video-skills
python3 scripts/install.py --target both --dry-run
python3 scripts/install.py --target both
```

一方だけに入れる場合は `--target claude` または `--target codex`。Windowsで `python3` がなければ `python` を使います。

| 対象 | 個人用 | プロジェクト用 |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |

プロジェクトだけに入れる場合は実際の絶対パスを指定します。

```bash
python3 scripts/install.py --target both --scope project --project /path/to/your-project
```

更新時は既存スキルを各製品の `skill-backups/` に保全します。バックアップは自動削除しません。

```bash
git pull --ff-only
python3 scripts/install.py --target both --update
```

インストール後、新しい会話で認識を確認してください。別の検索先に同じスキルがある場合は重複を確認します。

## Claudeウェブ・デスクトップへのインストール

[最新リリース](https://github.com/contenjoo/educational-video-skills/releases/latest)または[Contenjoo](https://contenjoo.com/)から個別スキルZIPを入手し、スキル管理画面でそれぞれアップロード・有効化してください。リポジトリー全体のZIPは使いません。各ZIPにはスキル名の最上位フォルダー、その中の `SKILL.md`、韓国語・英語・日本語の指示、参考文書、実行スクリプトが含まれます。実際に制作できる範囲はアプリ・組織・利用可能なツールによって変わります。

## 準備検査

Remotion：

```bash
python3 skills/remotion-lesson-video/scripts/preflight.py --mode remotion --network
```

キャプチャ：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install "Pillow>=10,<13"
.venv/bin/python skills/canva-video-maker/scripts/preflight.py --mode canva
```

Windowsの仮想環境Pythonは `.venv/Scripts/python.exe`。`--tts` はmacOSの韓国語システム音声を検査するときだけ追加します。準備検査の成功はログイン・制作・再生成功とは別です。

## 依頼例

Codex：

```text
$canva-video-maker
提供した実際の画面キャプチャから、テキストボックスの追加方法を説明する動画を作ってください。
日本語の音声・字幕と、クリック対象を示す番号のない四角を入れてください。
```

```text
$remotion-lesson-video
提供した実際の操作録画を編集して、初心者向けの教育動画を作ってください。
日本語の音声・字幕と練習時間を入れてください。
```

Claude Codeでは `/canva-video-maker` または `/remotion-lesson-video` を使います。ウェブ・デスクトップではスキルを有効化して目的を伝えます。既存のコマンド名とフォルダー名は互換性のため維持します。

## 検査と制作上の注意

実録画と静止画を区別します。特定の音声サービスは強制しません。画面確認後に台本を確定し、同梱レンダラーを再利用します。自動検査、実際の再生、人による全編聴取を区別し、アップロード・公開・既存講座の差し替えは依頼範囲で行います。

v3の制作時の確認事項、プレビューSHAと字幕全文の検査、v3.0.1の録画停止診断・無音動画検査を維持しています。v3.1では三言語の案内と同梱ファイルを追加しました。今回の言語対応確認は、全環境での日本語音声生成や母語話者による全編聴取を保証するものではありません。過去の実制作と補助作業の範囲は[検証記録（英語）](VALIDATION.en.md)を参照してください。

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

構造、相対リンク、公開内容、インストールの保全、入力保護を検査して `dist/` に二つのZIPを作ります。これらはログイン、TTS、撮影、レンダリング、再生の成功を保証しません。

問題は[Issues](https://github.com/contenjoo/educational-video-skills/issues)へ報告してください。パスワード、APIキー、児童生徒の個人情報を含めないでください。

[MIT](LICENSE)はこのリポジトリーのスキル・文書・ツールに適用されます。外部サービス、録画、フォント、画像、音声には各権利者の条件が適用されます。
