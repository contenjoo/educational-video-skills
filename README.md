# 교육영상 만들기 스킬 · Educational Video Skills

**Claude와 Codex에서 사용하는 두 가지 교육영상 제작 스킬입니다.** 실제 조작 녹화를 Remotion으로 편집하거나, 실제 Canva 캡처를 Python/Pillow·FFmpeg로 렌더합니다.

누구나 내려받아 사용·수정·재배포할 수 있습니다(MIT). 개인 계정, API 키, 특정 목소리, 기존 강의 원본은 포함하지 않습니다. Canva와 Remotion의 공식 배포물이 아닌 독립적인 제작 워크플로입니다.

| 스킬 | 가장 잘 맞는 작업 | 기본 결과 |
| --- | --- | --- |
| [`remotion-lesson-video`](skills/remotion-lesson-video/SKILL.md) | 실제 조작 녹화 편집, 여러 차시, 다국어 강의 | MP4, 자막, 대본, 편집 소스·검수 기록 |
| [`canva-video-maker`](skills/canva-video-maker/SKILL.md) | 캡처·강조·장면별 음성으로 만드는 Canva 교육영상 | MP4, SRT, 대본, 입력 자료·검수 기록 |

> v2 안내: v1.0의 두 번째 스킬은 제작 방식 오해로 Canva 편집기 안의 영상 편집을 설명했습니다. v2는 기존 캔바 교육영상 프로젝트의 캡처·음성·Python/FFmpeg 방식으로 바로잡았습니다. 기존 설치는 아래 `--update`로 백업 후 갱신하세요.

## 필요한 것

스킬은 AI에게 제작 절차를 알려 주는 파일입니다. 설치만으로 Canva 계정, 화면 녹화 권한, 음성 서비스, 영상 편집 도구가 생기지는 않습니다. Claude/Codex 이용료, Canva·음성 서비스·Remotion의 사용 조건과 요금은 각 서비스 기준입니다.

| 실행 환경 | 준비 사항 | 범위 |
| --- | --- | --- |
| Claude Code / Codex | 스킬 설치와 필요한 파일·터미널·브라우저 도구 | 연결된 도구가 지원하는 실제 제작·검수 |
| Claude 웹·데스크톱의 사용자 스킬 기능 | 개별 스킬 ZIP 업로드, 기능 이용 권한 | 연결된 도구에 따라 제작 범위가 달라짐 |
| 리모션 영상 | Node.js, Remotion 실행 환경, 실제 녹화, 사용자 녹음 또는 TTS | 로컬 렌더에는 터미널과 실행 가능한 브라우저 필요 |
| 캡처 기반 영상 | Python 3.9+, Pillow, FFmpeg/FFprobe, 한국어 폰트, 실제 캡처·음성 | Canva 안에서 영상 편집하지 않고 로컬 MP4 제작 |

도구가 없는 환경에서는 대본·장면표 등 가능한 준비 작업과 필요한 원본 목록을 만듭니다. 실제 제작을 하지 않았는데 완료했다고 보고하지 않도록 구성했습니다. Claude Code와 Codex 데스크톱에서 두 제작 방식의 MP4를 실제로 만들었습니다. 실행 경로·보조 작업·검수 한계는 [실사용 검증 기록](VALIDATION.md)을 확인하세요. 웹·데스크톱·CLI 전체 조합이나 모든 운영체제를 검증한 것은 아닙니다.

## 설치: Claude Code와 Codex

Python 3.9 이상과 Git이 있으면 아래처럼 설치합니다. 설치 스크립트는 Python 표준 라이브러리만 사용하고 **기존 같은 이름의 스킬은 덮어쓰지 않습니다.**

```bash
git clone https://github.com/contenjoo/educational-video-skills.git
cd educational-video-skills
python3 scripts/install.py --target both --dry-run
python3 scripts/install.py --target both
```

첫 제작 전 준비 검사를 실행하면 도구가 빠졌거나 네트워크가 막힌 상태에서 긴 제작을 시작하는 일을 줄일 수 있습니다.

```bash
python3 skills/remotion-lesson-video/scripts/preflight.py --mode remotion --network
python3 -m venv .venv
.venv/bin/python -m pip install "Pillow>=10,<13"
.venv/bin/python skills/canva-video-maker/scripts/preflight.py --mode canva
```

macOS 시스템 한국어 음성을 쓸 경우 첫 명령에 `--tts`를 추가하세요. Windows/Linux에서는 사용자 녹음이나 해당 환경의 TTS를 선택하면 됩니다. 준비 검사를 통과해도 실제 로그인·모델 호출·영상 제작·재생은 별도 확인이 필요합니다. 각 스킬의 `references/first-run.md`에 실제 검증에서 관찰한 오류와 대응을 정리했습니다.

Windows에서 `python3` 명령이 없으면 `python`을 사용합니다. 한 제품만 쓰려면 `--target claude` 또는 `--target codex`를 선택합니다.

| 대상 | 개인 설치 경로 | 프로젝트 설치 경로 |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |

현재 프로젝트에만 설치하려면 **설치할 프로젝트의 절대 경로**를 지정합니다.

```bash
python3 scripts/install.py --target both --scope project --project /path/to/your-project
```

수동 설치는 `skills/` 안의 두 스킬 폴더를 해당 경로에 복사하면 됩니다. 같은 이름이 이미 있을 때 기본 설치는 중단합니다. 아래 업데이트 명령을 선택하면 기존 폴더를 해당 제품의 `skill-backups/`에 보존한 뒤 새 버전을 설치합니다.

```bash
git pull --ff-only
python3 scripts/install.py --target both --update
```

백업 폴더는 자동 삭제하지 않습니다. Codex에 이전 `canva-video-maker`가 다른 검색 경로로 설치되어 있으면 중복 표시될 수 있으므로 검색 경로 전체를 확인하세요. 설치 후 새 대화에서 확인하고 필요하면 앱을 다시 시작하세요.

공식 설치 기준: [Codex 스킬](https://developers.openai.com/codex/skills/), [Claude Code 스킬](https://code.claude.com/docs/en/skills).

## 설치: Claude 웹·데스크톱

1. [최신 릴리스](https://github.com/contenjoo/educational-video-skills/releases/latest)에서 `remotion-lesson-video.zip`과 `canva-video-maker.zip`을 내려받습니다.
2. Claude의 사용자 스킬 관리 화면에서 각 ZIP을 업로드하고 활성화합니다. 정확한 메뉴와 사용 가능 여부는 [Claude 공식 안내](https://support.claude.com/en/articles/12512180-use-skills-in-claude)를 확인하세요. 조직 설정에 따라 업로드가 제한될 수 있습니다.
3. 필요한 터미널·브라우저·파일 도구를 사용할 수 있는지 확인하고 아래 예시로 요청합니다.

GitHub의 저장소 전체 ZIP 대신 **개별 스킬 ZIP**을 업로드하세요. 개별 ZIP은 최상위 스킬 폴더 안에 `SKILL.md`가 있는 형식입니다. 음성 생성이나 로컬 렌더 도구가 연결되지 않은 환경은 실행 가능한 준비 자료까지 제공합니다.

## 사용 예시

Codex:

```text
$remotion-lesson-video
초보 교사를 위한 캔바 포스터 만들기 영상을 만들어줘.
내가 제공한 실제 조작 녹화를 사용하고, 한국어 자막과 따라 할 시간을 넣어줘.
```

```text
$canva-video-maker
실제 캔바 화면 캡처로 텍스트 상자 추가 방법을 설명하는 교육영상을 만들어줘.
Python/Pillow·FFmpeg 방식으로 한국어 음성·자막과 클릭 위치 네모를 넣어줘.
```

Claude Code에서는 `/remotion-lesson-video`, `/canva-video-maker`로 호출할 수 있습니다. Claude 웹·데스크톱에서는 스킬을 켠 뒤 이름을 말하며 요청하세요. 일반 문장으로 목적과 제작 방식을 지정해도 AI가 해당 스킬을 선택할 수 있습니다.

## 제작 원칙

- 실제 녹화와 정지 캡처를 구분합니다. 조작 시연은 클릭·입력·메뉴 전환이 담긴 녹화를 우선합니다.
- 특정 음성 서비스나 화자를 강제하지 않습니다. 본인의 녹음이나 연결 가능한 TTS를 사용할 수 있습니다.
- 캡처 기반 방식은 화면 확인 후 대본을 확정하고 동봉 렌더러를 재사용합니다. Canva 타임라인 편집·업로드는 필요하지 않습니다.
- 파일 검사, 자동 음성 검사, 실제 사람의 시청·청취 결과를 구분합니다.
- 제작 요청에 포함되지 않은 외부 게시·공유·기존 강의 교체를 자동으로 수행하지 않습니다.

## 검증과 ZIP 만들기

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

`dist/`에 두 개의 독립적인 스킬 ZIP을 만듭니다. 검증은 YAML·구조·상대 참조·배포 파일의 개인 환경 의존성을 검사합니다. 실제 Canva 로그인·음성 생성·녹화·리모션 렌더 성공을 보증하는 검사는 아닙니다.

문제나 개선 제안은 [Issues](https://github.com/contenjoo/educational-video-skills/issues)에 남겨 주세요. 오류 기록에는 비밀번호·API 키·학생 개인정보를 포함하지 마세요.

## License

[MIT](LICENSE). 이 저장소의 스킬·문서·도구에 적용됩니다. 외부 서비스, 사용자 녹화, 폰트, 사진·영상 및 음성의 권리는 각 권리자와 사용 조건을 따릅니다.
