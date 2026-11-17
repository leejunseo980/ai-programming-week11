# test_ai_B.py — 프롬프트 B (명세 6칸만 주고 받은 테스트, 코드는 보여주지 않음)
# 주의: 고치지 않고 그대로 저장하는 것이 실험 규칙입니다.
import pytest

from load_scores import load_scores


def make(tmp_path, body):
    p = tmp_path / "scores.csv"
    p.write_text("name,score\n" + body, encoding="utf-8")
    return str(p)


def test_normal_file_returns_valid_scores(tmp_path):
    kept, skipped = load_scores(make(tmp_path, "김하나,88\n이두리,70\n"))
    assert list(kept) == [("김하나", 88), ("이두리", 70)]
    assert len(skipped) == 0


def test_blank_line_is_skipped_silently(tmp_path):
    kept, skipped = load_scores(make(tmp_path, "김하나,88\n\n이두리,70\n"))
    assert len(kept) == 2
    assert len(skipped) == 0


def test_name_with_comma_in_quotes(tmp_path):
    kept, _ = load_scores(make(tmp_path, '"최,네번",77\n'))
    assert kept[0][0] == "최,네번"
    assert kept[0][1] == 77


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(str(tmp_path / "nope.csv"))


def test_header_only_returns_empty(tmp_path):
    kept, skipped = load_scores(make(tmp_path, ""))
    assert len(kept) == 0
    assert len(skipped) == 0


def test_wrong_number_of_columns_skipped(tmp_path):
    kept, skipped = load_scores(make(tmp_path, "김하나,88,추가\n"))
    assert len(kept) == 0
    assert len(skipped) == 1


def test_missing_score_skipped(tmp_path):
    kept, skipped = load_scores(make(tmp_path, "김하나,\n"))
    assert len(kept) == 0
    assert len(skipped) == 1


def test_non_numeric_score_skipped(tmp_path):
    kept, skipped = load_scores(make(tmp_path, "한겨울,결석\n"))
    assert len(kept) == 0
    assert len(skipped) == 1


def test_missing_name_skipped(tmp_path):
    kept, skipped = load_scores(make(tmp_path, ",90\n"))
    assert len(kept) == 0
    assert len(skipped) == 1


def test_duplicate_names_both_kept(tmp_path):
    kept, _ = load_scores(make(tmp_path, "김하나,88\n김하나,91\n"))
    assert len(kept) == 2


@pytest.mark.parametrize("score", [0, 1, 50, 99, 100])
def test_valid_scores_kept(tmp_path, score):
    kept, skipped = load_scores(make(tmp_path, f"A,{score}\n"))
    assert len(kept) == 1
    assert len(skipped) == 0


@pytest.mark.parametrize("score", [-1, 101, 1000, -100])
def test_out_of_range_scores_skipped(tmp_path, score):
    kept, skipped = load_scores(make(tmp_path, f"A,{score}\n"))
    assert len(kept) == 0
    assert len(skipped) == 1


def test_skipped_record_has_line_number(tmp_path):
    _, skipped = load_scores(make(tmp_path, "A,80\nB,500\n"))
    assert skipped[0][0] == 3
