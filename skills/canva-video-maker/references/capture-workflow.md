# 실행과 lesson.json

[English](capture-workflow.en.md) · 한국어

이 스킬은 기존 교육영상 프로젝트의 캡처·대본·음성·Pillow·FFmpeg 절차를 이식한 경량 실행 도구다. 개인 프로젝트의 브랜드 자산·강의 목록·공개 권한·고정 화자 규칙을 포함하지 않는다.

## 준비와 실행

스킬 폴더의 실제 절대 경로를 `SKILL_DIR`로 설정하고 새 작업 폴더에서 실행한다. Windows PowerShell에서는 환경에 맞게 경로 인자를 직접 넣는다.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install "Pillow>=10,<13"
python3 "$SKILL_DIR/scripts/preflight.py" --mode canva
.venv/bin/python "$SKILL_DIR/scripts/render_lesson.py" lesson.json --frames --output preview
.venv/bin/python "$SKILL_DIR/scripts/render_lesson.py" lesson.json --validate
.venv/bin/python "$SKILL_DIR/scripts/render_lesson.py" lesson.json --output output
```

FFmpeg/FFprobe는 시스템 패키지 관리자로 설치한다. 폰트는 사용자가 가진 한국어 폰트를 `font`에 지정한다. 폰트·Pillow를 배포 파일에 넣거나 자동 다운로드하지 않는다. Windows venv Python은 `.venv/Scripts/python.exe`다. 검사는 반드시 Pillow를 설치한 같은 Python으로 실행한다. 예시의 `python3`도 필요하면 해당 venv Python으로 바꾼다.

`--frames`는 음성·승인 없이도 화면을 만들지만 최종 결과가 아니다. `--validate`는 출력 없이 실제 이미지·승인·SHA·음성 출처를 검사한다. `output`이나 `preview`가 이미 있으면 다른 출력 경로를 지정한다. 기본 결과는 1920×1080, 30fps, H.264/AAC다. 장면이 너무 길면 나누고 음성 속도를 높이지 않는다.

## 입력

아래는 형식 예시이며 검수·생성 증거가 아니다. 실제 자료와 기록으로 채운다. 경로는 lesson.json이 있는 폴더 기준이다. SHA-256는 `hashlib.sha256(Path(...).read_bytes()).hexdigest()` 등으로 계산한다.

```json
{
  "schema_version": 1,
  "title": "텍스트 상자 추가하기",
  "font": "fonts/KoreanFont.ttf",
  "scenes": [{
    "image": "images/01.png",
    "caption": "텍스트 상자를 추가해 주세요.",
    "narration": "왼쪽 텍스트 메뉴에서 텍스트 상자 추가를 눌러 주세요.",
    "audio": "audio/01.wav",
    "hold_seconds": 1.2,
    "capture": {
      "kind": "actual_screen_capture",
      "source": "실제 캡처 도구 또는 원본 파일과 구간",
      "captured_at": "실제 촬영 시각"
    },
    "image_review": {
      "approved": false,
      "reviewed_by": "실제로 확인한 담당자",
      "reviewed_at": "실제 검수 시각",
      "sha256": "검수한 이미지 SHA-256"
    },
    "preview_review": {
      "approved": false,
      "reviewed_by": "Actual final-card reviewer",
      "reviewed_at": "Actual review timestamp",
      "sha256": "Exact reviewed PNG SHA-256 from preview.json"
    },
    "audio_provenance": {
      "provider": "본인 녹음 또는 실제 TTS 제공자",
      "generation_id": "실제 녹음 세션이나 생성 작업 식별자",
      "sha256": "실제 음성 파일 SHA-256"
    },
    "crop": [0, 0, 1280, 720],
    "highlights": [[75, 180, 200, 55]]
  }]
}
```

`crop`, `highlights`는 선택이다. crop은 원본 픽셀 x/y/폭/높이, highlights는 **크롭 후 이미지**의 픽셀 좌표다. 화면 밖 좌표는 거부한다. 원본 비율을 유지하며 맞추고 짧은 캡션을 화면 하단에 표시한다. narration 전체는 SRT·대본으로 출력한다. highlight는 실제 조작 대상을 확인한 뒤에만 넣는다. `capture.kind`는 실제 화면 직접 캡처 `actual_screen_capture` 또는 실제 녹화 프레임 `actual_recording_frame`을 사용한다. 이 기록은 사용자가 제공한 출처 진술이며 도구가 원격 원본을 인증하는 기능은 아니다.

완성본의 `render.json`은 `rendered_pending_playback_review`다. 전체 청취를 하지 않았는데 승인 상태로 바꾸지 않는다. 자막 시각은 장면 음성 안의 추정치이므로 실제 확인한 시각이나 강제 정렬 도구로 보정한다.


## v3 미리보기 검수와 자막

`--frames`는 최종 화면 PNG와 해시가 담긴 preview.json을 만든다. 모든 화면의 실제 대상·표시 위치·언어·잘림·빈칸·개인정보를 확인한 뒤에만 장면의 `preview_review.approved`, 실제 검수자·시각·정확한 PNG SHA를 기록한다. 자동 승인 명령이 아니다. `--validate`는 화면을 메모리에서 생성해 누락/오래된 미리보기 검수와 잘못된 크롭·좌표를 거부한다. 제목·문구·원본·폰트·순서·마킹이 바뀌면 화면 해시도 바뀌므로 다시 확인한다. v2에서 업데이트할 때 새로 필요한 필드이며 이전 승인을 보지 않은 화면에 옮겨 적지 않는다.

짧은 SRT 구절과 narration.txt를 만들고 승인된 발화 문구가 모두 보존됐는지 검사한다. 기본 구절 시각은 측정한 장면 음성 안의 추정치다. 실제로 정렬한 시각이 있다면 장면의 선택 필드 `subtitles`에 `[{"start": 0.0, "end": 1.4, "text": "텍스트 메뉴를 열어 주세요."}, {"start": 1.4, "end": 3.2, "text": "텍스트 상자 추가를 눌러 주세요."}]`처럼 넣는다. 문구는 해당 장면의 전체 표시용 발화와 일치해야 하고, 양수 길이·증가·겹침 없음·음성 범위 안을 지킨다. 확인하지 않은 정렬 시각을 꾸미지 않는다. `subtitle_max_chars` 기본 42, 허용 10~120으로 자동 구절 길이를 조정한다.

최종 렌더는 동봉 미디어/자막 검사를 1회 실행해 render.json에 넣는다. 무음·빈 음성, 단어 누락, 0초/겹친 자막, 영상 범위를 넘는 자막은 실패한다. 가독성 경고는 직접 확인해야 한다. 내레이션 재생 속도를 바꾸거나 발화 중간에 쉼을 넣지 않는다. 남은 직접 검수와 목적지 확인은 [재발 방지 기준](production-checks.md)을 따른다.
