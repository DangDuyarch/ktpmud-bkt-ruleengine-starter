"""Vi du minh hoa dinh dang test - KHONG phai bo test an dung de cham diem.
Sinh vien tu viet them test cho du cac muc nguy co theo dac ta.
"""
import pytest

from rule_engine.classifier import classify


def test_classify_is_implemented():
    """Vi du khung: thay bang case that theo Data Dictionary khi de bai duoc cong bo."""
    with pytest.raises(NotImplementedError):
        classify({"uas7_score": 0, "has_angioedema": False, "duration_weeks": 0})
