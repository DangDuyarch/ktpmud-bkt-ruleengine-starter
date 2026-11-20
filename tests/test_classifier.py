"""Bộ Unit Test hoàn chỉnh đáp ứng AC_TRACEABILITY (A-01..A-08) và SECURITY_CHECKLIST (SEC-02..SEC-11)."""

import datetime
import os
import sys
import uuid
from pathlib import Path

# Đảm bảo pytest (kể cả trên CI Linux) luôn tìm thấy thư mục gốc chứa rule_engine
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pytest
from rule_engine.classifier import AuditError, classify


# --- 1. MA TRẬN TÌNH HUỐNG LÂM SÀNG (A-01, A-03, A-04, A-05) ---

def test_tc01_r01_pv():
    patient = {
        "tuoi": 30.0,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 120,
    }
    res = classify(patient)
    assert set(res.keys()) == {"muc_do", "rule_id", "ly_do"}
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
    with pytest.raises(TypeError):
        classify({"tuoi": None, "co_di_nguyen_nghi_ngo": "true"})


# --- 2. TEST VALIDATION LỖI (TYPEERROR & VALUEERROR - SEC-02, SEC-03) ---

def test_invalid_type_age_str():
    with pytest.raises(TypeError):
        classify({"tuoi": "30"})


def test_invalid_type_bool_int():
    # Bool nhận số 1 -> TypeError
    with pytest.raises(TypeError):
        classify({"tuoi": 20.0, "co_di_nguyen_nghi_ngo": 1})


def test_invalid_value_extra_key_pii():
    with pytest.raises(ValueError) as exc_info:
        classify({"tuoi": 30, "ten_benh_nhan": "Nguyen Van A"})
    # SEC-08/SEC-10: Message lỗi không lộ giá trị input
    assert "Nguyen Van A" not in str(exc_info.value)


def test_invalid_value_negative_bp():
    with pytest.raises(ValueError):
        classify({"tuoi": 30, "huyet_ap_tam_thu": -10})


# --- 3. TEST AUDIT TRAIL & FAIL-CLOSED SECURITY (A-06, SEC-05..SEC-11) ---

def test_audit_success_4_fields_and_no_pii(tmp_path, monkeypatch):
    """SEC-05, SEC-06, SEC-07: Kiểm tra log SUCCESS đủ 4 trường, chuẩn UTC ISO, không lộ raw input."""
    audit_dir = tmp_path / "isolated_audit"
    monkeypatch.setenv("AUDIT_LOG_DIR", str(audit_dir))

    patient = {
        "tuoi": 42.5,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 115,
    }
    res = classify(patient)
    assert res["muc_do"] == "PHAN_VE"

    log_file = audit_dir / "audit.log"
    assert log_file.exists()
    lines = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1

    parts = [p.strip() for p in lines[0].split("|")]
    assert len(parts) == 4

    ts_str, uid_str, action, status = parts
    # Kiểm tra ISO 8601 UTC
    dt = datetime.datetime.fromisoformat(ts_str)
    assert dt.tzinfo is not None
    # Kiểm tra UUID hợp lệ
    assert uuid.UUID(uid_str)
    assert action == "CLASSIFY"
    assert status == "SUCCESS"
    # Kiểm tra không lọt dữ liệu lâm sàng thô
    assert "42.5" not in lines[0]
    assert "115" not in lines[0]


def test_audit_invalid_input_logs_before_raise(tmp_path, monkeypatch):
    """SEC-08: Input không hợp lệ ghi INVALID_INPUT vào audit rồi mới phát sinh TypeError/ValueError."""
    audit_dir = tmp_path / "isolated_audit"
    monkeypatch.setenv("AUDIT_LOG_DIR", str(audit_dir))

    with pytest.raises(ValueError):
        classify({"tuoi": 25, "cccd": "001204009999"})

    log_file = audit_dir / "audit.log"
    assert log_file.exists()
    lines = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert "CLASSIFY | INVALID_INPUT" in lines[0]
    assert "001204009999" not in lines[0]


def test_audit_fail_closed_raises_audit_error_with_cause(tmp_path, monkeypatch):
    """SEC-09: Khi audit lỗi I/O -> raise AuditError kế thừa RuntimeError, giữ __cause__, không trả kết quả."""
    blocked_path = tmp_path / "blocked_file"
    blocked_path.write_text("not a directory", encoding="utf-8")
    monkeypatch.setenv("AUDIT_LOG_DIR", str(blocked_path))

    patient = {
        "tuoi": 30.0,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 120,
    }
    with pytest.raises(AuditError) as exc_info:
        classify(patient)

    assert isinstance(exc_info.value, RuntimeError)
    assert exc_info.value.__cause__ is not None


def test_audit_error_takes_precedence_over_validation_error(tmp_path, monkeypatch):
    """SEC-10: Lỗi kép (input sai + audit lỗi I/O) -> AuditError phải được ưu tiên hơn TypeError/ValueError."""
    blocked_path = tmp_path / "blocked_file"
    blocked_path.write_text("not a directory", encoding="utf-8")
    monkeypatch.setenv("AUDIT_LOG_DIR", str(blocked_path))

    with pytest.raises(AuditError) as exc_info:
        classify({"tuoi": "invalid_str_age"})

    assert "invalid_str_age" not in str(exc_info.value)


def test_default_audit_dir_is_outside_repo(monkeypatch):
    """SEC-11: Đảm bảo thư mục audit mặc định không nằm trong thư mục làm việc của repository."""
    monkeypatch.delenv("AUDIT_LOG_DIR", raising=False)
    from rule_engine.classifier import _get_default_audit_dir

    repo_root = os.path.abspath(os.getcwd())
    default_dir = os.path.abspath(_get_default_audit_dir())
try:
        is_inside = os.path.commonpath([repo_root, default_dir]) == repo_root
    except ValueError:
        is_inside = False
    assert not is_inside
