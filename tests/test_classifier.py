"""Bộ Unit Test hoàn chỉnh."""

import pytest
from rule_engine.classifier import classify


#1. MA TRẬN 18 TÌNH HUỐNG (MỤC 10)
def test_tc01_r01_pv():
    patient = {
        "tuoi": 30.0,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 120,
    }
    res = classify(patient)
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R01-PV"


def test_tc02_r_soc():
    patient = {
        "tuoi": 30.0,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 85,
    }
    res = classify(patient)
    assert res["muc_do"] == "SOC_PHAN_VE"
    assert res["rule_id"] == "R-SOC"


def test_tc03_r02_pv():
    patient = {
        "tuoi": 20.0,
        "co_di_nguyen_nghi_ngo": True,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_tieu_hoa_nang": True,
        "co_trieu_chung_ho_hap": False,
        "co_trieu_chung_tuan_hoan": False,
        "huyet_ap_tam_thu": 110,
    }
    res = classify(patient)
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R02-PV"


def test_tc04_r03_pv():
    patient = {
        "tuoi": 20.0,
        "co_di_nguyen_nghi_ngo": True,
        "di_nguyen_qua_duong_hit": False,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 110,
    }
    res = classify(patient)
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R03-PV"


def test_tc05_r03_hit_true_only_respiratory():
    patient = {
        "tuoi": 20.0,
        "co_di_nguyen_nghi_ngo": True,
        "di_nguyen_qua_duong_hit": True,
        "co_trieu_chung_ho_hap": True,
        "co_ton_thuong_da_niem_mac": False,
        "co_trieu_chung_tuan_hoan": False,
        "co_trieu_chung_tieu_hoa_nang": False,
    }
    res = classify(patient)
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_tc08_and_09_boundary_drop_30_percent():
    # Giảm đúng 30%: HATT 140 -> 98 -> PHAN_VE
    p_exact = {
        "tuoi": 25.0,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 98,
        "huyet_ap_tam_thu_nen": 140,
    }
    assert classify(p_exact)["muc_do"] == "PHAN_VE"

    # Giảm > 30%: HATT 140 -> 97 -> SOC_PHAN_VE
    p_more = {
        "tuoi": 25.0,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 97,
        "huyet_ap_tam_thu_nen": 140,
    }
    assert classify(p_more)["muc_do"] == "SOC_PHAN_VE"


def test_tc12_missing_tuoi():
    patient = {
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
    }
    res = classify(patient)
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_tc18_validation_before_missing_tuoi():
    # tuoi = None và co_di_nguyen_nghi_ngo = "true" (chuỗi) -> BẮT LỖI TypeError trước khi xét missing tuổi
    with pytest.raises(TypeError):
        classify({"tuoi": None, "co_di_nguyen_nghi_ngo": "true"})


#2. TEST VALIDATION LỖI (TYPEERROR & VALUEERROR)

def test_invalid_type_age_str():
    with pytest.raises(TypeError):
        classify({"tuoi": "30"})


def test_invalid_type_bool_int():
    # Bool nhận số 1 -> TypeError
    with pytest.raises(TypeError):
        classify({"tuoi": 20.0, "co_di_nguyen_nghi_ngo": 1})


def test_invalid_value_extra_key_pii():
    with pytest.raises(ValueError):
        classify({"tuoi": 30, "ten_benh_nhan": "Nguyen Van A"})


def test_invalid_value_negative_bp():
    with pytest.raises(ValueError):
        classify({"tuoi": 30, "huyet_ap_tam_thu": -10})