"""Rule Engine WAO/EAACI - khung bai tap BKT-1 (Track A), mon KTPMUD.

Sinh vien hien thuc ham classify() theo dac ta WAO/EAACI da co san trong
do_an_mon_hoc.md (Muc 2 va 4.1, xem https://fossbk-spec.github.io/ktpmud-book/do_an_mon_hoc).
KHONG tu dat nguong/quy tac moi chua duoc GV xac nhan.
"""
from __future__ import annotations

from typing import TypedDict


class PatientInput(TypedDict):
    """Input mau - cau truc that lay dung theo Data Dictionary cua de bai (se cap nhat khi cong bo de)."""
    uas7_score: int
    has_angioedema: bool
    duration_weeks: int


class ClassificationResult(TypedDict):
    risk_level: str  # vi du: "LOW" | "MEDIUM" | "HIGH" - dung dung nhan theo bang WAO/EAACI
    reason: str


def classify(patient: PatientInput) -> ClassificationResult:
    """Phan loai muc nguy co theo bang WAO/EAACI.

    TODO (sinh vien): hien thuc dung logic theo do_an_mon_hoc.md Muc 2/4.1.
    """
    raise NotImplementedError("Sinh vien hien thuc ham nay theo dac ta WAO/EAACI")
