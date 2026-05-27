import os
import re
from typing import List, Dict, Any, Optional
import pymupdf  # PyMuPDF
import docx
from app.core.logging import logger
from app.ingestion.ocr import ocr_processor

class ParsedBlock:
    def __init__(self, text: str, page_number: int, block_type: str = "text", heading: str = ""):
        self.text = text
        self.page_number = page_number
        self.block_type = block_type  # text, heading, table, ocr
        self.heading = heading

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "page_number": self.page_number,
            "block_type": self.block_type,
            "heading": self.heading
        }

class DocumentParser:
    """Layout-aware multi-format document parser extracting text, headings, and tables."""

    def parse(self, file_path: str, file_type: str) -> List[ParsedBlock]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return self._parse_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            return self._parse_docx(file_path)
        elif ext in [".png", ".jpg", ".jpeg"]:
            return self._parse_image(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _parse_pdf(self, file_path: str) -> List[ParsedBlock]:
        blocks: List[ParsedBlock] = []
        doc = pymupdf.open(file_path)
        current_heading = "Document Start"

        for page_idx in range(len(doc)):
            page_num = page_idx + 1
            page = doc[page_idx]

            # 1. Extract tables if available via PyMuPDF table finder
            try:
                tabs = page.find_tables()
                if tabs and len(tabs.tables) > 0:
                    for tab in tabs.tables:
                        tab_data = tab.extract()
                        if tab_data:
                            # Format table into markdown
                            header = [str(c or "").strip() for c in tab_data[0]]
                            table_lines = [" | ".join(header), " | ".join(["---"] * len(header))]
                            for row in tab_data[1:]:
                                table_lines.append(" | ".join([str(c or "").strip() for c in row]))
                            table_md = "\n".join(table_lines)
                            blocks.append(ParsedBlock(
                                text=table_md,
                                page_number=page_num,
                                block_type="table",
                                heading=current_heading
                            ))
            except Exception as e:
                logger.debug(f"Table detection skipped on page {page_num}: {e}")

            # 2. Extract layout-aware text blocks
            page_dict = page.get_text("dict")
            page_blocks = page_dict.get("blocks", [])
            page_has_text = False

            for b in page_blocks:
                if "lines" not in b:
                    continue
                block_text_parts = []
                max_font_size = 0.0

                for line in b["lines"]:
                    line_spans = []
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        if text:
                            line_spans.append(text)
                            font_size = span.get("size", 10.0)
                            if font_size > max_font_size:
                                max_font_size = font_size
                    if line_spans:
                        block_text_parts.append(" ".join(line_spans))

                block_text = "\n".join(block_text_parts).strip()
                if not block_text:
                    continue

                page_has_text = True
                first_line = block_text.splitlines()[0].strip()
                if re.match(r"^(SECTION\s+\d+|ARTICLE\s+\d+|INVOICE\s+|SCHEDULE\s+|EXHIBIT\s+|PARTIES:)", first_line, re.IGNORECASE):
                    current_heading = first_line

                # Detect heading based on font size threshold or uppercase styling
                if max_font_size >= 13.0 or (block_text.isupper() and len(block_text) < 80):
                    current_heading = block_text
                    blocks.append(ParsedBlock(
                        text=block_text,
                        page_number=page_num,
                        block_type="heading",
                        heading=current_heading
                    ))
                else:
                    blocks.append(ParsedBlock(
                        text=block_text,
                        page_number=page_num,
                        block_type="text",
                        heading=current_heading
                    ))

            # 3. Fallback to OCR if page has negligible text (scanned page)
            if not page_has_text:
                logger.info(f"Page {page_num} of {file_path} contains no digital text; running OCR fallback.")
                pix = page.get_pixmap()
                img_path = f"{file_path}_page_{page_num}_tmp.png"
                try:
                    pix.save(img_path)
                    ocr_text = ocr_processor.extract_text_from_image(img_path)
                    if ocr_text:
                        blocks.append(ParsedBlock(
                            text=ocr_text,
                            page_number=page_num,
                            block_type="ocr",
                            heading=f"Page {page_num} (OCR Scanned)"
                        ))
                finally:
                    if os.path.exists(img_path):
                        os.remove(img_path)

        doc.close()
        return blocks

    def _parse_docx(self, file_path: str) -> List[ParsedBlock]:
        doc = docx.Document(file_path)
        blocks: List[ParsedBlock] = []
        current_heading = "Document Start"
        page_num = 1  # Standard estimation for DOCX without page breaks
        paragraph_count = 0

        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue

            paragraph_count += 1
            if paragraph_count % 30 == 0:
                page_num += 1

            if para.style and ("Heading" in para.style.name or para.style.name.startswith("Heading")):
                current_heading = text
                blocks.append(ParsedBlock(
                    text=text,
                    page_number=page_num,
                    block_type="heading",
                    heading=current_heading
                ))
            else:
                blocks.append(ParsedBlock(
                    text=text,
                    page_number=page_num,
                    block_type="text",
                    heading=current_heading
                ))

        # Parse DOCX Tables
        for table in doc.tables:
            table_lines = []
            for i, row in enumerate(table.rows):
                row_cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
                table_lines.append(" | ".join(row_cells))
                if i == 0:
                    table_lines.append(" | ".join(["---"] * len(row_cells)))
            if table_lines:
                blocks.append(ParsedBlock(
                    text="\n".join(table_lines),
                    page_number=page_num,
                    block_type="table",
                    heading=current_heading
                ))

        return blocks

    def _parse_image(self, file_path: str) -> List[ParsedBlock]:
        text = ocr_processor.extract_text_from_image(file_path)
        return [ParsedBlock(
            text=text if text else "[Image: No extractable text detected]",
            page_number=1,
            block_type="ocr",
            heading="Image Document"
        )]

document_parser = DocumentParser()
