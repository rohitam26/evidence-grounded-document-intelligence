import json
import os

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "evaluation", "datasets", "evaluation_dataset.json")

def generate_52_eval_cases():
    cases = []
    
    # --- Category 1: Acme Service Agreement (14 questions) ---
    acme_questions = [
        ("What are the payment terms under the Acme contract?", "Net 30 days from invoice issuance date", "acme_service_agreement.pdf", 1, "All invoices are payable under Net 30 days"),
        ("What is the monthly fixed subscription rate for Acme?", "$15,000.00", "acme_service_agreement.pdf", 1, "compensate Provider at a fixed monthly subscription rate of $15,000.00"),
        ("What is the late payment finance charge under Acme Agreement?", "1.5% per month", "acme_service_agreement.pdf", 1, "Late payments shall incur a monthly finance charge of 1.5%"),
        ("What is the effective date of the Acme Agreement?", "January 10, 2026", "acme_service_agreement.pdf", 1, "entered into as of January 10, 2026"),
        ("Who is the Provider in the Acme Agreement?", "Beta Global Solutions", "acme_service_agreement.pdf", 1, "Beta Global Solutions ('Provider')"),
        ("Who is the Client in the Acme Agreement?", "Acme Corporation", "acme_service_agreement.pdf", 1, "Acme Corporation ('Client')"),
        ("What services will Provider deliver to Acme?", "Cloud data analytics and automated document classification", "acme_service_agreement.pdf", 1, "deliver cloud data analytics and automated document classification"),
        ("How long do confidentiality obligations survive under Acme contract?", "Three (3) years", "acme_service_agreement.pdf", 1, "survive termination for a period of three (3) years"),
        ("What is the initial duration or term of the Acme Agreement?", "12 months", "acme_service_agreement.pdf", 2, "remain active for twelve (12) months"),
        ("What is the notice period required for termination without cause in Acme contract?", "30 days prior written notice", "acme_service_agreement.pdf", 2, "providing thirty (30) days prior written notice"),
        ("Within how many days must Provider delete client data upon termination of Acme agreement?", "45 days", "acme_service_agreement.pdf", 2, "delete client data within forty-five (45) days"),
        ("Which governing law applies to the Acme Agreement?", "State of Delaware", "acme_service_agreement.pdf", 2, "governed by and construed in accordance with the laws of the State of Delaware"),
        ("In which county will Acme disputes be settled?", "New Castle County, Delaware", "acme_service_agreement.pdf", 2, "settled in New Castle County, Delaware"),
        ("Who signed the Acme Agreement on behalf of Acme Corporation?", "John H. Smith, Chief Executive Officer", "acme_service_agreement.pdf", 2, "For Acme Corporation: John H. Smith, Chief Executive Officer"),
    ]
    for q, ans, doc, page, ev in acme_questions:
        cases.append({
            "id": f"eval-{len(cases)+1:03d}",
            "question": q,
            "expected_answer": ans,
            "expected_document": doc,
            "expected_page": page,
            "expected_evidence": ev,
            "is_unanswerable": False
        })

    # --- Category 2: Beta Master Agreement (14 questions) ---
    beta_questions = [
        ("What are the payment terms in the Beta Master Agreement?", "Net 60 days strictly from invoice date", "beta_master_agreement.pdf", 1, "payable strictly under Net 60 days from invoice date"),
        ("What is the total contract value of the Beta Vendor Agreement?", "$180,000.00", "beta_master_agreement.pdf", 1, "total contract value of $180,000.00"),
        ("How are payments tranches structured in the Beta agreement?", "Quarterly tranches of $45,000.00", "beta_master_agreement.pdf", 1, "payable in quarterly tranches of $45,000.00"),
        ("Do late penalties or interest charges apply under the Beta Agreement?", "No interest charges or late penalties shall apply", "beta_master_agreement.pdf", 1, "No interest charges or late penalties shall apply"),
        ("What is the effective date of the Beta Master Agreement?", "February 1, 2026", "beta_master_agreement.pdf", 1, "effective as of February 1, 2026"),
        ("Who is the Contractor in the Beta Agreement?", "Gamma Enterprises LLC", "beta_master_agreement.pdf", 1, "Gamma Enterprises LLC ('Contractor')"),
        ("What services will Contractor deliver to Beta Global Solutions?", "Multi-lingual technical support, documentation auditing, and security patch verification", "beta_master_agreement.pdf", 1, "technical support, documentation auditing, and security patch verification"),
        ("How many business days written request is required for compliance audit logs in Beta Agreement?", "10 business days", "beta_master_agreement.pdf", 1, "upon ten (10) business days written request"),
        ("What is the initial term duration of the Beta Agreement?", "24 months", "beta_master_agreement.pdf", 2, "initial term of this Agreement is twenty-four (24) months"),
        ("What is the termination notice period for convenience in Beta agreement?", "60 days advance written notice", "beta_master_agreement.pdf", 2, "upon sixty (60) days advance written notice"),
        ("What is the cure period for material breach under the Beta Agreement?", "15 days", "beta_master_agreement.pdf", 2, "remedied within fifteen (15) days"),
        ("Which governing jurisdiction applies to the Beta Master Agreement?", "State of California", "beta_master_agreement.pdf", 2, "governed by the laws of the State of California"),
        ("Where must formal arbitration take place for Beta Agreement disputes?", "San Francisco, California", "beta_master_agreement.pdf", 2, "exclusively in San Francisco, California"),
        ("Who signed for Gamma Enterprises LLC in the Beta Agreement?", "David K. Reynolds, Managing Director", "beta_master_agreement.pdf", 2, "Gamma Enterprises LLC: David K. Reynolds, Managing Director"),
    ]
    for q, ans, doc, page, ev in beta_questions:
        cases.append({
            "id": f"eval-{len(cases)+1:03d}",
            "question": q,
            "expected_answer": ans,
            "expected_document": doc,
            "expected_page": page,
            "expected_evidence": ev,
            "is_unanswerable": False
        })

    # --- Category 3: Acme Invoice 1042 (8 questions) ---
    invoice_questions = [
        ("What is the invoice number on the Acme commercial invoice?", "ACME-2026-1042", "acme_invoice_1042.pdf", 1, "Invoice Number: ACME-2026-1042"),
        ("What is the invoice issuance date for invoice 1042?", "January 15, 2026", "acme_invoice_1042.pdf", 1, "Invoice Date: January 15, 2026"),
        ("When is the payment due date for invoice ACME-2026-1042?", "February 14, 2026", "acme_invoice_1042.pdf", 1, "Payment Due Date: February 14, 2026"),
        ("What is the total amount due on invoice 1042?", "$48,600.00", "acme_invoice_1042.pdf", 1, "Total Amount Due: $48,600.00"),
        ("What is the subtotal on invoice 1042 before taxes?", "$45,000.00", "acme_invoice_1042.pdf", 1, "Subtotal: $45,000.00"),
        ("What is the applicable state tax amount on invoice 1042?", "$3,600.00", "acme_invoice_1042.pdf", 1, "Applicable State Tax (8%): $3,600.00"),
        ("What are the payment terms specified on invoice 1042?", "Net 30 days", "acme_invoice_1042.pdf", 1, "Payment Terms: Net 30 days"),
        ("What routing number is specified for wire remittance on invoice 1042?", "#031100209", "acme_invoice_1042.pdf", 1, "Routing #031100209"),
    ]
    for q, ans, doc, page, ev in invoice_questions:
        cases.append({
            "id": f"eval-{len(cases)+1:03d}",
            "question": q,
            "expected_answer": ans,
            "expected_document": doc,
            "expected_page": page,
            "expected_evidence": ev,
            "is_unanswerable": False
        })

    # --- Category 4: Gamma Contract Amendment (6 questions) ---
    gamma_questions = [
        ("What is the execution date of Amendment No. 1 to the Services Contract?", "March 1, 2026", "gamma_contract_amendment.docx", 1, "executed on March 1, 2026"),
        ("How does the contract term renew under Amendment No. 1?", "Automatically renews for consecutive 12-month periods", "gamma_contract_amendment.docx", 1, "automatically renew for additional consecutive 12-month periods"),
        ("What notice period is required for non-renewal under Amendment No. 1?", "90 days prior to expiration", "gamma_contract_amendment.docx", 1, "at least ninety (90) days prior to the expiration date"),
        ("What is the guaranteed system uptime SLA under Amendment No. 1?", "99.9% uptime", "gamma_contract_amendment.docx", 1, "guarantees 99.9% system uptime"),
        ("What credit is Client entitled to if unplanned downtime exceeds 4 hours?", "10% credit against monthly fees", "gamma_contract_amendment.docx", 1, "entitle Client to a 10% credit against monthly fees"),
        ("Which parties executed Amendment No. 1?", "Beta Global Solutions and Gamma Enterprises LLC", "gamma_contract_amendment.docx", 1, "between Beta Global Solutions and Gamma Enterprises LLC"),
    ]
    for q, ans, doc, page, ev in gamma_questions:
        cases.append({
            "id": f"eval-{len(cases)+1:03d}",
            "question": q,
            "expected_answer": ans,
            "expected_document": doc,
            "expected_page": page,
            "expected_evidence": ev,
            "is_unanswerable": False
        })

    # --- Category 5: Intentionally Unanswerable / Hallucination-Trap Questions (10 questions) ---
    unanswerable = [
        "What is the penalty for using quantum computing decryption in the Acme contract?",
        "What is the personal home address of Sarah Jenkins in the Beta Agreement?",
        "What are the secret extraterrestrial space mining rights mentioned in the invoice?",
        "What is the discount rate for payments made in Bitcoin in the Acme agreement?",
        "What is the annual software escrow deposit fee charged by Gamma Enterprises?",
        "What are the carbon offset emissions credits agreed between Acme and Beta?",
        "What is the interest penalty for early termination of the Gamma amendment?",
        "What is the company car allowance provided to John Smith in the Acme agreement?",
        "What is the London arbitration court address specified for Beta Global Solutions?",
        "What is the insurance policy deductible for drone delivery in the commercial invoice?"
    ]
    for q in unanswerable:
        cases.append({
            "id": f"eval-{len(cases)+1:03d}",
            "question": q,
            "expected_answer": "ABSTAIN",
            "expected_document": "None",
            "expected_page": 0,
            "expected_evidence": "None (Intentionally unanswerable prompt)",
            "is_unanswerable": True
        })

    with open(DATASET_PATH, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2)

    print(f"Generated {len(cases)} verified evaluation cases at: {DATASET_PATH}")

if __name__ == "__main__":
    generate_52_eval_cases()
