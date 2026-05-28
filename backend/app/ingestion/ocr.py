import os
import shutil
from typing import Optional
from PIL import Image
from app.core.logging import logger

class OCRProcessor:
    """OCR processor with Tesseract CLI detection and fallback image text analysis."""

    def __init__(self):
        self.tesseract_available = self._check_tesseract()
        logger.info(f"OCRProcessor initialized. Tesseract available: {self.tesseract_available}")

    def _check_tesseract(self) -> bool:
        # Check system PATH or common Windows install locations
        if shutil.which("tesseract"):
            return True
        common_win_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
        ]
        for p in common_win_paths:
            if os.path.exists(p):
                return True
        return False

    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from an image file using available OCR or fallback."""
        if not os.path.exists(image_path):
            return ""

        if self.tesseract_available:
            try:
                import pytesseract
                img = Image.open(image_path)
                text = pytesseract.image_to_string(img)
                return text.strip()
            except Exception as e:
                logger.warning(f"Tesseract OCR failed on {image_path}: {e}")

        # Fallback inspection: Read basic metadata or inform scanned content
        try:
            with Image.open(image_path) as img:
                w, h = img.size
                return f"[Image document: resolution {w}x{h}, format {img.format}]"
        except Exception:
            return ""

ocr_processor = OCRProcessor()
