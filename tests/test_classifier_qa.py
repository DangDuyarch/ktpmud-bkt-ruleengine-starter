
import pytest

from rule_engine.classifier import classify


def tao_benh_nhan(**overrides):
    """Tạo dữ liệu kiểm thử mặc định, cho phép thay đổi từng trường."""
    patient = {
        "tuoi": 25,
        "huyet_ap_tam_thu": 120,
        "huyet_ap_tam_thu_nen": 120,
        "co_di_nguyen_nghi_ngo": False,
        "di_nguyen_qua_duong_hit": False,
        "co_ton_thuong_da_niem_mac": False,
        "co_trieu_chung_ho_hap": False,
        "co_trieu_chung_tuan_hoan": False,
        "co_trieu_chung_tieu_hoa_nang": False,
    }
    patient.update(overrides)
    return patient


def test_r01_phan_ve_khong_ro_di_nguyen():
    patient = tao_benh_nhan(
        co_ton_thuong_da_niem_mac=True,
        co_trieu_chung_ho_hap=True,
    )

    result = classify(patient)

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R01-PV"


def test_r02_phan_ve_tu_hai_he_co_quan():
    patient = tao_benh_nhan(
        co_di_nguyen_nghi_ngo=True,
        co_ton_thuong_da_niem_mac=True,
        co_trieu_chung_tieu_hoa_nang=True,
    )

    result = classify(patient)

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R02-PV"


def test_r03_phan_ve_co_di_nguyen_khong_qua_duong_hit():
    patient = tao_benh_nhan(
        co_di_nguyen_nghi_ngo=True,
        di_nguyen_qua_duong_hit=False,
        co_trieu_chung_ho_hap=True,
    )

    result = classify(patient)

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R03-PV"


def test_khong_du_dieu_kien_thi_theo_doi():
    patient = tao_benh_nhan()

    result = classify(patient)

    assert result["muc_do"] == "THEO_DOI"
    assert result["rule_id"] is None


def test_dau_ra_co_du_cac_truong_bat_buoc():
    patient = tao_benh_nhan()

    result = classify(patient)

    assert set(result.keys()) == {"muc_do", "rule_id", "ly_do"}
    assert isinstance(result["ly_do"], str)
