from flask import Blueprint, jsonify
from app.api.auth import require_auth
from app.core.database import get_db_session
from app.models import Report

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("", methods=["GET"])
@require_auth
def list_reports():
    with get_db_session() as db:
        reports = db.query(Report).order_by(Report.created_at.desc()).all()
        return jsonify([
            {
                "id": r.id,
                "title": r.title,
                "report_type": r.report_type,
                "content_markdown": r.content_markdown,
                "evidence_citations": r.evidence_citations,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in reports
        ])

@reports_bp.route("/<report_id>", methods=["GET"])
@require_auth
def get_report(report_id: str):
    with get_db_session() as db:
        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            return jsonify({"error": "Report not found"}), 404
        return jsonify({
            "id": report.id,
            "title": report.title,
            "report_type": report.report_type,
            "content_markdown": report.content_markdown,
            "evidence_citations": report.evidence_citations,
            "created_at": report.created_at.isoformat() if report.created_at else None
        })
