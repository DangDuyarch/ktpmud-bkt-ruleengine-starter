"""Rule Engine WAO/EAACI - Track A: Dr May Day Rule Engine Sprint.

Thực hiện: Nguyễn Hoàng Sơn (Nhóm 26)
Reviewer: Duy (Spec), Quý (Coverage)
Quy chuẩn: REQUIREMENTS
"""
from __future__ import annotations

import datetime
import math
import os
import uuid
from typing import Optional, TypedDict


class PatientInput(TypedDict, total=False):
    """Input theo dung Data Dictionary trong REQUIREMENTS v1.1 (9 truong)."""
    tuoi: float
    huyet_ap_tam_thu: Optional[int]
    huyet_ap_tam_thu_nen: Optional[int]
    co_di_nguyen_nghi_ngo: bool
    di_nguyen_qua_duong_hit: bool
    co_ton_thuong_da_niem_mac: bool
    co_trieu_chung_ho_hap: bool
    co_trieu_chung_tuan_hoan: bool
    co_trieu_chung_tieu_hoa_nang: bool


class ClassificationResult(TypedDict):
    muc_do: str  # "SOC_PHAN_VE" | "PHAN_VE" | "THEO_DOI"
    rule_id: Optional[str]  # "R-SOC" | "R01-PV" | "R02-PV" | "R03-PV" | None
    ly_do: str


class AuditError(RuntimeError):
    """Ngoai le khi ghi audit trail bi loi he thong."""
    pass


ALLOWED_KEYS = {
    "tuoi",
    "huyet_ap_tam_thu",
    "huyet_ap_tam_thu_nen",
    "co_di_nguyen_nghi_ngo",
    "di_nguyen_qua_duong_hit",
    "co_ton_thuong_da_niem_mac",
    "co_trieu_chung_ho_hap",
    "co_trieu_chung_tuan_hoan",
    "co_trieu_chung_tieu_hoa_nang",
}


def _log_audit(status: str, user_uuid: Optional[str] = None) -> None:
    """Ghi audit 4 truong (Timestamp, User_UUID, Action_Type, Status) ra file audit.log."""
    log_dir = os.environ.get("AUDIT_LOG_DIR", ".audit_logs")
    log_file = os.path.join(log_dir, "audit.log")
    
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    uid = user_uuid or str(uuid.uuid4())
    log_entry = f"{timestamp} | {uid} | CLASSIFY | {status}\n"

    try:
        os.makedirs(log_dir, exist_ok=True)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        raise AuditError("Loi he thong khi ghi audit trail.") from e


def _validate_input(patient: PatientInput) -> None:
    """Validate nghiem ngac theo Muc 3.2 trong REQUIREMENTS v1.1."""
    if not isinstance(patient, dict):
        raise TypeError("Input phai la kieu dictionary.")

    # 1. Zero PII: Khoa ngoai allowlist -> ValueError
    extra_keys = set(patient.keys()) - ALLOWED_KEYS
    if extra_keys:
        raise ValueError("Input chua khoa ngoai danh sach dac ta.")

    # 2. Validate tuoi (float/int, >= 0, khong nhan bool)
    if "tuoi" in patient and patient["tuoi"] is not None:
        val = patient["tuoi"]
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            raise TypeError("Truong tuoi phai la so (int/float).")
        if math.isnan(val) or math.isinf(val) or val < 0:
            raise ValueError("Truong tuoi phai la so huu han >= 0.")

    # 3. Validate huyet_ap_tam_thu (int hoac None, >= 0, khong nhan bool/float/str)
    if "huyet_ap_tam_thu" in patient and patient["huyet_ap_tam_thu"] is not None:
        val = patient["huyet_ap_tam_thu"]
        if isinstance(val, bool) or not isinstance(val, int):
            raise TypeError("Truong huyet_ap_tam_thu phai la int hoac None.")
        if val < 0:
            raise ValueError("Truong huyet_ap_tam_thu phai >= 0.")

    # 4. Validate huyet_ap_tam_thu_nen (int hoac None, > 0, khong nhan bool/float/str)
    if "huyet_ap_tam_thu_nen" in patient and patient["huyet_ap_tam_thu_nen"] is not None:
        val = patient["huyet_ap_tam_thu_nen"]
        if isinstance(val, bool) or not isinstance(val, int):
            raise TypeError("Truong huyet_ap_tam_thu_nen phai la int hoac None.")
        if val <= 0:
            raise ValueError("Truong huyet_ap_tam_thu_nen phai > 0.")

    # 5. Validate 6 truong boolean (bool hoac None, khong nhan so 1/0 hay string)
    bool_keys = [
        "co_di_nguyen_nghi_ngo",
        "di_nguyen_qua_duong_hit",
        "co_ton_thuong_da_niem_mac",
        "co_trieu_chung_ho_hap",
        "co_trieu_chung_tuan_hoan",
        "co_trieu_chung_tieu_hoa_nang",
    ]
    for key in bool_keys:
        if key in patient and patient[key] is not None:
            val = patient[key]
            if not isinstance(val, bool):
                raise TypeError(f"Truong {key} phai la bool (True/False) hoac None.")


def _get_bool_state(patient: PatientInput, key: str) -> Optional[bool]:
    """Lay gia tri boolean: True, False, hoac None (UNKNOWN)."""
    val = patient.get(key)
    return val if isinstance(val, bool) else None


def _eval_r01(patient: PatientInput) -> Optional[bool]:
    """R01-PV = (co_di_nguyen_nghi_ngo == False) AND da_niem_mac AND (ho_hap OR tuan_hoan)"""
    di_nguyen = _get_bool_state(patient, "co_di_nguyen_nghi_ngo")
    da_niem_mac = _get_bool_state(patient, "co_ton_thuong_da_niem_mac")
    ho_hap = _get_bool_state(patient, "co_trieu_chung_ho_hap")
    tuan_hoan = _get_bool_state(patient, "co_trieu_chung_tuan_hoan")

    if di_nguyen is True:
        return False
    
    if ho_hap is True or tuan_hoan is True:
        or_res: Optional[bool] = True
    elif ho_hap is False and tuan_hoan is False:
        or_res = False
    else:
        or_res = None

    conds = [di_nguyen is False, da_niem_mac, or_res]
    if False in conds:
        return False
    if None in conds:
        return None
    return True


def _eval_r02(patient: PatientInput) -> Optional[bool]:
    """R02-PV = co_di_nguyen_nghi_ngo AND (it nhat 2/4 he co quan True)"""
    di_nguyen = _get_bool_state(patient, "co_di_nguyen_nghi_ngo")
    if di_nguyen is False:
        return False

    systems = [
        _get_bool_state(patient, "co_ton_thuong_da_niem_mac"),
        _get_bool_state(patient, "co_trieu_chung_ho_hap"),
        _get_bool_state(patient, "co_trieu_chung_tuan_hoan"),
        _get_bool_state(patient, "co_trieu_chung_tieu_hoa_nang"),
    ]
    t_count = sum(1 for s in systems if s is True)
    u_count = sum(1 for s in systems if s is None)

    if t_count >= 2:
        sys_res: Optional[bool] = True
    elif t_count + u_count < 2:
        sys_res = False
    else:
        sys_res = None

    if di_nguyen is False or sys_res is False:
        return False
    if di_nguyen is None or sys_res is None:
        return None
    return True


def _eval_r03(patient: PatientInput) -> Optional[bool]:
    """R03-PV = co_di_nguyen_nghi_ngo AND (((NOT duong_hit) AND ho_hap) OR tuan_hoan)"""
    di_nguyen = _get_bool_state(patient, "co_di_nguyen_nghi_ngo")
    if di_nguyen is False:
        return False

    duong_hit = _get_bool_state(patient, "di_nguyen_qua_duong_hit")
    ho_hap = _get_bool_state(patient, "co_trieu_chung_ho_hap")
    tuan_hoan = _get_bool_state(patient, "co_trieu_chung_tuan_hoan")

    not_hit = (not duong_hit) if duong_hit is not None else None
    if not_hit is False or ho_hap is False:
        sub_and: Optional[bool] = False
    elif not_hit is True and ho_hap is True:
        sub_and = True
    else:
        sub_and = None

    if sub_and is True or tuan_hoan is True:
        sub_or: Optional[bool] = True
    elif sub_and is False and tuan_hoan is False:
        sub_or = False
    else:
        sub_or = None

    if di_nguyen is False or sub_or is False:
        return False
    if di_nguyen is None or sub_or is None:
        return None
    return True


def _eval_soc(patient: PatientInput) -> Optional[bool]:
    """Tầng 1 (R-SOC): Kiểm tra tiêu chí tụt huyết áp theo tuổi."""
    tuoi = patient.get("tuoi")
    if tuoi is None or tuoi < 0:
        return None

    hatt = patient.get("huyet_ap_tam_thu")
    if hatt is None:
        return None

    if 0 <= tuoi < 1:
        return hatt < 70
    elif 1 <= tuoi < 11:
        return hatt < (70 + 2 * tuoi)
    elif 11 <= tuoi < 18:
        return hatt < 90
    else:  # tuoi >= 18
        if hatt < 90:
            return True
        hatt_nen = patient.get("huyet_ap_tam_thu_nen")
        if hatt_nen is not None and hatt_nen > 0:
            # 10 * HATT < 7 * HATT_nền tương đương giảm > 30% so với nền
            return (10 * hatt) < (7 * hatt_nen)
        return None


def classify(patient: PatientInput) -> ClassificationResult:
    """Phân loại phản vệ theo đúng REQUIREMENTS v1.1."""
    # 1. Validate Toàn bộ input trước. Nếu lỗi -> ghi audit INVALID_INPUT rồi raise TypeError/ValueError.
    try:
        _validate_input(patient)
    except (TypeError, ValueError) as err:
        try:
            _log_audit(status="INVALID_INPUT")
        except AuditError:
            pass
        raise err

    # 2. Thiếu/null tuoi -> THEO_DOI (Ghi audit SUCCESS)
    tuoi = patient.get("tuoi")
    if tuoi is None:
        _log_audit(status="SUCCESS")
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": "Thieu thong tin tuoi (tuoi), khong du du kien de phan loai.",
        }

    # 3. Đánh giá Tầng 2 theo thứ tự ưu tiên R01 > R02 > R03
    r01_state = _eval_r01(patient)
    r02_state = _eval_r02(patient)
    r03_state = _eval_r03(patient)

    matched_rule: Optional[str] = None
    if r01_state is True:
        matched_rule = "R01-PV"
    elif r02_state is True:
        matched_rule = "R02-PV"
    elif r03_state is True:
        matched_rule = "R03-PV"

    # 4. Nếu không có rule Tầng 2 nào TRUE -> THEO_DOI
    if matched_rule is None:
        _log_audit(status="SUCCESS")
        is_any_unknown = None in (r01_state, r02_state, r03_state)
        reason = (
            "Chua du du kien de phan loai phan ve."
            if is_any_unknown
            else "Khong khop voi bat ky kich ban phan ve nao (R01, R02, R03)."
        )
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": reason,
        }

    # 5. Kiểm tra Tầng 1 (Sốc phản vệ)
    soc_state = _eval_soc(patient)
    _log_audit(status="SUCCESS")

    if soc_state is True:
        return {
            "muc_do": "SOC_PHAN_VE",
            "rule_id": "R-SOC",
            "ly_do": f"Khop {matched_rule} va co bieu hien tut huyet ap tam thu theo lua tuoi.",
        }

    reason_pv = (
        f"Khop {matched_rule}, chua xac nhan duoc soc (huyet ap khong tut hoac thieu du lieu)."
        if soc_state is None
        else f"Khop {matched_rule}."
    )
    return {
        "muc_do": "PHAN_VE",
        "rule_id": matched_rule,
        "ly_do": reason_pv,
    }