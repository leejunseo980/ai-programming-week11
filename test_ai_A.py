# test_ai_A.py — 프롬프트 A (load_scores.py 코드를 보여주고 받은 테스트)
# 주의: 고치지 않고 그대로 저장하는 것이 실험 규칙입니다.
import pytest

from load_scores import load_scores, MIN_SCORE, MAX_SCORE


def write_csv(tmp_path, text):
    p = tmp_path / "data.csv"
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_valid_rows(tmp_path):
    path = write_csv(tmp_path, "name,score\nA,80\nB,90\n")
    kept, skipped = load_scores(path)
    assert kept == [("A", 80), ("B", 90)]
    assert skipped == []


def test_blank_lines_are_ignored_without_record(tmp_path):
    path = write_csv(tmp_path, "name,score\n\nA,80\n\n")
    kept, skipped = load_scores(path)
    assert kept == [("A", 80)]
    assert skipped == []


def test_quoted_comma_in_name(tmp_path):
    path = write_csv(tmp_path, 'name,score\n"Kim,Jr",70\n')
    kept, _ = load_scores(path)
    assert kept == [("Kim,Jr", 70)]


def test_whitespace_is_stripped(tmp_path):
    path = write_csv(tmp_path, "name,score\n  A  ,  77 \n")
    kept, _ = load_scores(path)
    assert kept == [("A", 77)]


def test_duplicate_names_are_kept(tmp_path):
    path = write_csv(tmp_path, "name,score\nA,10\nA,20\n")
    kept, _ = load_scores(path)
    assert kept == [("A", 10), ("A", 20)]


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_scores("does_not_exist.csv")


def test_header_only(tmp_path):
    path = write_csv(tmp_path, "name,score\n")
    assert load_scores(path) == ([], [])


def test_wrong_column_count(tmp_path):
    path = write_csv(tmp_path, "name,score\nA,80,extra\nB\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert [s[2] for s in skipped] == ["열 개수가 2가 아님"] * 2


def test_empty_name(tmp_path):
    path = write_csv(tmp_path, "name,score\n,80\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped == [(2, ",80", "이름이 비어 있음")]


def test_empty_score(tmp_path):
    path = write_csv(tmp_path, "name,score\nA,\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped == [(2, "A,", "점수가 비어 있음")]


@pytest.mark.parametrize("raw", ["abc", "88.5", "7 2"])
def test_non_integer_score(tmp_path, raw):
    path = write_csv(tmp_path, f"name,score\nA,{raw}\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped[0][2] == "점수가 정수가 아님"


@pytest.mark.parametrize("score, ok", [
    (MIN_SCORE - 1, False),
    (MIN_SCORE, True),
    (MIN_SCORE + 1, True),
    (MAX_SCORE - 1, True),
    (MAX_SCORE, True),
    (MAX_SCORE + 1, False),
])
def test_score_boundaries(tmp_path, score, ok):
    path = write_csv(tmp_path, f"name,score\nA,{score}\n")
    kept, skipped = load_scores(path)
    assert (len(kept) == 1) == ok
    assert (len(skipped) == 1) == (not ok)


def test_line_numbers_are_one_based(tmp_path):
    path = write_csv(tmp_path, "name,score\nA,80\nB,999\n")
    _, skipped = load_scores(path)
    assert skipped[0][0] == 3


def test_bom_header(tmp_path):
    p = tmp_path / "bom.csv"
    p.write_bytes("name,score\nA,80\n".encode("utf-8-sig"))
    kept, _ = load_scores(str(p))
    assert kept == [("A", 80)]
