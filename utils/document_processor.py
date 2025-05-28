# utils/document_processor.py
import io
from pypdf import PdfReader


class DocumentProcessor:
    def extract_text_from_pdf(self, pdf_file_buffer: io.BytesIO) -> str:
        """Extracts text from a PDF file buffer."""
        reader = PdfReader(pdf_file_buffer)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    def process_text_file(self, text_file_buffer: io.StringIO) -> str:
        """Reads text from a text file buffer."""
        return text_file_buffer.read()