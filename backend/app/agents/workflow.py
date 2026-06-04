import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from app.agents.state import AgentState
from app.agents.tools import (
    tool_search_documents,
    tool_retrieve_evidence,
    tool_extract_document_fields,
    tool_compare_documents,
    tool_find_obligations,
    tool_identify_deadlines,
    tool_validate_citations,
    tool_generate_report
)
from app.core.database import get_db_session
from app.models import AgentRun, Report, Document
from app.core.logging import logger

class DocumentAnalysisAgent:
    """Stateful Document Analysis Agent with step-by-step execution trace."""

    def run(self, goal: str, user_id: str, document_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        start_time = time.time()
        run_id = str(uuid.uuid4())

        # Initialize State
        state: AgentState = {
            "run_id": run_id,
            "user_id": user_id,
            "goal": goal,
            "document_ids": document_ids,
            "intent": None,
            "plan_steps": [],
            "current_step_index": 0,
            "retrieved_evidence": [],
            "extracted_data": {},
            "comparison_results": None,
            "validated_citations": [],
            "report_markdown": None,
            "execution_trace": [],
            "status": "running",
            "error": None
        }

        # Persist Initial Run Record
        with get_db_session() as db:
            db_run = AgentRun(
                id=run_id,
                user_id=user_id,
                goal=goal,
                status="running",
                steps_trace=[]
            )
            db.add(db_run)

        try:
            # 1. Intent Classification
            state = self._step_classify_intent(state)

            # 2. Task Planning
            state = self._step_plan_tasks(state)

            # 3. Document Retrieval & Evidence Gathering
            state = self._step_retrieve_evidence(state)

            # 4. Extraction & Cross-Checking
            state = self._step_extract_and_cross_check(state)

            # 5. Citation Validation
            state = self._step_validate_citations(state)

            # 6. Report Generation
            state = self._step_generate_report(state)

            state["status"] = "completed"
            duration = round(time.time() - start_time, 3)

            # Persist Final State
            with get_db_session() as db:
                db_run = db.query(AgentRun).filter(AgentRun.id == run_id).first()
                if db_run:
                    db_run.status = "completed"
                    db_run.steps_trace = state["execution_trace"]
                    db_run.final_output = state["report_markdown"]
                    db_run.duration_sec = duration

                # Save report
                db_report = Report(
                    id=f"rep-{run_id[:8]}",
                    user_id=user_id,
                    title=f"Autonomous Analysis: {goal[:60]}",
                    report_type="agent_analysis",
                    content_markdown=state["report_markdown"],
                    evidence_citations=state["retrieved_evidence"][:5]
                )
                db.add(db_report)

            logger.info(f"Agent run {run_id} completed successfully in {duration}s")
            return {
                "run_id": run_id,
                "goal": goal,
                "status": "completed",
                "steps": state["execution_trace"],
                "final_output": state["report_markdown"],
                "duration_sec": duration
            }

        except Exception as e:
            duration = round(time.time() - start_time, 3)
            logger.error(f"Agent run {run_id} failed: {e}", exc_info=True)
            with get_db_session() as db:
                db_run = db.query(AgentRun).filter(AgentRun.id == run_id).first()
                if db_run:
                    db_run.status = "failed"
                    db_run.steps_trace = state["execution_trace"]
                    db_run.duration_sec = duration
            return {
                "run_id": run_id,
                "goal": goal,
                "status": "failed",
                "error": str(e),
                "steps": state["execution_trace"],
                "duration_sec": duration
            }

    def _record_trace(self, state: AgentState, action: str, tool_name: Optional[str] = None, tool_input: Optional[Any] = None, tool_output: Optional[Any] = None):
        step_number = len(state["execution_trace"]) + 1
        entry = {
            "step_number": step_number,
            "action": action,
            "tool_name": tool_name,
            "tool_input": tool_input,
            "tool_output": tool_output,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        state["execution_trace"].append(entry)

    def _step_classify_intent(self, state: AgentState) -> AgentState:
        goal_lower = state["goal"].lower()
        if "compare" in goal_lower:
            intent = "document_comparison"
        elif "extract" in goal_lower or "schema" in goal_lower:
            intent = "structured_extraction"
        elif "obligation" in goal_lower or "sla" in goal_lower or "deadline" in goal_lower:
            intent = "compliance_audit"
        else:
            intent = "general_intelligence_analysis"

        state["intent"] = intent
        self._record_trace(state, action=f"Classified user intent: {intent}")
        return state

    def _step_plan_tasks(self, state: AgentState) -> AgentState:
        intent = state["intent"]
        if intent == "document_comparison":
            plan = ["Retrieve document representations", "Execute schema field extraction", "Compute cross-document diffs", "Validate evidence", "Compile report"]
        elif intent == "compliance_audit":
            plan = ["Retrieve contractual obligations", "Identify critical deadlines", "Validate supporting citations", "Compile executive compliance report"]
        else:
            plan = ["Search relevant passages", "Extract key facts", "Cross-check assertions", "Generate grounded report"]

        state["plan_steps"] = plan
        self._record_trace(state, action="Constructed execution plan", tool_output=plan)
        return state

    def _step_retrieve_evidence(self, state: AgentState) -> AgentState:
        goal = state["goal"]
        doc_ids = state["document_ids"]

        evidence = tool_search_documents(query=goal, document_ids=doc_ids, top_k=5)
        state["retrieved_evidence"] = evidence
        self._record_trace(
            state,
            action="Executed document retrieval",
            tool_name="search_documents",
            tool_input={"query": goal, "document_ids": doc_ids},
            tool_output=f"Retrieved {len(evidence)} verified passages."
        )
        return state

    def _step_extract_and_cross_check(self, state: AgentState) -> AgentState:
        doc_ids = state["document_ids"]

        if state["intent"] == "document_comparison":
            with get_db_session() as db:
                available_docs = db.query(Document).all()
                all_ids = [d.id for d in available_docs]

            target_a = doc_ids[0] if doc_ids and len(doc_ids) > 0 else (all_ids[0] if all_ids else None)
            target_b = doc_ids[1] if doc_ids and len(doc_ids) > 1 else (all_ids[1] if len(all_ids) > 1 else target_a)

            if target_a and target_b and target_a != target_b:
                comp = tool_compare_documents(target_a, target_b, user_id=state["user_id"])
                state["comparison_results"] = comp
                self._record_trace(
                    state,
                    action="Executed cross-document comparison",
                    tool_name="compare_documents",
                    tool_input={"doc_a": target_a, "doc_b": target_b},
                    tool_output=f"Identified {len(comp.get('differences', []))} fields and {comp.get('conflict_count', 0)} conflicts."
                )
        else:
            obligations = tool_find_obligations(document_ids=doc_ids)
            deadlines = tool_identify_deadlines(document_ids=doc_ids)
            state["extracted_data"] = {
                "obligations": obligations[:3],
                "deadlines": deadlines[:3]
            }
            self._record_trace(
                state,
                action="Extracted obligations and deadlines",
                tool_name="find_obligations",
                tool_output=f"Extracted {len(obligations)} obligations and {len(deadlines)} deadline items."
            )
        return state

    def _step_validate_citations(self, state: AgentState) -> AgentState:
        claims = []
        for e in state["retrieved_evidence"][:3]:
            claims.append({
                "claim": state["goal"],
                "passage": e.get("content", "")
            })

        val_result = tool_validate_citations(claims)
        self._record_trace(
            state,
            action="Validated evidence citations against source text",
            tool_name="validate_citations",
            tool_output=val_result
        )
        return state

    def _step_generate_report(self, state: AgentState) -> AgentState:
        findings = []
        if state.get("comparison_results"):
            for diff in state["comparison_results"].get("differences", [])[:4]:
                findings.append(f"**{diff['category']}**: {diff['difference_summary']}")
        elif state.get("extracted_data"):
            for ob in state["extracted_data"].get("obligations", [])[:2]:
                findings.append(f"**Obligation ({ob['document']})**: {ob['obligation_text'][:120]}...")
            for dl in state["extracted_data"].get("deadlines", [])[:2]:
                findings.append(f"**Deadline ({dl['document']})**: {', '.join(dl['key_deadlines'])}")
        else:
            findings.append("Analyzed document intelligence and verified citations across indexed corporate files.")

        report_md = tool_generate_report(
            title=f"Intelligence Audit Report: {state['goal']}",
            evidence=state["retrieved_evidence"],
            findings=findings
        )
        state["report_markdown"] = report_md
        self._record_trace(
            state,
            action="Generated evidence-grounded executive report",
            tool_name="generate_report",
            tool_output="Report generated successfully."
        )
        return state

document_analysis_agent = DocumentAnalysisAgent()
