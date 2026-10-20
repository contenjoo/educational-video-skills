# 교육영상 만들기 스킬 · Educational Video Skills

**Claude와 Codex에서 사용하는 두 가지 교육영상 제작 스킬입니다.** 실제 조작 화면으로 따라 하기 영상을 만들거나, Canva에서 직접 수정할 수 있는 동영상 프로젝트를 만듭니다.

누구나 내려받아 사용·수정·재배포할 수 있습니다(MIT). 개인 계정, API 키, 특정 목소리, 기존 강의 원본은 포함하지 않습니다. Canva와 Remotion의 공식 배포물이 아닌 독립적인 제작 워크플로입니다.

| 스킬 | 가장 잘 맞는 작업 | 기본 결과 |
| --- | --- | --- |
| [`remotion-lesson-video`](skills/remotion-lesson-video/SKILL.md) | 실제 조작 녹화 편집, 여러 차시, 다국어 강의 | MP4, 자막, 대본, 편집 소스·검수 기록 |
| [`canva-video-maker`](skills/canva-video-maker/SKILL.md) | Canva에서 고쳐 쓸 수 있는 교육·안내 영상 | 편집 가능한 Canva 동영상과 링크·검수 기록 |

## 필요한 것

스킬은 AI에게 제작 절차를 알려 주는 파일입니다. 설치만으로 Canva 계정, 화면 녹화 권한, 음성 서비스, 영상 편집 도구가 생기지는 않습니다. Claude/Codex 이용료, Canva·음성 서비스·Remotion의 사용 조건과 요금은 각 서비스 기준입니다.

| 실행 환경 | 준비 사항 | 범위 |
| --- | --- | --- |
| Claude Code / Codex | 스킬 설치와 필요한 파일·터미널·브라우저 도구 | 연결된 도구가 지원하는 실제 제작·검수 |
| Claude 웹·데스크톱의 사용자 스킬 기능 | 개별 스킬 ZIP 업로드, 기능 이용 권한 | 연결된 도구에 따라 제작 범위가 달라짐 |
| 리모션 영상 | Node.js, Remotion 실행 환경, 실제 녹화, 사용자 녹음 또는 TTS | 로컬 렌더에는 터미널과 실행 가능한 브라우저 필요 |
| Canva 영상 | 본인의 Canva 계정과 편집 가능한 도구 | Canva 연결 도구 또는 지원되는 브라우저 조작 필요 |

도구가 없는 환경에서는 대본·장면표 등 가능한 준비 작업과 필요한 원본 목록을 만듭니다. 실제 편집이나 저장을 하지 않았는데 완료했다고 보고하지 않도록 구성했습니다. Claude와 Codex의 **공통 SKILL.md 형식으로 작성하고 구조를 검사**했으며, 모든 제품·계정에서 실제 제작을 끝까지 실행해 검증한 것은 아닙니다.

## 설치: Claude Code와 Codex

Python 3.9 이상과 Git이 있으면 아래처럼 설치합니다. 설치 스크립트는 Python 표준 라이브러리만 사용하고 **기존 같은 이름의 스킬은 덮어쓰지 않습니다.**

```bash
git clone https://github.com/contenjoo/educational-video-skills.git
cd educational-video-skills
python3 scripts/install.py --target both --dry-run
python3 scripts/install.py --target both
```

Windows에서 `python3` 명령이 없으면 `python`을 사용합니다. 한 제품만 쓰려면 `--target claude` 또는 `--target codex`를 선택합니다.

| 대상 | 개인 설치 경로 | 프로젝트 설치 경로 |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |

현재 프로젝트에만 설치하려면 **설치할 프로젝트의 절대 경로**를 지정합니다.

```bash
python3 scripts/install.py --target both --scope project --project /path/to/your-project
```

수동 설치는 `skills/` 안의 두 스킬 폴더를 해당 경로에 복사하면 됩니다. 같은 이름의 스킬이 이미 있다면 내용을 비교하고 기존 스킬을 별도로 보존한 뒤 교체 여부를 결정하세요. Codex에 이전 `canva-video-maker`가 다른 검색 경로로 설치되어 있으면 중복 표시될 수 있으므로 검색 경로 전체를 확인하세요. 설치 후 새 대화에서 확인하고 필요하면 앱을 다시 시작하세요.

공식 설치 기준: [Codex 스킬](https://developers.openai.com/codex/skills/), [Claude Code 스킬](https://code.claude.com/docs/en/skills).

## 설치: Claude 웹·데스크톱

1. [최신 릴리스](https://github.com/contenjoo/educational-video-skills/releases/latest)에서 `remotion-lesson-video.zip`과 `canva-video-maker.zip`을 내려받습니다.
2. Claude의 사용자 스킬 관리 화면에서 각 ZIP을 업로드하고 활성화합니다. 정확한 메뉴와 사용 가능 여부는 [Claude 공식 안내](https://support.claude.com/en/articles/12512180-use-skills-in-claude)를 확인하세요. 조직 설정에 따라 업로드가 제한될 수 있습니다.
3. 필요한 Canva·브라우저·파일 도구를 사용할 수 있는지 확인하고 아래 예시로 요청합니다.

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
캔바에서 직접 수정할 수 있는 1분짜리 학급 소식지 안내 영상을 만들어줘.
Canva 내장 한국어 음성과 실제 화면을 사용해줘.
```

Claude Code에서는 `/remotion-lesson-video`, `/canva-video-maker`로 호출할 수 있습니다. Claude 웹·데스크톱에서는 스킬을 켠 뒤 이름을 말하며 요청하세요. 일반 문장으로 목적과 제작 방식을 지정해도 AI가 해당 스킬을 선택할 수 있습니다.

## 제작 원칙

- 실제 녹화와 정지 캡처를 구분합니다. 조작 시연은 클릭·입력·메뉴 전환이 담긴 녹화를 우선합니다.
- 특정 음성 서비스나 화자를 강제하지 않습니다. 본인의 녹음이나 연결 가능한 TTS를 사용할 수 있습니다.
- Canva 작업은 현재 지원 API를 우선하고 필요한 구간만 편집기를 조작합니다.
- 파일 검사, 자동 음성 검사, 실제 사람의 시청·청취 결과를 구분합니다.
- 제작 요청에 포함되지 않은 외부 게시·공유·기존 강의 교체를 자동으로 수행하지 않습니다.

## 검증과 ZIP 만들기

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 scripts/package.py
```

`dist/`에 두 개의 독립적인 스킬 ZIP을 만듭니다. 검증은 YAML·구조·상대 참조·배포 파일의 개인 환경 의존성을 검사합니다. 실제 Canva 로그인·음성 생성·녹화·리모션 렌더 성공을 보증하는 검사는 아닙니다.

문제나 개선 제안은 [Issues](https://github.com/contenjoo/educational-video-skills/issues)에 남겨 주세요. 오류 기록에는 비밀번호·API 키·학생 개인정보를 포함하지 마세요.

## License

[MIT](LICENSE). 이 저장소의 스킬·문서·도구에 적용됩니다. 외부 서비스, 사용자 녹화, 폰트, 사진·영상 및 음성의 권리는 각 권리자와 사용 조건을 따릅니다.
