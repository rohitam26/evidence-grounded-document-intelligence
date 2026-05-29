import os
import pymupdf
import docx

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "sample_documents")
os.makedirs(SAMPLE_DIR, exist_ok=True)

def create_acme_service_agreement():
    path = os.path.join(SAMPLE_DIR, "acme_service_agreement.pdf")
    doc = pymupdf.open()

    # Page 1
    p1 = doc.new_page()
    text_p1 = (
        "MASTER SERVICES AGREEMENT\n\n"
        "This Master Services Agreement ('Agreement') is entered into as of January 10, 2026 ('Effective Date'), "
        "by and between Acme Corporation ('Client'), a Delaware corporation, and Beta Global Solutions ('Provider'), "
        "a California corporation.\n\n"
        "SECTION 1: SCOPE OF SERVICES\n"
        "Provider shall deliver cloud data analytics and automated document classification software as detailed in Exhibit A.\n\n"
        "SECTION 2: FEES AND PAYMENT TERMS\n"
        "Client shall compensate Provider at a fixed monthly subscription rate of $15,000.00. "
        "All invoices are payable under Net 30 days from invoice issuance date. "
        "Late payments shall incur a monthly finance charge of 1.5% or the maximum permitted by law.\n\n"
        "SECTION 3: CONFIDENTIALITY AND SECURITY\n"
        "Both parties agree to protect proprietary data using standard industry encryption and access controls. "
        "Confidentiality obligations survive termination for a period of three (3) years."
    )
    p1.insert_textbox(pymupdf.Rect(50, 50, 550, 750), text_p1, fontsize=11)

    # Page 2
    p2 = doc.new_page()
    text_p2 = (
        "SECTION 4: TERM AND TERMINATION\n"
        "This Agreement shall commence on the Effective Date and remain active for twelve (12) months. "
        "Either party may terminate this Agreement without cause by providing thirty (30) days prior written notice. "
        "Upon termination, Provider shall deliver all deliverables and delete client data within forty-five (45) days.\n\n"
        "SECTION 5: GOVERNING LAW AND DISPUTE RESOLUTION\n"
        "This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, "
        "excluding its conflict of law principles. Any dispute shall be settled in New Castle County, Delaware.\n\n"
        "SECTION 6: SIGNATURES\n"
        "For Acme Corporation: John H. Smith, Chief Executive Officer\n"
        "For Beta Global Solutions: Sarah Jenkins, Chief Operating Officer\n"
        "Date of Signature: January 10, 2026"
    )
    p2.insert_textbox(pymupdf.Rect(50, 50, 550, 750), text_p2, fontsize=11)

    doc.save(path)
    doc.close()
    print(f"Created: {path}")

def create_beta_master_agreement():
    path = os.path.join(SAMPLE_DIR, "beta_master_agreement.pdf")
    doc = pymupdf.open()

    # Page 1
    p1 = doc.new_page()
    text_p1 = (
        "VENDOR SERVICES MASTER AGREEMENT\n\n"
        "This Vendor Services Master Agreement ('Agreement') is made effective as of February 1, 2026, "
        "by and between Beta Global Solutions ('Client') and Gamma Enterprises LLC ('Contractor').\n\n"
        "ARTICLE 1: SERVICES DELIVERABLE\n"
        "Contractor will provide multi-lingual technical support, documentation auditing, and security patch verification.\n\n"
        "ARTICLE 2: FINANCIAL PROVISIONS AND PAYMENT TERMS\n"
        "Client shall pay Contractor total contract value of $180,000.00 payable in quarterly tranches of $45,000.00. "
        "All undisputed invoice amounts are payable strictly under Net 60 days from invoice date. "
        "No interest charges or late penalties shall apply.\n\n"
        "ARTICLE 3: AUDIT RIGHTS\n"
        "Client retains the right to inspect Contractor compliance logs upon ten (10) business days written request."
    )
    p1.insert_textbox(pymupdf.Rect(50, 50, 550, 750), text_p1, fontsize=11)

    # Page 2
    p2 = doc.new_page()
    text_p2 = (
        "ARTICLE 4: TERMINATION PROTOCOL\n"
        "The initial term of this Agreement is twenty-four (24) months. "
        "Either party may terminate for convenience upon sixty (60) days advance written notice. "
        "Immediate termination is permitted solely in cases of material breach unremedied within fifteen (15) days.\n\n"
        "ARTICLE 5: GOVERNING JURISDICTION\n"
        "This Agreement is governed by the laws of the State of California. "
        "Any formal arbitration or litigation shall take place exclusively in San Francisco, California.\n\n"
        "IN WITNESS WHEREOF:\n"
        "Beta Global Solutions: Sarah Jenkins, COO\n"
        "Gamma Enterprises LLC: David K. Reynolds, Managing Director\n"
        "Execution Date: February 1, 2026"
    )
    p2.insert_textbox(pymupdf.Rect(50, 50, 550, 750), text_p2, fontsize=11)

    doc.save(path)
    doc.close()
    print(f"Created: {path}")

def create_acme_invoice():
    path = os.path.join(SAMPLE_DIR, "acme_invoice_1042.pdf")
    doc = pymupdf.open()
    p1 = doc.new_page()

    text = (
        "COMMERCIAL INVOICE\n\n"
        "Vendor: Acme Corporation\n"
        "Address: 100 Enterprise Way, Suite 400, Wilmington, DE 19801\n"
        "Customer: Beta Global Solutions\n"
        "Address: 500 Technology Boulevard, San Jose, CA 95110\n\n"
        "Invoice Number: ACME-2026-1042\n"
        "Invoice Date: January 15, 2026\n"
        "Payment Due Date: February 14, 2026\n"
        "Payment Terms: Net 30 days\n\n"
        "Item Description | Quantity | Unit Price | Total\n"
        "Enterprise Document Intelligence License Q1 | 1 | $35,000.00 | $35,000.00\n"
        "System Architecture Onboarding Workshop | 1 | $10,000.00 | $10,000.00\n\n"
        "Subtotal: $45,000.00\n"
        "Applicable State Tax (8%): $3,600.00\n"
        "Total Amount Due: $48,600.00\n\n"
        "Remittance: Wire transfer to Delaware Commercial Bank, Routing #031100209"
    )
    p1.insert_textbox(pymupdf.Rect(50, 50, 550, 750), text, fontsize=11)
    doc.save(path)
    doc.close()
    print(f"Created: {path}")

def create_gamma_docx():
    path = os.path.join(SAMPLE_DIR, "gamma_contract_amendment.docx")
    doc = docx.Document()
    doc.add_heading("AMENDMENT NO. 1 TO SERVICES CONTRACT", level=1)
    doc.add_paragraph(
        "This Amendment No. 1 is executed on March 1, 2026, by and between Beta Global Solutions and Gamma Enterprises LLC."
    )
    doc.add_heading("RENEWAL CLAUSE", level=2)
    doc.add_paragraph(
        "The contract term shall automatically renew for additional consecutive 12-month periods unless either party "
        "provides written notice of non-renewal at least ninety (90) days prior to the expiration date."
    )
    doc.add_heading("SERVICE LEVEL OBLIGATIONS", level=2)
    doc.add_paragraph(
        "Provider guarantees 99.9% system uptime during normal operating business hours. Any unplanned downtime "
        "exceeding four (4) hours per calendar month shall entitle Client to a 10% credit against monthly fees."
    )
    doc.save(path)
    print(f"Created: {path}")

if __name__ == "__main__":
    create_acme_service_agreement()
    create_beta_master_agreement()
    create_acme_invoice()
    create_gamma_docx()
    print("All sample documents successfully generated.")
