# 성적 관리 프로그램 (load_scores)

## 무엇을 하나요 (What)
성적 CSV 파일을 읽어 유효한 점수(0~100 정수)만 골라 내고, 건너뛴 줄은 줄 번호와 이유와 함께 기록합니다.

## 왜 만들었나요 (Why)
실제 성적 파일에는 빈 칸 · 범위 밖 점수 · 열 개수가 다른 줄 · 동명이인이 섞여 있어, 그냥 읽으면 프로그램이 죽거나 잘못된 평균이 나옵니다. 그래서 "무엇을 버렸고 왜 버렸는지"를 남기면서 읽는 함수가 필요했습니다. 같은 이름은 동명이인일 수 있으므로 지우지 않고 둘 다 남깁니다.

## 어떻게 쓰나요 (How)
Python 3.10 이상이 필요합니다.

```bash
python load_scores.py scores.csv
```

출력 예: `읽은 줄 : 5개` / `건너뛴 줄 : 5개` 와 각 줄의 사유.

## 어떻게 테스트하나요
```bash
pip install pytest pytest-cov
pytest
pytest --cov=load_scores --cov-report=term-missing
```

통과 화면:

```
test_load_scores.py ...............                                      [100%]
load_scores.py      45      0   100%
15 passed
```

## 파일 구성
| 파일 | 역할 |
| --- | --- |
| `load_scores.py` | 성적 CSV를 읽는 함수 `load_scores(path)` |
| `test_load_scores.py` | 직접 만든 테스트 (정상 · 예외 · 경계값) |
| `test_ai_A.py` | AI에게 코드를 주고 받은 테스트 (비교용) |
| `test_ai_B.py` | AI에게 명세를 주고 받은 테스트 (비교용) |
| `scores.csv` · `empty.csv` · `weird.csv` | 테스트용 입력 파일 |
| `bug3_logic.py` · `prompts.txt` | 함정 실험용 코드 · 프롬프트 원문 |

## 만든 사람
- 이름 · 학번: 이준서 (학번은 직접 입력)
- AI 사용: 테스트 코드와 README 초안 작성에 Claude를 사용했고, 케이스 설계와 결과 확인은 직접 했습니다.
