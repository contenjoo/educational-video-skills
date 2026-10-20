# 교육영상 만들기 스킬

**[한국어](README.md) · [English](README.en.md)**

Claude와 Codex에서 실제 화면·대본·음성을 교육영상으로 만드는 두 가지 스킬입니다.

| 방식 | 적합한 작업 | 결과물 |
| --- | --- | --- |
| [리모션 교육영상](skills/remotion-lesson-video/SKILL.md) | 실제 조작 녹화 편집, 확대·움직임, 여러 차시·다국어 영상 | MP4·SRT·대본·편집 소스·검수 기록 |
| [캡처 교육영상](skills/canva-video-maker/SKILL.md) | 실제 화면 캡처·강조·장면별 음성을 활용한 설명 | MP4·SRT·대본·입력 자료·렌더 기록 |

누구나 사용·수정·재배포할 수 있습니다(MIT). 개인 계정·API 키·특정 목소리·기존 강의 원본은 포함하지 않습니다. 독립적인 제작 워크플로입니다.

## v3: 제작 시행착오 반영

두 스킬의 한국어·영어 지침에 실제 제작에서 겪은 방식 오해, 빈 번호 자리, 잘못된 마킹, 음성·자막 누락, 낙관적 일정, 번역·폴더 누락과 공개본 교체 문제를 반영했습니다. 원본 프로젝트 확인, 짧은 완성본과 복잡한 대표 장면 검수, 일괄 제작, 목적지별 반영 확인을 구분합니다.

두 ZIP 모두 `scripts/check_media.py`를 포함합니다. 최종 미디어 디코드·음성·SRT 시간·전체 대본 보존을 검사하고 직접 청취·의미 대조·게시본 검증은 미확인으로 남깁니다. 자동 검사로 모든 실패를 막거나 100% 완성을 보장하지는 않습니다.

**v2에서 업데이트:** 캡처 렌더러에는 장면별 `preview_review`가 새로 필요합니다. `--frames`의 PNG를 실제로 확인한 뒤 preview.json의 SHA를 기록하세요. 문구·마킹·레이아웃 변경 후 예전 승인을 재사용할 수 없습니다. 긴 대본은 짧은 SRT 구절로 나누고, 기본 시각이 추정치임을 표시합니다. [입력과 마이그레이션](skills/canva-video-maker/references/capture-workflow.md), [공통 재발 방지 기준](skills/remotion-lesson-video/references/production-checks.md)을 확인하세요. 기존 식별자와 Claude·Codex 설치 경로는 유지합니다.

## 준비

- 공통: 실제 화면 자료, 본인 녹음 또는 이용 가능한 TTS, 필요한 파일·터미널·브라우저 도구.
- 리모션: Node.js·npm, 실행 가능한 렌더 브라우저, FFmpeg/FFprobe.
- 캡처: Python 3.9+, Pillow, FFmpeg/FFprobe, 제작 언어를 지원하는 폰트.

스킬 설치로 도구나 계정 권한이 생기지는 않습니다. 도구가 없는 환경에서는 대본·장면표 등 가능한 준비까지 진행하고 미완료 항목을 알립니다. 각 서비스와 미디어·폰트의 사용 조건 및 비용은 사용자가 확인합니다.

## Claude Code·Codex 설치

Python 3.9 이상과 Git으로 설치합니다. 기본 설치는 기존 같은 이름의 스킬을 덮어쓰지 않습니다.

```bash
git clone https://github.com/contenjoo/educational-video-skills.git
cd educational-video-skills
python3 scripts/install.py --target both --dry-run
python3 scripts/install.py --target both
```

한 제품만 설치하려면 `--target claude` 또는 `--target codex`를 사용합니다. Windows에서 `python3`가 없으면 `python`을 사용합니다.

| 대상 | 개인 설치 | 프로젝트 설치 |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |

프로젝트에만 설치할 때는 프로젝트의 절대 경로를 지정합니다.

```bash
python3 scripts/install.py --target both --scope project --project /path/to/your-project
```

업데이트는 기존 스킬을 해당 제품의 `skill-backups/`에 보존한 뒤 설치합니다. 백업은 자동 삭제하지 않습니다.

```bash
git pull --ff-only
python3 scripts/install.py --target both --update
```

설치 후 새 대화에서 확인합니다. 다른 검색 경로에 같은 식별자의 스킬이 있다면 중복 설치를 확인하세요. 공식 안내: [Codex](https://developers.openai.com/codex/skills/), [Claude Code](https://code.claude.com/docs/en/skills).

## Claude 웹·데스크톱 설치

1. [최신 릴리스](https://github.com/contenjoo/educational-video-skills/releases/latest)에서 두 개별 스킬 ZIP을 받습니다.
2. 사용자 스킬 관리 화면에서 ZIP을 각각 업로드·활성화합니다. [공식 안내](https://support.claude.com/en/articles/12512180-use-skills-in-claude)를 확인하세요.
3. 터미널·파일·브라우저 도구의 지원 범위를 확인하고 제작을 요청합니다.

저장소 전체 ZIP 대신 개별 스킬 ZIP을 사용합니다. 각 ZIP에는 최상위 스킬 폴더와 `SKILL.md`, 한국어·영어 안내가 들어 있습니다. 조직·앱별 기능 제한에 따라 실제 렌더 가능 범위가 달라집니다.

## 준비 검사

리모션은 다음 명령으로 검사합니다.

```bash
python3 skills/remotion-lesson-video/scripts/preflight.py --mode remotion --network
```

캡처 방식은 가상환경에 Pillow를 설치한 뒤 같은 Python으로 검사합니다.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install "Pillow>=10,<13"
.venv/bin/python skills/canva-video-maker/scripts/preflight.py --mode canva
```

Windows의 가상환경 Python은 `.venv/Scripts/python.exe`입니다. macOS 시스템 한국어 음성을 선택했을 때만 검사 명령에 `--tts`를 추가합니다. 준비 검사 통과와 로그인·실제 제작·재생 성공은 별도입니다.

## 사용

Codex에서 호출합니다.

```text
$remotion-lesson-video
제공한 실제 조작 녹화로 초보자용 교육영상을 만들어줘.
한국어 음성·자막과 따라 할 시간을 넣어줘.
```

```text
$canva-video-maker
제공한 실제 화면 캡처로 텍스트 상자 추가 방법을 설명해줘.
Python/Pillow·FFmpeg로 음성·자막과 클릭 위치 네모를 넣어줘.
```

Claude Code에서는 `/remotion-lesson-video` 또는 `/canva-video-maker`로 호출합니다. 웹·데스크톱에서는 스킬을 활성화하고 제작 목적을 설명합니다. 기존 설치 호환성을 위해 명령·폴더 식별자는 유지합니다.

## 검증·제작 원칙

실제 녹화와 정지 캡처를 구분하고, 특정 음성 서비스를 강제하지 않습니다. 캡처 방식은 화면 확인 후 대본을 확정하고 동봉 렌더러를 재사용합니다. 자동 검사·실제 재생·사람의 전편 청취를 구분합니다. 외부 게시·공유·기존 강의 교체는 요청 범위에서만 수행합니다.

Claude Code와 Codex 데스크톱에서 두 방식의 실제 MP4를 제작했습니다. 보조 작업과 검수 한계는 [실사용 검증 기록](VALIDATION.md)을 확인하세요. 모든 운영체제·계정·앱 조합이나 사람의 전편 청취를 검증한 것은 아닙니다. v1에서 잘못 안내한 두 번째 방식은 v2에서 캡처 기반 제작으로 수정했습니다.

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

위 명령은 구조·상대 참조·공개 내용·설치 백업·입력 보호를 검사하고 `dist/`에 두 ZIP을 만듭니다. 실제 로그인·음성 생성·녹화·렌더·재생을 보증하지는 않습니다.

문의·오류 제보는 [Issues](https://github.com/contenjoo/educational-video-skills/issues)를 이용하세요. 비밀번호·API 키·학생 개인정보를 포함하지 마세요.

## 라이선스

[MIT](LICENSE)는 이 저장소의 스킬·문서·도구에 적용됩니다. 외부 서비스·녹화·폰트·시각 자료·음성의 권리는 각 권리자와 사용 조건을 따릅니다.
