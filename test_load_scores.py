# test_load_scores.py — 설계표의 여덟 케이스 (정상 3 · 예외 2 · 경계 3)
import pytest

from load_scores import load_scores


# ---------- 정상 ----------
def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5
    assert ("김하나", 88) in kept
    assert ("서한별", 95) in kept


def test_빈_줄은_건너뛴다():
    kept, skipped = load_scores("scores.csv")
    # scores.csv 10행은 빈 줄 — 기록(skipped)에 나타나면 안 된다
    assert all(line_no != 10 for line_no, _, _ in skipped)
    assert len(skipped) == 5


def test_이름에_쉼표가_있어도_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert ("최,네번", 77) in kept


# ---------- 예외 ----------
def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []


# ---------- 경계 ----------
def _쓰기(경로, 점수):
    경로.write_text(f"name,score\n홍길동,{점수}\n", encoding="utf-8")


@pytest.mark.parametrize("점수, 유효한가", [
    (-1, False),    # 경계 바로 아래
    (0, True),      # ★ 아래쪽 경계
    (1, True),
    (99, True),
    (100, True),    # ★ 위쪽 경계
    (101, False),   # 경계 바로 위
])
def test_점수_경계값(tmp_path, 점수, 유효한가):
    임시 = tmp_path / "임시.csv"
    _쓰기(임시, 점수)
    kept, skipped = load_scores(str(임시))
    assert (len(kept) == 1) == 유효한가


# ---------- 기록표 ②에서 추가한 테스트 (안 지나간 줄 → 입력) ----------
def test_weird_파일은_유효한_줄만_남긴다():
    # 이름 빈칸 · 점수 빈칸 · 범위 밖 · 소수 · "7 2" 등이 섞인 파일
    kept, skipped = load_scores("weird.csv")
    assert kept == [("한겨울", 77), ("윤보람", 88)]
    assert len(skipped) == 7


def test_열_개수가_다르면_건너뛰고_이유를_적는다():
    kept, skipped = load_scores("scores.csv")
    이유 = {line_no: why for line_no, _, why in skipped}
    assert 이유[9] == "열 개수가 2가 아님"
    assert 이유[4] == "점수가 비어 있음"
    assert 이유[8] == "점수가 정수가 아님"


def test_같은_이름은_둘_다_남긴다():
    kept, _ = load_scores("scores.csv")
    assert [s for n, s in kept if n == "김하나"] == [88, 91]


def test_직접_실행하면_결과를_출력한다(capsys, monkeypatch):
    import runpy
    import sys

    monkeypatch.setattr(sys, "argv", ["load_scores.py", "weird.csv"])
    runpy.run_path("load_scores.py", run_name="__main__")
    out = capsys.readouterr().out
    assert "읽은 줄 : 2개" in out
    assert "건너뛴 줄 : 7개" in out