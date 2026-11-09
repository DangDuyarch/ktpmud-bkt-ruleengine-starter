"""Rule Engine WAO/EAACI - bài tập BKT-1 (Track A), môn KTPMUD.

Người thực hiện: Nguyễn Hoàng Sơn
Reviewer: Duy (Spec), Quý (Coverage)
"""
from __future__ import annotations

from typing import Optional, TypedDict


class PatientInput(TypedDict, total=False):
    """Input theo dung Data Dictionary trong docs/decision-table.md."""
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


def _check_r01(patient: PatientInput) -> bool:
    """R01 — Không rõ dị nguyên."""
    if patient.get("co_di_nguyen_nghi_ngo", False):
        return False
    da_niem_mac = bool(patient.get("co_ton_thuong_da_niem_mac", False))
    ho_hap = bool(patient.get("co_trieu_chung_ho_hap", False))
    tuan_hoan = bool(patient.get("co_trieu_chung_tuan_hoan", False))

    return da_niem_mac and (ho_hap or tuan_hoan)


def _check_r02(patient: PatientInput) -> bool:
    """R02 — Dị nguyên nghi ngờ, >=2/4 hệ cơ quan."""
    if not patient.get("co_di_nguyen_nghi_ngo", False):
        return False
    
    systems = [
        bool(patient.get("co_ton_thuong_da_niem_mac", False)),
        bool(patient.get("co_trieu_chung_ho_hap", False)),
        bool(patient.get("co_trieu_chung_tuan_hoan", False)),
        bool(patient.get("co_trieu_chung_tieu_hoa_nang", False)),
    ]
    return sum(systems) >= 2


def _check_r03(patient: PatientInput) -> bool:
    """R03 — Dị nguyên đã biết."""
    if not patient.get("co_di_nguyen_nghi_ngo", False):
        return False

    duong_hit = bool(patient.get("di_nguyen_qua_duong_hit", False))
    ho_hap = bool(patient.get("co_trieu_chung_ho_hap", False))
    tuan_hoan = bool(patient.get("co_trieu_chung_tuan_hoan", False))

    return ((not duong_hit) and ho_hap) or tuan_hoan


def _is_soc(patient: PatientInput) -> bool:
    """Tầng 1: Kiểm tra tiêu chí tụt huyết áp theo tuổi."""
    tuoi = patient.get("tuoi")
    if tuoi is None or tuoi < 0:
        return False

    hatt = patient.get("huyet_ap_tam_thu")
    if hatt is None:
        return False

    # Ngưỡng tụt huyết áp theo nhóm tuổi
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
            # Điều kiện: giảm > 30% so với HATT nền (strict > 30%)
            return (hatt_nen - hatt) / hatt_nen > 0.30
        return False


def classify(patient: PatientInput) -> ClassificationResult:
    """Phân loại mức độ phản vệ theo bảng quyết định WAO/EAACI."""
    # SỬA LỖI 1: Theo đặc tả, thiếu tuoi -> THEO_DOI ngay lập tức
    tuoi = patient.get("tuoi")
    if tuoi is None or tuoi < 0:
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": "Thieu thong tin tuoi hop le cua benh nhan.",
        }

    # 1. Kiểm tra Tầng 2 (Các kịch bản Phản vệ) theo thứ tự ưu tiên R01 -> R02 -> R03
    matched_rule: Optional[str] = None
    if _check_r01(patient):
        matched_rule = "R01-PV"
    elif _check_r02(patient):
        matched_rule = "R02-PV"
    elif _check_r03(patient):
        matched_rule = "R03-PV"

    # Nếu không khớp kịch bản nào ở Tầng 2 -> THEO_DOI
    if matched_rule is None:
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": "Chua du dieu kien phan loai phan ve.",
        }

    # 2. Kiểm tra Tầng 1 (Sốc phản vệ) khi đã khớp Tầng 2
    if _is_soc(patient):
        return {
            "muc_do": "SOC_PHAN_VE",
            "rule_id": "R-SOC",
            "ly_do": "Dap ung tieu chi phan loai soc phan ve.",
        }

    # 3. Trả về mức độ Phản vệ
    return {
        "muc_do": "PHAN_VE",
        "rule_id": matched_rule,
        "ly_do": f"Dap ung tieu chi phan ve theo rule {matched_rule}.",
    }