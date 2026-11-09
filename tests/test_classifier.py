"""Bộ Unit Test đầy đủ cho rule_engine/classifier.py."""

import pytest
from rule_engine.classifier import classify


# --- 1. TEST TẦNG 2: R01, R02, R03 ---

def test_r01_success():
    """R01: Không dị nguyên + Da niêm mạc + Hô hấp."""
    patient = {
        "tuoi": 20.0,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 120,
    }
    res = classify(patient)
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R01-PV"


def test_r02_success():
    """R02: Có dị nguyên + 2/4 hệ cơ quan (Da + Tiêu hóa)."""
    patient = {
        "tuoi": 15.0,
        "co_di_nguyen_nghi_ngo": True,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_tieu_hoa_nang": True,
        "huyet_ap_tam_thu": 110,
    }
    res = classify(patient)
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R02-PV"


def test_r03_success():
    """R03: Có dị nguyên + Đường hít False + Hô hấp True."""
    patient = {
        "tuoi": 30.0,
        "co_di_nguyen_nghi_ngo": True,
        "di_nguyen_qua_duong_hit": False,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 115,
    }
    res = classify(patient)
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R03-PV"


def test_rule_conflict_r02_and_r03():
    """Trường hợp thỏa mãn cả R02 và R03: Trả về R02-PV theo ưu tiên."""
    patient = {
        "tuoi": 25.0,
        "co_di_nguyen_nghi_ngo": True,
        "di_nguyen_qua_duong_hit": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 120,
    }
    res = classify(patient)
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R02-PV"


# --- 2. TEST TẦNG 1: R-SOC VÀ KIỂM THỬ BIÊN ---

@pytest.mark.parametrize(
    "tuoi, hatt, hatt_nen, expected_muc_do, expected_rule",
    [
        # Tuổi < 1 (Ngưỡng 70)
        (0.5, 69, None, "SOC_PHAN_VE", "R-SOC"),
        (0.5, 70, None, "PHAN_VE", "R01-PV"),
        # Tuổi 1 đến <11 (Ngưỡng 70 + 2*tuoi)
        (1.0, 71, None, "SOC_PHAN_VE", "R-SOC"),
        (1.0, 72, None, "PHAN_VE", "R01-PV"),
        (5.0, 79, None, "SOC_PHAN_VE", "R-SOC"),
        (5.0, 80, None, "PHAN_VE", "R01-PV"),
        # Tuổi 11 đến <18 (Ngưỡng 90)
        (11.0, 89, None, "SOC_PHAN_VE", "R-SOC"),
        (11.0, 90, None, "PHAN_VE", "R01-PV"),
        # Tuổi >= 18 (HATT < 90)
        (18.0, 89, None, "SOC_PHAN_VE", "R-SOC"),
        (18.0, 90, None, "PHAN_VE", "R01-PV"),
        # Tuổi >= 18 (Xét mức giảm % so với nền)
        (30.0, 84, 120, "PHAN_VE", "R01-PV"),
        (30.0, 83, 120, "SOC_PHAN_VE", "R-SOC"),
    ],
)
def test_soc_boundaries(tuoi, hatt, hatt_nen, expected_muc_do, expected_rule):
    """Kiểm thử biên huyết áp theo độ tuổi."""
    patient = {
        "tuoi": tuoi,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": hatt,
        "huyet_ap_tam_thu_nen": hatt_nen,
    }
    res = classify(patient)
    assert res["muc_do"] == expected_muc_do
    assert res["rule_id"] == expected_rule


# --- 3. TEST DỮ LIỆU THIẾU VÀ TRƯỜNG HỢP KHÔNG KHỚP ---

def test_missing_tuoi():
    """Thiếu trường tuổi -> THEO_DOI."""
    patient = {
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
    }
    res = classify(patient)
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_missing_huyet_ap():
    """Có phản vệ nhưng thiếu huyết áp tâm thu -> Trả PHAN_VE."""
    patient = {
        "tuoi": 25.0,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": None,
    }
    res = classify(patient)
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R01-PV"


def test_no_rules_matched():
    """Không có triệu chứng -> THEO_DOI."""
    patient = {
        "tuoi": 20.0,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": False,
    }
    res = classify(patient)
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None