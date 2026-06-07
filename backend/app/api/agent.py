from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from app.api.auth import require_auth
from app.schemas.agent import AgentRunRequest
from app.agents.workflow import document_analysis_agent
from app.core.database import get_db_session
from app.models import AgentRun

agent_bp = Blueprint("agent", __name__)

@agent_bp.route("/run", methods=["POST"])
@require_auth
def run_agent():
    try:
        body = AgentRunRequest(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422

    res = document_analysis_agent.run(
        goal=body.goal,
        user_id=g.user_id,
        document_ids=body.document_ids
    )
    return jsonify(res)

@agent_bp.route("/runs/<run_id>", methods=["GET"])
@require_auth
def get_agent_run(run_id: str):
    with get_db_session() as db:
        run = db.query(AgentRun).filter(AgentRun.id == run_id).first()
        if not run:
            return jsonify({"error": "Agent run not found"}), 404
        return jsonify({
            "run_id": run.id,
            "goal": run.goal,
            "status": run.status,
            "steps": run.steps_trace,
            "final_output": run.final_output,
            "duration_sec": run.duration_sec,
            "created_at": run.created_at.isoformat() if run.created_at else None
        })
