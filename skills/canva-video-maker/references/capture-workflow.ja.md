# 実行方法とlesson.json

[한국어](capture-workflow.md) · [English](capture-workflow.en.md) · 日本語

キャプチャ → 台本 → 音声 → Pillow → FFmpegの制作手順を使う。非公開のブランド、講座一覧、公開権限、固定音声の規則は含まない。

## 準備と実行

`SKILL_DIR` をインストールしたスキルの絶対パスに設定し、新しいプロジェクトフォルダーで実行する。Windows PowerShellではパス表記を環境に合わせる。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install "Pillow>=10,<13"
.venv/bin/python "$SKILL_DIR/scripts/preflight.py" --mode canva
.venv/bin/python "$SKILL_DIR/scripts/render_lesson.py" lesson.json --frames --output preview
.venv/bin/python "$SKILL_DIR/scripts/render_lesson.py" lesson.json --validate
.venv/bin/python "$SKILL_DIR/scripts/render_lesson.py" lesson.json --output output
```

FFmpeg/FFprobeはOSのパッケージ管理ツールで導入する。`font` は制作言語に対応した手持ちのフォントに設定する。フォントとPillowは同梱も自動取得もしない。Windowsの仮想環境Pythonは `.venv/Scripts/python.exe`。準備検査にもPillowを入れた同じPythonを使う。日本語は日本語グリフを含むフォントを選び、漢字・かな・句読点と改行をプレビューで確認する。

`--frames` は音声・確認承認なしでもプレビューを作れるが、最終動画は生成しない。`--validate` は画像、確認記録、SHA、音声の出所を検査する。出力先が既にあれば新しいパスを選ぶ。標準は1920×1080、30fps、H.264/AAC。長い場面は音声を速めず分割する。

## 入力

次は形式の例であり、実際の確認・生成の証拠ではない。すべての仮の値を実ファイルと記録に置き換える。パスはlesson.jsonからの相対パス。SHA-256は例えば `hashlib.sha256(Path(...).read_bytes()).hexdigest()` で計算する。

```json
{
  "schema_version": 1,
  "title": "テキストボックスを追加する",
  "font": "fonts/YourJapaneseFont.ttf",
  "scenes": [
    {
      "image": "images/01.png",
      "caption": "テキストボックスを追加します。",
      "narration": "テキストメニューを開き、テキストボックスを追加を選びます。",
      "audio": "audio/01.wav",
      "hold_seconds": 1.2,
      "capture": {
        "kind": "actual_screen_capture",
        "source": "Actual capture tool or source file and time range",
        "captured_at": "Actual capture timestamp"
      },
      "image_review": {
        "approved": false,
        "reviewed_by": "Actual reviewer",
        "reviewed_at": "Actual review timestamp",
        "sha256": "Reviewed image SHA-256"
      },
      "preview_review": {
        "approved": false,
        "reviewed_by": "Actual final-card reviewer",
        "reviewed_at": "Actual review timestamp",
        "sha256": "Exact reviewed PNG SHA-256 from preview.json"
      },
      "audio_provenance": {
        "provider": "Own recording or actual TTS provider",
        "generation_id": "Actual recording session or generation job ID",
        "sha256": "Actual audio SHA-256"
      },
      "crop": [
        0,
        0,
        1280,
        720
      ],
      "highlights": [
        [
          75,
          180,
          200,
          55
        ]
      ]
    }
  ]
}
```

`crop` と `highlights` は任意のx/y/width/heightピクセル矩形である。切り抜きは元画像の座標、強調は**切り抜いた画像**の座標を使う。範囲外は拒否される。縦横比を維持し、画像の下に短い説明を置き、発話全文をSRTと台本に書き出す。実対象を確認した場合だけ強調を追加する。

直接キャプチャには `actual_screen_capture`、実録画からのフレームには `actual_recording_frame` を使う。取得元の記録は申告であり、レンダラーによる遠隔認証ではない。

最終render.jsonの状態は `rendered_pending_playback_review`。未実施の全編聴取を承認済みにしない。標準の字幕時間は実音声内での推定であり、確認済みの時刻や強制アラインメントで改善する。

## v3のプレビュー確認と字幕

`--frames` は完成カードPNGとハッシュ入りpreview.jsonを作る。対象の意味と位置、言語、切れ、余白、個人情報を各カードで確認する。その後に各場面の `preview_review.approved`、実際の確認者・時刻・正確なPNG SHAを記録する。自動承認の指示ではない。`--validate` はカードをメモリー内に作り、確認の欠落・古い承認・無効な切り抜きや強調を拒否する。タイトル、説明、元画像、フォント、順序、強調を変えるとハッシュが変わり再確認が必要。v2から移行するときも新しい画像を見ずに承認をコピーしない。

レンダラーは短いSRT字幕とnarration.txtを出力し、承認済み発話の全文が保たれたか検査する。標準の時刻は実測した場面音声内での推定と明記する。実際に整列済みの時間があれば、各場面の任意の `subtitles` に例えば `[{"start": 0.0, "end": 1.4, "text": "テキストメニューを開きます。"}]` の形式で指定する。この短い例だけで台本全文を網羅するわけではない。実入力では字幕全文が承認済み表示台本を過不足なく含み、時間が正で増加し、重ならず発話の長さに収まる必要がある。整列時刻を捏造しない。`subtitle_max_chars` の標準は42、指定範囲は10〜120。言語・配置に合わせる。

最終レンダリングは共通メディア・字幕チェッカーを一度実行し、render.jsonに記録する。無音・空音声、単語欠落、ゼロ長・重複時刻、字幕の途中切れは不合格。読みやすさの警告は別途確認する。発話速度を変えたり途中に間を入れたりしない。残る手動確認と公開先確認は[制作時の確認事項](production-checks.ja.md)を参照する。
