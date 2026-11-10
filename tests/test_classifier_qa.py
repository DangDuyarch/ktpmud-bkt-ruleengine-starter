import math

import pytest

from rule_engine.classifier import classify


# ============================================================
# Ham tao du lieu kiem thu mac dinh
# ============================================================

def tao_benh_nhan(**overrides):
    """Tao du lieu synthetic hop le, cho phep thay doi tung truong."""
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


def tao_benh_nhan_phan_ve(**overrides):
    """Tao benh nhan khop R01, mac dinh khong tut huyet ap."""
    patient = tao_benh_nhan(
        co_di_nguyen_nghi_ngo=False,
        co_ton_thuong_da_niem_mac=True,
        co_trieu_chung_ho_hap=True,
    )
    patient.update(overrides)
    return patient


# ============================================================
# A-01, A-03: Kiem thu cac rule phan loai
# ============================================================

def test_r01_phan_ve_khong_ro_di_nguyen():
    result = classify(tao_benh_nhan(
        co_ton_thuong_da_niem_mac=True,
        co_trieu_chung_ho_hap=True,
    ))

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R01-PV"


def test_r01_khop_khi_co_trieu_chung_tuan_hoan():
    result = classify(tao_benh_nhan(
        co_ton_thuong_da_niem_mac=True,
        co_trieu_chung_tuan_hoan=True,
    ))

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R01-PV"


def test_r01_khong_khop_neu_thieu_ton_thuong_da_niem_mac():
    result = classify(tao_benh_nhan(
        co_trieu_chung_ho_hap=True,
    ))

    assert result["muc_do"] == "THEO_DOI"
    assert result["rule_id"] is None


def test_r02_phan_ve_tu_hai_he_co_quan():
    result = classify(tao_benh_nhan(
        co_di_nguyen_nghi_ngo=True,
        co_ton_thuong_da_niem_mac=True,
        co_trieu_chung_tieu_hoa_nang=True,
    ))

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R02-PV"


def test_r02_khong_khop_khi_chi_co_mot_he_co_quan():
    result = classify(tao_benh_nhan(
        co_di_nguyen_nghi_ngo=True,
        co_trieu_chung_ho_hap=True,
        di_nguyen_qua_duong_hit=True,
    ))

    assert result["muc_do"] == "THEO_DOI"
    assert result["rule_id"] is None


def test_r03_phan_ve_khi_di_nguyen_khong_qua_duong_hit():
    result = classify(tao_benh_nhan(
        co_di_nguyen_nghi_ngo=True,
        di_nguyen_qua_duong_hit=False,
        co_trieu_chung_ho_hap=True,
    ))

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R03-PV"


def test_r03_phan_ve_khi_co_trieu_chung_tuan_hoan():
    result = classify(tao_benh_nhan(
        co_di_nguyen_nghi_ngo=True,
        di_nguyen_qua_duong_hit=True,
        co_trieu_chung_tuan_hoan=True,
    ))

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R03-PV"


def test_r02_duoc_uu_tien_hon_r03_khi_cung_khop():
    result = classify(tao_benh_nhan(
        co_di_nguyen_nghi_ngo=True,
        di_nguyen_qua_duong_hit=False,
        co_ton_thuong_da_niem_mac=True,
        co_trieu_chung_ho_hap=True,
    ))

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R02-PV"


def test_tut_huyet_ap_don_doc_khong_du_ket_luan():
    result = classify(tao_benh_nhan(
        huyet_ap_tam_thu=50,
    ))

    assert result["muc_do"] == "THEO_DOI"
    assert result["rule_id"] is None


# ============================================================
# A-03: Kiem thu nguong soc theo tuoi
# ============================================================

@pytest.mark.parametrize(
    ("tuoi", "hatt", "muc_do"),
    [
        (0, 69, "SOC_PHAN_VE"),
        (0, 70, "PHAN_VE"),
        (0.5, 69, "SOC_PHAN_VE"),
        (0.5, 70, "PHAN_VE"),
        (5, 79, "SOC_PHAN_VE"),
        (5, 80, "PHAN_VE"),
        (10, 89, "SOC_PHAN_VE"),
        (10, 90, "PHAN_VE"),
        (11, 89, "SOC_PHAN_VE"),
        (11, 90, "PHAN_VE"),
        (17, 89, "SOC_PHAN_VE"),
        (17, 90, "PHAN_VE"),
        (18, 89, "SOC_PHAN_VE"),
        (18, 90, "PHAN_VE"),
    ],
)
def test_nguong_soc_theo_tuoi(tuoi, hatt, muc_do):
    result = classify(tao_benh_nhan_phan_ve(
        tuoi=tuoi,
        huyet_ap_tam_thu=hatt,
        huyet_ap_tam_thu_nen=120,
    ))

    assert result["muc_do"] == muc_do

    if muc_do == "SOC_PHAN_VE":
        assert result["rule_id"] == "R-SOC"
    else:
        assert result["rule_id"] == "R01-PV"


def test_nguoi_lon_giam_dung_30_phan_tram_khong_ket_luan_soc():
    result = classify(tao_benh_nhan_phan_ve(
        tuoi=25,
        huyet_ap_tam_thu=140,
        huyet_ap_tam_thu_nen=200,
    ))

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R01-PV"


def test_nguoi_lon_giam_tren_30_phan_tram_ket_luan_soc():
    result = classify(tao_benh_nhan_phan_ve(
        tuoi=25,
        huyet_ap_tam_thu=139,
        huyet_ap_tam_thu_nen=200,
    ))

    assert result["muc_do"] == "SOC_PHAN_VE"
    assert result["rule_id"] == "R-SOC"


def test_nguoi_lon_hatt_duoi_90_khong_can_hatt_nen():
    result = classify(tao_benh_nhan_phan_ve(
        tuoi=25,
        huyet_ap_tam_thu=89,
        huyet_ap_tam_thu_nen=None,
    ))

    assert result["muc_do"] == "SOC_PHAN_VE"
    assert result["rule_id"] == "R-SOC"


# ============================================================
# A-04: Du lieu thieu/null va logic ba trang thai
# ============================================================

@pytest.mark.parametrize("tuoi", [None])
def test_thieu_tuoi_tra_theo_doi(tuoi):
    result = classify(tao_benh_nhan_phan_ve(tuoi=tuoi))

    assert result["muc_do"] == "THEO_DOI"
    assert result["rule_id"] is None
    assert "tuoi" in result["ly_do"].lower()


def test_bo_trong_khoa_tuoi_tra_theo_doi():
    patient = tao_benh_nhan_phan_ve()
    patient.pop("tuoi")

    result = classify(patient)

    assert result["muc_do"] == "THEO_DOI"
    assert result["rule_id"] is None
    assert "tuoi" in result["ly_do"].lower()


def test_thieu_hatt_nhung_khop_rule_thi_phan_ve():
    result = classify(tao_benh_nhan_phan_ve(
        huyet_ap_tam_thu=None,
    ))

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R01-PV"
    assert "soc" in result["ly_do"].lower() or "huyet ap" in result["ly_do"].lower()


def test_thieu_khoa_hatt_nhung_khop_rule_thi_phan_ve():
    patient = tao_benh_nhan_phan_ve()
    patient.pop("huyet_ap_tam_thu")

    result = classify(patient)

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R01-PV"


def test_nguoi_lon_hatt_tu_90_tro_len_thieu_nen():
    result = classify(tao_benh_nhan_phan_ve(
        tuoi=25,
        huyet_ap_tam_thu=100,
        huyet_ap_tam_thu_nen=None,
    ))

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R01-PV"


def test_thieu_truong_bool_duoc_coi_la_unknown():
    result = classify(tao_benh_nhan(
        co_di_nguyen_nghi_ngo=None,
        co_ton_thuong_da_niem_mac=True,
        co_trieu_chung_ho_hap=True,
    ))

    assert result["muc_do"] == "THEO_DOI"
    assert result["rule_id"] is None


def test_rule_da_true_khong_bi_huy_vi_truong_khac_unknown():
    result = classify(tao_benh_nhan(
        co_di_nguyen_nghi_ngo=True,
        co_ton_thuong_da_niem_mac=True,
        co_trieu_chung_tieu_hoa_nang=True,
        di_nguyen_qua_duong_hit=None,
    ))

    assert result["muc_do"] == "PHAN_VE"
    assert result["rule_id"] == "R02-PV"


def test_r02_unknown_khi_chua_du_hai_true_nhung_con_unknown():
    result = classify(tao_benh_nhan(
        co_di_nguyen_nghi_ngo=True,
        co_ton_thuong_da_niem_mac=True,
        co_trieu_chung_ho_hap=None,
        co_trieu_chung_tuan_hoan=None,
        co_trieu_chung_tieu_hoa_nang=False,
    ))

    assert result["muc_do"] == "THEO_DOI"
    assert result["rule_id"] is None


# ============================================================
# A-04: Validation - sai kieu phai TypeError
# ============================================================

@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("tuoi", "25"),
        ("tuoi", True),
        ("tuoi", False),
        ("huyet_ap_tam_thu", 80.5),
        ("huyet_ap_tam_thu", "80"),
        ("huyet_ap_tam_thu", True),
        ("huyet_ap_tam_thu_nen", 120.5),
        ("huyet_ap_tam_thu_nen", "120"),
        ("huyet_ap_tam_thu_nen", False),
        ("co_di_nguyen_nghi_ngo", 1),
        ("di_nguyen_qua_duong_hit", 0),
        ("co_ton_thuong_da_niem_mac", "true"),
        ("co_trieu_chung_ho_hap", 1),
        ("co_trieu_chung_tuan_hoan", "False"),
        ("co_trieu_chung_tieu_hoa_nang", 0),
    ],
)
def test_sai_kieu_du_lieu_phat_sinh_type_error(field, value):
    patient = tao_benh_nhan(**{field: value})

    with pytest.raises(TypeError):
        classify(patient)


# ============================================================
# A-04: Validation - sai mien phai ValueError
# ============================================================

@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("tuoi", -1),
        ("tuoi", float("nan")),
        ("tuoi", float("inf")),
        ("tuoi", float("-inf")),
        ("huyet_ap_tam_thu", -1),
        ("huyet_ap_tam_thu_nen", 0),
        ("huyet_ap_tam_thu_nen", -1),
    ],
)
def test_sai_mien_du_lieu_phat_sinh_value_error(field, value):
    patient = tao_benh_nhan(**{field: value})

    with pytest.raises(ValueError):
        classify(patient)


def test_tuoi_va_huyet_ap_khong_tu_dat_gioi_han_tren():
    result = classify(tao_benh_nhan(
        tuoi=150,
        huyet_ap_tam_thu=200,
        huyet_ap_tam_thu_nen=200,
    ))

    assert result["muc_do"] == "THEO_DOI"
    assert result["rule_id"] is None


def test_khoa_ngoai_allowlist_phat_sinh_value_error():
    patient = tao_benh_nhan(ten="synthetic")

    with pytest.raises(ValueError):
        classify(patient)


def test_validate_truong_khong_lien_quan_truoc_khi_suy_luan():
    patient = tao_benh_nhan(
        co_ton_thuong_da_niem_mac=True,
        co_trieu_chung_ho_hap=True,
        co_trieu_chung_tieu_hoa_nang="sai-kieu",
    )

    with pytest.raises(TypeError):
        classify(patient)


def test_thieu_tuoi_khong_che_giau_loi_sai_kieu_o_truong_khac():
    patient = tao_benh_nhan(
        tuoi=None,
        co_di_nguyen_nghi_ngo="true",
    )

    with pytest.raises(TypeError):
        classify(patient)


# ============================================================
# A-05: Kiem tra contract dau ra va tinh tat dinh
# ============================================================

@pytest.mark.parametrize(
    "patient",
    [
        tao_benh_nhan(),
        tao_benh_nhan(
            co_ton_thuong_da_niem_mac=True,
            co_trieu_chung_ho_hap=True,
        ),
        tao_benh_nhan(
            co_di_nguyen_nghi_ngo=True,
            co_ton_thuong_da_niem_mac=True,
            co_trieu_chung_tieu_hoa_nang=True,
        ),
        tao_benh_nhan(tuoi=None),
    ],
)
def test_dau_ra_chi_co_ba_khoa(patient):
    result = classify(patient)

    assert set(result.keys()) == {"muc_do", "rule_id", "ly_do"}
    assert result["muc_do"] in {
        "SOC_PHAN_VE",
        "PHAN_VE",
        "THEO_DOI",
    }
    assert result["rule_id"] in {
        "R-SOC",
        "R01-PV",
        "R02-PV",
        "R03-PV",
        None,
    }
    assert isinstance(result["ly_do"], str)
    assert result["ly_do"].strip()


def test_theo_doi_luon_co_rule_id_none():
    result = classify(tao_benh_nhan())

    assert result["muc_do"] == "THEO_DOI"
    assert result["rule_id"] is None


def test_cung_input_cho_cung_ket_qua_phan_loai():
    patient = tao_benh_nhan_phan_ve()

    first = classify(patient)
    second = classify(patient)

    assert first["muc_do"] == second["muc_do"]
    assert first["rule_id"] == second["rule_id"]
    assert first["ly_do"] == second["ly_do"]


def test_ly_do_khong_chua_gia_tri_input_dac_biet():
    patient = tao_benh_nhan_phan_ve()
    result = classify(patient)

    # Ly do duoc phep nhac ten rule va ten truong,
    # nhung khong duoc dua gia tri du lieu benh nhan vao.
    assert isinstance(result["ly_do"], str)
    assert "120" not in result["ly_do"]
    assert "25" not in result["ly_do"]
    assert "ten" not in result["ly_do"].lower()
